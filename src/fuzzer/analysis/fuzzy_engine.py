from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Literal

import numpy as np
import skfuzzy as fuzz
from jsonschema import ValidationError, validate
from skfuzzy import control as ctrl
from skfuzzy.control import ControlSystem

from fuzzer.analysis.classification import AnomalySeverity
from fuzzer.executor.result import ExecutionResult
from fuzzer.model.endpoint import Endpoint


_HIGH_THRESHOLD = 0.66
_MEDIUM_THRESHOLD = 0.33
FUZZY_MODEL_ID = "mamdani-behavior-evidence-access-v3"

_RULE_DESCRIPTIONS = {
    "R1_LOW_CONTRADICTION": "low behavioral contradiction -> low priority",
    "R2_MEDIUM_CONTRADICTION": (
        "medium behavioral contradiction -> medium priority"
    ),
    "R3_HIGH_CONTRADICTION_WEAK_EVIDENCE": (
        "high contradiction with limited evidence -> medium priority"
    ),
    "R4_HIGH_CONTRADICTION_STRONG_EVIDENCE": (
        "high contradiction with strong evidence -> high priority"
    ),
    "R5_POTENTIAL_ACCESS_EXPOSURE": (
        "potential access-control exposure -> medium priority"
    ),
    "R6_CLEAR_ACCESS_EXPOSURE": (
        "clear access-control exposure -> high priority"
    ),
}


@dataclass(frozen=True)
class FuzzyAssessment:
    model_id: str
    score: float
    severity: AnomalySeverity
    inputs: dict[str, float]
    memberships: dict[str, dict[str, float]]
    activated_rules: list[dict[str, Any]]
    fallback_used: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "model_id": self.model_id,
            "inputs": self.inputs,
            "memberships": self.memberships,
            "activated_rules": self.activated_rules,
            "fallback_used": self.fallback_used,
        }


