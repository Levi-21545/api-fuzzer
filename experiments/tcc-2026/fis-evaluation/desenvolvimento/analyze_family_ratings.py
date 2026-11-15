#!/usr/bin/env python3
"""Build consensus and compare blinded family ratings with FIS variants."""

from __future__ import annotations

import importlib.util
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from scipy.stats import spearmanr

from fuzzer.analysis.fuzzy_engine import FuzzyEngine
from fuzzer.executor.result import ExecutionResult
from fuzzer.parser.openapi_parser import parse_openapi


HERE = Path(__file__).resolve().parent
EXPORTER_PATH = HERE / "export_blind_items.py"
RATER_PATHS = [HERE / f"family_rater_{name}.json" for name in ("a", "b", "c")]
ADJUDICATION_PATH = HERE / "family_adjudication.json"
PRIORITIES = ("LOW", "MEDIUM", "HIGH")
VALIDITIES = ("SUPPORTED", "NOT_SUPPORTED", "INDETERMINATE")
ORDINAL = {"LOW": 0, "MEDIUM": 1, "HIGH": 2}
MODEL_VARIANTS = ("v2", "status_only", "v3", "rubric_candidate")
EXPECTED_REJECTION_CONTEXTS = {
    "invalid_mutation",
    "missing_credential",
    "invalid_credential",
}


