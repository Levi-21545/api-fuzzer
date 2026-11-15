#!/usr/bin/env python3
"""Validate blind ratings, compute majority, and prepare adjudication."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
BLIND_PATH = HERE / "blind_families.json"
RATER_PATHS = [HERE / f"rater_{name}.json" for name in ("a", "b", "c")]
ADJUDICATION_PATH = HERE / "adjudication.json"
PACKET_PATH = HERE / "adjudication_packet.json"
CONSENSUS_PATH = HERE / "consensus.json"
VALIDITIES = {"SUPPORTED", "NOT_SUPPORTED", "INDETERMINATE"}
PRIORITIES = {"LOW", "MEDIUM", "HIGH"}
EXPECTED_FIELDS = {
    "blind_id",
    "validity",
    "priority",
    "confidence",
    "rationale",
    "missing_evidence",
}


def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _validate_records(
    path: Path,
    records: Any,
    expected_ids: list[str],
) -> list[dict[str, Any]]:
    if not isinstance(records, list) or len(records) != len(expected_ids):
        raise ValueError(f"{path.name}: expected {len(expected_ids)} records")
    if [record.get("blind_id") for record in records] != expected_ids:
        raise ValueError(f"{path.name}: IDs or order differ from blind corpus")
    for record in records:
        if set(record) != EXPECTED_FIELDS:
            raise ValueError(f"{path.name}: unexpected fields in {record}")
        validity = record.get("validity")
        priority = record.get("priority")
        confidence = record.get("confidence")
        if validity not in VALIDITIES:
            raise ValueError(f"{path.name}: invalid validity in {record}")
        if validity == "SUPPORTED" and priority not in PRIORITIES:
            raise ValueError(f"{path.name}: supported record without priority")
        if validity != "SUPPORTED" and priority is not None:
            raise ValueError(f"{path.name}: unsupported record with priority")
        if not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1:
            raise ValueError(f"{path.name}: invalid confidence in {record}")
        if not isinstance(record.get("rationale"), str):
            raise ValueError(f"{path.name}: rationale must be a string")
        if not isinstance(record.get("missing_evidence"), list):
            raise ValueError(f"{path.name}: missing_evidence must be a list")
    return records


def _majority(values: list[str]) -> str | None:
    value, count = Counter(values).most_common(1)[0]
    return value if count >= 2 else None


def _load_adjudication(expected_ids: list[str]) -> dict[str, dict[str, Any]]:
    if not ADJUDICATION_PATH.is_file():
        return {}
    records = _validate_records(
        ADJUDICATION_PATH,
        _json(ADJUDICATION_PATH),
        expected_ids,
    )
    return {record["blind_id"]: record for record in records}


def main() -> None:
    blind = _json(BLIND_PATH)
    families = blind["families"]
    ids = [family["blind_id"] for family in families]
    raters = [
        _validate_records(path, _json(path), ids)
        for path in RATER_PATHS
    ]

    resolved: list[dict[str, Any]] = []
    unresolved: list[dict[str, Any]] = []
    for index, blind_id in enumerate(ids):
        ratings = [rater[index] for rater in raters]
        validity = _majority([rating["validity"] for rating in ratings])
        priority = None
        if validity == "SUPPORTED":
            supported_priorities = [
                rating["priority"]
                for rating in ratings
                if rating["validity"] == "SUPPORTED"
            ]
            priority = _majority(supported_priorities)
        record = {
            "blind_id": blind_id,
            "validity": validity,
            "priority": priority,
            "source": "majority",
            "ratings": [
                {
                    "validity": rating["validity"],
                    "priority": rating["priority"],
                    "confidence": rating["confidence"],
                }
                for rating in ratings
            ],
        }
        if validity is None or (validity == "SUPPORTED" and priority is None):
            unresolved.append(record)
        else:
            resolved.append(record)

    unresolved_ids = [record["blind_id"] for record in unresolved]
    by_id = {family["blind_id"]: family for family in families}
    packet = {
        "schema_version": "meilisearch-confirmatory-adjudication-v1",
        "instructions": blind["instructions"],
        "families": [by_id[blind_id] for blind_id in unresolved_ids],
    }
    PACKET_PATH.write_text(
        json.dumps(packet, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    adjudication = _load_adjudication(unresolved_ids)
    final = list(resolved)
    remaining = list(unresolved)
    if adjudication:
        final.extend(
            {
                "blind_id": blind_id,
                "validity": adjudication[blind_id]["validity"],
                "priority": adjudication[blind_id]["priority"],
                "source": "adjudication",
                "ratings": next(
                    record["ratings"]
                    for record in unresolved
                    if record["blind_id"] == blind_id
                ),
            }
            for blind_id in unresolved_ids
        )
        remaining = []

    final_by_id = {record["blind_id"]: record for record in final}
    ordered_final = [
        final_by_id[blind_id]
        for blind_id in ids
        if blind_id in final_by_id
    ]
    exact_validity = sum(
        len({rater[index]["validity"] for rater in raters}) == 1
        for index in range(len(ids))
    )
    unanimously_supported_indexes = [
        index
        for index in range(len(ids))
        if all(rater[index]["validity"] == "SUPPORTED" for rater in raters)
    ]
    exact_priority = sum(
        len({rater[index]["priority"] for rater in raters}) == 1
        for index in unanimously_supported_indexes
    )
    output = {
        "schema_version": "meilisearch-confirmatory-consensus-v1",
        "families": len(ids),
        "resolved_by_majority": len(resolved),
        "unresolved_before_adjudication": unresolved,
        "adjudicated": len(adjudication),
        "remaining_unresolved": remaining,
        "agreement": {
            "exact_validity": exact_validity,
            "exact_validity_rate": round(exact_validity / len(ids), 4),
            "unanimously_supported": len(unanimously_supported_indexes),
            "exact_priority_among_unanimously_supported": exact_priority,
            "exact_priority_rate": (
                None
                if not unanimously_supported_indexes
                else round(exact_priority / len(unanimously_supported_indexes), 4)
            ),
        },
        "final_validity": dict(
            sorted(Counter(record["validity"] for record in ordered_final).items())
        ),
        "final_priority": dict(
            sorted(
                Counter(
                    record["priority"]
                    for record in ordered_final
                    if record["validity"] == "SUPPORTED"
                ).items()
            )
        ),
        "reference": ordered_final,
    }
    CONSENSUS_PATH.write_text(
        json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "families": len(ids),
                "resolved_by_majority": len(resolved),
                "unresolved": len(unresolved),
                "adjudicated": len(adjudication),
                "remaining": len(remaining),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