class FuzzyEngine:
    def __init__(self) -> None:
        self._system = self._build_system()

    def _build_system(self) -> ControlSystem:
        contradiction = ctrl.Antecedent(
            np.arange(0, 1.01, 0.01), "behavior_contradiction"
        )
        evidence = ctrl.Antecedent(
            np.arange(0, 1.01, 0.01), "evidence_strength"
        )
        access = ctrl.Antecedent(
            np.arange(0, 1.01, 0.01), "access_control_exposure"
        )
        ascore = ctrl.Consequent(np.arange(0, 1.01, 0.01), "anomaly_score")

        contradiction["low"] = fuzz.trapmf(
            contradiction.universe, [0, 0, 0.2, 0.4]
        )
        contradiction["medium"] = fuzz.trimf(
            contradiction.universe, [0.25, 0.55, 0.8]
        )
        contradiction["high"] = fuzz.trapmf(
            contradiction.universe, [0.7, 0.85, 1, 1]
        )

        evidence["limited"] = fuzz.trapmf(
            evidence.universe, [0, 0, 0.4, 0.7]
        )
        evidence["strong"] = fuzz.trapmf(
            evidence.universe, [0.6, 0.8, 1, 1]
        )

        access["none"] = fuzz.trapmf(access.universe, [0, 0, 0.1, 0.3])
        access["potential"] = fuzz.trimf(access.universe, [0.2, 0.6, 0.85])
        access["clear"] = fuzz.trapmf(access.universe, [0.7, 0.9, 1, 1])

        ascore["low"] = fuzz.trapmf(ascore.universe, [0, 0, 0.2, 0.4])
        ascore["medium"] = fuzz.trimf(ascore.universe, [0.25, 0.5, 0.75])
        ascore["high"] = fuzz.trapmf(ascore.universe, [0.6, 0.8, 1, 1])

        rules = [
            ctrl.Rule(
                contradiction["low"],
                ascore["low"],
                label="R1_LOW_CONTRADICTION",
            ),
            ctrl.Rule(
                contradiction["medium"],
                ascore["medium"],
                label="R2_MEDIUM_CONTRADICTION",
            ),
            ctrl.Rule(
                contradiction["high"] & evidence["limited"],
                ascore["medium"],
                label="R3_HIGH_CONTRADICTION_WEAK_EVIDENCE",
            ),
            ctrl.Rule(
                contradiction["high"] & evidence["strong"],
                ascore["high"],
                label="R4_HIGH_CONTRADICTION_STRONG_EVIDENCE",
            ),
            ctrl.Rule(
                access["potential"],
                ascore["medium"],
                label="R5_POTENTIAL_ACCESS_EXPOSURE",
            ),
            ctrl.Rule(
                access["clear"],
                ascore["high"],
                label="R6_CLEAR_ACCESS_EXPOSURE",
            ),
        ]

        return ctrl.ControlSystem(rules)

    def _response_contract_state(
        self,
        endpoint: Endpoint,
        result: ExecutionResult,
    ) -> tuple[bool, bool | None]:
        status_key = str(result.status_code)
        if result.status_code is None or status_key not in endpoint.responses:
            return False, None
        try:
            body = json.loads(result.raw_response or "null")
            validate(body, endpoint.responses[status_key].to_jsonschema())
        except (json.JSONDecodeError, ValidationError):
            return True, False
        return True, True

    def _compute_behavior_contradiction(
        self,
        endpoint: Endpoint,
        result: ExecutionResult,
        expects_rejection: bool,
    ) -> float:
        status = result.status_code
        if status is None or 500 <= status < 600:
            return 1.0

        documented, schema_valid = self._response_contract_state(endpoint, result)
        if expects_rejection:
            return 0.7 if 200 <= status < 300 else 0.15

        if 200 <= status < 300:
            if schema_valid is False:
                return 0.65
            return 0.0 if documented else 0.25

        if 300 <= status < 500:
            if status == 400 and not documented and endpoint.request_body is not None:
                return 0.6
            return 0.2
        return 0.4

    def _compute_access_control_exposure(
        self,
        result: ExecutionResult,
        case_kind: str,
        auth_probe_kind: str | None,
    ) -> float:
        status = result.status_code
        if case_kind != "auth_probe" or status is None or not 200 <= status < 300:
            return 0.0
        if auth_probe_kind == "missing_credential":
            return 1.0
        return 0.6

    def assess(
        self,
        endpoint: Endpoint,
        result: ExecutionResult,
        expects_rejection: bool = False,
        *,
        case_kind: Literal["baseline", "mutation", "auth_probe"] = "baseline",
        auth_probe_kind: Literal[
            "missing_credential", "invalid_credential"
        ]
        | None = None,
        evidence_strength: float = 0.5,
    ) -> FuzzyAssessment:
        contradiction = self._compute_behavior_contradiction(
            endpoint, result, expects_rejection
        )
        evidence_strength = max(0.0, min(float(evidence_strength), 1.0))
        inputs = {
            "behavior_contradiction": contradiction,
            "evidence_strength": evidence_strength,
            "access_control_exposure": self._compute_access_control_exposure(
                result, case_kind, auth_probe_kind
            ),
        }

        sim = ctrl.ControlSystemSimulation(self._system)
        for name, value in inputs.items():
            sim.input[name] = value

        fallback_used = False
        activated_rules: list[dict[str, Any]] = []
        try:
            sim.compute()
            score_val = float(sim.output["anomaly_score"])
            for rule in self._system.rules:
                strength = float(rule.aggregate_firing[sim])
                if strength > 0:
                    activated_rules.append(
                        {
                            "id": str(rule.label),
                            "description": _RULE_DESCRIPTIONS[str(rule.label)],
                            "strength": round(strength, 4),
                        }
                    )
        except (ValueError, KeyError, TypeError):
            score_val = contradiction
            fallback_used = True

        score_val = max(0.0, min(1.0, score_val))

        if score_val >= _HIGH_THRESHOLD:
            severity = AnomalySeverity.HIGH
        elif score_val >= _MEDIUM_THRESHOLD:
            severity = AnomalySeverity.MEDIUM
        else:
            severity = AnomalySeverity.LOW

        activated_rules.sort(key=lambda item: (-item["strength"], item["id"]))
        return FuzzyAssessment(
            model_id=FUZZY_MODEL_ID,
            score=round(score_val, 2),
            severity=severity,
            inputs=inputs,
            memberships=self._memberships(inputs),
            activated_rules=activated_rules,
            fallback_used=fallback_used,
        )

    def score(
        self,
        endpoint: Endpoint,
        result: ExecutionResult,
        expects_rejection: bool = False,
        **context: Any,
    ) -> tuple[float, AnomalySeverity]:
        """Return the legacy score tuple while assessment consumers migrate."""
        assessment = self.assess(
            endpoint,
            result,
            expects_rejection,
            **context,
        )
        return assessment.score, assessment.severity

    def _memberships(self, inputs: dict[str, float]) -> dict[str, dict[str, float]]:
        memberships: dict[str, dict[str, float]] = {}
        for antecedent in self._system.antecedents:
            value = inputs[antecedent.label]
            memberships[antecedent.label] = {
                term_name: round(
                    float(
                        fuzz.interp_membership(
                            antecedent.universe,
                            term.mf,
                            value,
                        )
                    ),
                    4,
                )
                for term_name, term in antecedent.terms.items()
            }
        return memberships