def _load_exporter() -> Any:
    spec = importlib.util.spec_from_file_location("blind_export", EXPORTER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load blind exporter")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_ratings(expected_ids: list[str]) -> list[dict[str, dict[str, Any]]]:
    loaded: list[dict[str, dict[str, Any]]] = []
    for path in RATER_PATHS:
        records = json.loads(path.read_text(encoding="utf-8"))
        ids = [record.get("blind_id") for record in records]
        if ids != expected_ids:
            raise ValueError(f"{path.name} does not preserve the 161 blind IDs")
        for record in records:
            if record.get("validity") not in VALIDITIES:
                raise ValueError(f"invalid validity in {path.name}: {record}")
            priority = record.get("priority")
            if record["validity"] == "SUPPORTED" and priority not in PRIORITIES:
                raise ValueError(f"missing priority in {path.name}: {record}")
            if record["validity"] != "SUPPORTED" and priority is not None:
                raise ValueError(f"unexpected priority in {path.name}: {record}")
        loaded.append({record["blind_id"]: record for record in records})
    return loaded


def _majority(values: list[str]) -> str | None:
    counts = Counter(values)
    value, count = counts.most_common(1)[0]
    return value if count >= 2 else None


def _consensus(
    families: list[dict[str, Any]],
    raters: list[dict[str, dict[str, Any]]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    resolved: list[dict[str, Any]] = []
    unresolved: list[dict[str, Any]] = []
    for family in families:
        blind_id = family["blind_id"]
        records = [rater[blind_id] for rater in raters]
        validity = _majority([record["validity"] for record in records])
        priority = None
        if validity == "SUPPORTED":
            supported = [
                record["priority"]
                for record in records
                if record["validity"] == "SUPPORTED"
            ]
            priority = _majority(supported)
        consensus = {
            "blind_id": blind_id,
            "validity": validity,
            "priority": priority,
            "ratings": [
                {
                    "validity": record["validity"],
                    "priority": record["priority"],
                }
                for record in records
            ],
        }
        if validity is None or (validity == "SUPPORTED" and priority is None):
            unresolved.append(consensus)
        else:
            resolved.append(consensus)
    return resolved, unresolved


def _execution_result(record: dict[str, Any], endpoint: Any) -> ExecutionResult:
    return ExecutionResult(
        case_id=record["case_id"],
        endpoint_id=record["endpoint_id"],
        method=endpoint.method,
        url=record.get("url") or "",
        status_code=record.get("status_code"),
        response_time_ms=float(record.get("response_time_ms") or 0),
        response_size=record.get("response_size"),
        raw_response=record.get("raw_response"),
        error=record.get("error"),
    )


def _rubric_candidate_prediction(family: dict[str, Any]) -> dict[str, Any]:
    """Prioritize from request and response facts, without analyzer labels.

    This is a development-only, family-level candidate. Repetition is available
    after deduplication and therefore acts as an evidence modifier here; the
    online finding-level FIS must remain explicit about that separation.
    """
    context = family["review_context"]
    expects_rejection = context in EXPECTED_REJECTION_CONTEXTS
    status = family["observation_summary"]["status_code"]
    documented = family["contract"]["observed_status_documented"]
    schema_counts = family["contract"]["response_schema_validity_counts"]
    schema_invalid = int(schema_counts.get("False", 0)) > 0
    repeated_with_support = int(family["occurrence_count"]) >= 3
    requires_authentication = family["endpoint"]["requires_authentication"]

    if status is None:
        priority = "MEDIUM" if expects_rejection else "HIGH"
        reason = "transport failure, moderated when rejection was expected"
    elif 500 <= status < 600:
        if expects_rejection:
            priority = "MEDIUM"
            reason = "server failure while processing an intentionally invalid request"
        elif repeated_with_support:
            priority = "HIGH"
            reason = (
                "server failure repeated at least three times for a "
                "generated-valid request"
            )
        else:
            priority = "MEDIUM"
            reason = "isolated server failure for a request expected to be valid"
    elif 200 <= status < 300 and expects_rejection:
        if context == "missing_credential" and requires_authentication:
            priority = "HIGH"
            reason = "authenticated operation accepted a request with no credential"
        else:
            priority = "MEDIUM"
            reason = "request expected to be rejected was accepted"
    elif 200 <= status < 300 and schema_invalid:
        priority = "MEDIUM"
        reason = "successful response body diverged from the documented schema"
    elif 200 <= status < 300 and not documented:
        priority = "LOW"
        reason = (
            "successful response used an undocumented status without "
            "stronger contradiction"
        )
    elif 300 <= status < 500 and expects_rejection:
        priority = "LOW"
        reason = "request expected to be rejected was rejected safely"
    elif 300 <= status < 500:
        priority = "LOW"
        reason = (
            "generated-valid request was rejected without proof that "
            "semantic preconditions held"
        )
    elif not documented or schema_invalid:
        priority = "MEDIUM"
        reason = "observed response diverged from the documented contract"
    else:
        priority = "LOW"
        reason = "no stronger technical-priority condition was observed"

    return {
        "score": {"LOW": 0.17, "MEDIUM": 0.5, "HIGH": 0.83}[priority],
        "priority": priority,
        "member_priorities": {priority: family["signature_count"]},
        "reason": reason,
    }


def _family_predictions(
    exporter: Any, families: list[dict[str, Any]]
) -> dict[str, dict[str, dict[str, Any]]]:
    raw: dict[str, tuple[dict[str, Any], Any]] = {}
    root = exporter.PILOTS_ROOT
    for target, run_id in exporter.RUNS.items():
        run_dir = root / target / run_id
        manifest = exporter._json(run_dir / "run_manifest.json")
        spec = parse_openapi(str(run_dir / manifest["inputs"]["schema"]))
        endpoints = {endpoint.id: endpoint for endpoint in spec.endpoints}
        for unique in exporter._json(run_dir / "analysis/findings_unique.json"):
            raw[unique["signature"]["id"]] = (unique, endpoints)

    engine = FuzzyEngine()
    predictions: dict[str, dict[str, dict[str, Any]]] = {}
    for family in families:
        variants: dict[str, list[tuple[float, str]]] = {
            "v2": [],
            "status_only": [],
            "v3": [],
        }
        for signature_id in family["_member_signature_ids"]:
            unique, endpoints = raw[signature_id]
            plan = unique["representative"]["plan"]
            record = unique["representative"]["result"]
            finding = unique["representative"]["finding"]
            endpoint = endpoints[record["endpoint_id"]]
            result = _execution_result(record, endpoint)
            mutations = plan.get("mutations") or []
            expects_rejection = plan.get("case_kind") == "auth_probe" or any(
                not mutation.get("expected_valid", False) for mutation in mutations
            )
            stored = finding.get("severity_assessment") or {}
            if stored.get("model_id") != "mamdani-status-time-response-size-v2":
                raise ValueError("canonical artifact does not contain a v2 assessment")
            deviation = float(stored["inputs"]["status_deviation"])
            if deviation >= 0.66:
                status_priority = "HIGH"
            elif deviation >= 0.33:
                status_priority = "MEDIUM"
            else:
                status_priority = "LOW"
            auth_probe_kind = None
            if plan.get("case_kind") == "auth_probe":
                headers = {
                    str(name).casefold()
                    for name in (plan.get("headers") or {})
                    if str(name).casefold() not in {"accept", "content-type"}
                }
                auth_probe_kind = (
                    "invalid_credential" if headers else "missing_credential"
                )
            status = result.status_code
            strong_repetition = (
                int(unique.get("occurrence_count") or 0) >= 3
                and not expects_rejection
                and (status is None or 500 <= status < 600)
            )
            current = engine.assess(
                endpoint,
                result,
                expects_rejection,
                case_kind=str(plan.get("case_kind") or "baseline"),
                auth_probe_kind=auth_probe_kind,
                evidence_strength=1.0 if strong_repetition else 0.5,
            )
            variants["v2"].append(
                (float(finding["severity_score"]), str(finding["severity"]))
            )
            variants["status_only"].append((deviation, status_priority))
            variants["v3"].append((current.score, current.severity.name))

        predictions[family["blind_id"]] = {
            name: {
                "score": max(values, key=lambda value: value[0])[0],
                "priority": max(values, key=lambda value: value[0])[1],
                "member_priorities": dict(
                    sorted(Counter(value[1] for value in values).items())
                ),
            }
            for name, values in variants.items()
        }
        predictions[family["blind_id"]]["rubric_candidate"] = (
            _rubric_candidate_prediction(family)
        )
    return predictions


def _metrics(
    references: dict[str, str],
    predictions: dict[str, dict[str, dict[str, Any]]],
) -> dict[str, Any]:
    results: dict[str, Any] = {}
    for model in MODEL_VARIANTS:
        pairs = [
            (reference, predictions[blind_id][model]["priority"])
            for blind_id, reference in references.items()
        ]
        confusion = Counter(
            f"{reference}->{predicted}" for reference, predicted in pairs
        )
        accuracy = sum(reference == predicted for reference, predicted in pairs) / len(
            pairs
        )
        mae = sum(
            abs(ORDINAL[reference] - ORDINAL[predicted])
            for reference, predicted in pairs
        ) / len(pairs)
        f1_values: list[float] = []
        for label in PRIORITIES:
            true_positive = sum(r == label and p == label for r, p in pairs)
            false_positive = sum(r != label and p == label for r, p in pairs)
            false_negative = sum(r == label and p != label for r, p in pairs)
            denominator = 2 * true_positive + false_positive + false_negative
            f1_values.append(
                0.0 if denominator == 0 else 2 * true_positive / denominator
            )
        scores = [predictions[blind_id][model]["score"] for blind_id in references]
        labels = [ORDINAL[references[blind_id]] for blind_id in references]
        correlation = spearmanr(scores, labels).statistic
        results[model] = {
            "n": len(pairs),
            "accuracy": round(accuracy, 4),
            "macro_f1_three_classes": round(sum(f1_values) / 3, 4),
            "ordinal_mae": round(mae, 4),
            "spearman": None if correlation != correlation else round(correlation, 4),
            "confusion": dict(sorted(confusion.items())),
        }
    return results


def _apply_adjudication(
    resolved: list[dict[str, Any]],
    unresolved: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    if not ADJUDICATION_PATH.is_file():
        return resolved, unresolved
    adjudicated = json.loads(ADJUDICATION_PATH.read_text(encoding="utf-8"))
    expected = {record["blind_id"] for record in unresolved}
    received = {record.get("blind_id") for record in adjudicated}
    if received != expected:
        raise ValueError("adjudication IDs do not match unresolved family IDs")
    additions: list[dict[str, Any]] = []
    still_unresolved: list[dict[str, Any]] = []
    for record in adjudicated:
        validity = record.get("validity")
        priority = record.get("priority")
        if validity not in VALIDITIES:
            raise ValueError(f"invalid adjudicated validity: {record}")
        if validity == "SUPPORTED" and priority not in PRIORITIES:
            still_unresolved.append(record)
            continue
        if validity != "SUPPORTED" and priority is not None:
            raise ValueError(f"unexpected adjudicated priority: {record}")
        additions.append(
            {
                "blind_id": record["blind_id"],
                "validity": validity,
                "priority": priority,
                "adjudicated": True,
            }
        )
    return resolved + additions, still_unresolved


def _breakdowns(
    families: list[dict[str, Any]],
    references: dict[str, str],
    predictions: dict[str, dict[str, dict[str, Any]]],
) -> dict[str, Any]:
    dimensions = {
        "api": lambda family: family["target"],
        "analyzer_classification": lambda family: family["_classification"],
        "review_context": lambda family: family["review_context"],
    }
    output: dict[str, Any] = {}
    for dimension, getter in dimensions.items():
        grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for family in families:
            if family["blind_id"] in references:
                grouped[str(getter(family))].append(family)
        output[dimension] = {}
        for group, members in sorted(grouped.items()):
            v2_pairs = [
                (
                    references[family["blind_id"]],
                    predictions[family["blind_id"]]["v2"]["priority"],
                )
                for family in members
            ]
            candidate_pairs = [
                (
                    references[family["blind_id"]],
                    predictions[family["blind_id"]]["rubric_candidate"]["priority"],
                )
                for family in members
            ]
            output[dimension][group] = {
                "n": len(members),
                "reference": dict(
                    sorted(Counter(pair[0] for pair in v2_pairs).items())
                ),
                "v2_prediction": dict(
                    sorted(Counter(pair[1] for pair in v2_pairs).items())
                ),
                "v2_accuracy": round(
                    sum(reference == predicted for reference, predicted in v2_pairs)
                    / len(v2_pairs),
                    4,
                ),
                "v2_confusion": dict(
                    sorted(
                        Counter(
                            f"{reference}->{predicted}"
                            for reference, predicted in v2_pairs
                        ).items()
                    )
                ),
                "rubric_candidate_prediction": dict(
                    sorted(Counter(pair[1] for pair in candidate_pairs).items())
                ),
                "rubric_candidate_accuracy": round(
                    sum(
                        reference == predicted
                        for reference, predicted in candidate_pairs
                    )
                    / len(candidate_pairs),
                    4,
                ),
                "rubric_candidate_confusion": dict(
                    sorted(
                        Counter(
                            f"{reference}->{predicted}"
                            for reference, predicted in candidate_pairs
                        ).items()
                    )
                ),
            }
    return output


def main() -> None:
    exporter = _load_exporter()
    families = exporter._load_families()
    ids = [family["blind_id"] for family in families]
    raters = _load_ratings(ids)
    resolved, unresolved = _consensus(families, raters)
    final_records, remaining_unresolved = _apply_adjudication(resolved, unresolved)
    predictions = _family_predictions(exporter, families)
    references = {
        record["blind_id"]: record["priority"]
        for record in final_records
        if record["validity"] == "SUPPORTED"
    }
    validity_counts = Counter(record["validity"] for record in final_records)
    priority_counts = Counter(references.values())
    variant_band_differences = {
        model: sum(
            predictions[family["blind_id"]][model]["priority"]
            != predictions[family["blind_id"]]["v2"]["priority"]
            for family in families
        )
        for model in ("status_only", "v3", "rubric_candidate")
    }
    exact_validity = sum(
        len({rater[family["blind_id"]]["validity"] for rater in raters}) == 1
        for family in families
    )
    exact_priority = sum(
        len(
            {
                rater[family["blind_id"]]["priority"]
                for rater in raters
                if rater[family["blind_id"]]["validity"] == "SUPPORTED"
            }
        )
        == 1
        for family in families
        if all(
            rater[family["blind_id"]]["validity"] == "SUPPORTED"
            for rater in raters
        )
    )
    unanimous_supported = sum(
        all(
            rater[family["blind_id"]]["validity"] == "SUPPORTED"
            for rater in raters
        )
        for family in families
    )
    output = {
        "families": len(families),
        "resolved_without_adjudication": len(resolved),
        "adjudicated": len(final_records) - len(resolved),
        "unresolved_before_adjudication": unresolved,
        "remaining_unresolved": remaining_unresolved,
        "agreement": {
            "exact_validity": exact_validity,
            "exact_validity_rate": round(exact_validity / len(families), 4),
            "unanimously_supported": unanimous_supported,
            "exact_priority_among_unanimously_supported": exact_priority,
            "exact_priority_rate": (
                None
                if unanimous_supported == 0
                else round(exact_priority / unanimous_supported, 4)
            ),
        },
        "consensus_validity": dict(sorted(validity_counts.items())),
        "consensus_priority": dict(sorted(priority_counts.items())),
        "variant_band_differences_from_v2": variant_band_differences,
        "metrics_final": _metrics(references, predictions),
        "breakdowns": _breakdowns(families, references, predictions),
        "rubric_candidate_mismatches": [
            {
                "blind_id": family["blind_id"],
                "target": family["target"],
                "classification": family["_classification"],
                "review_context": family["review_context"],
                "status_code": family["observation_summary"]["status_code"],
                "status_documented": family["contract"][
                    "observed_status_documented"
                ],
                "occurrence_count": family["occurrence_count"],
                "reference": references[family["blind_id"]],
                "prediction": predictions[family["blind_id"]]["rubric_candidate"][
                    "priority"
                ],
                "reason": predictions[family["blind_id"]]["rubric_candidate"][
                    "reason"
                ],
            }
            for family in families
            if family["blind_id"] in references
            and references[family["blind_id"]]
            != predictions[family["blind_id"]]["rubric_candidate"]["priority"]
        ],
    }
    print(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
