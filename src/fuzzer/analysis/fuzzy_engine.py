from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from skfuzzy.control import ControlSystem

from fuzzer.analysis.classification import AnomalySeverity
from fuzzer.executor.result import ExecutionResult
from fuzzer.model.endpoint import Endpoint


_DEVIATION_NO_STATUS = 1.0
_DEVIATION_SERVER_ERROR = 1.0
_DEVIATION_EXPECTED = 0.0
_DEVIATION_NO_REFERENCE = 0.5
_DEVIATION_CLIENT_ERROR = 0.6
_DEVIATION_OTHER = 0.4
_DEVIATION_UNEXPECTED_ACCEPTANCE = 0.6

_HIGH_THRESHOLD = 0.66
_MEDIUM_THRESHOLD = 0.33
FUZZY_MODEL_ID = "mamdani-status-time-response-size-v2"

_RULE_DESCRIPTIONS = {
    "R1_HIGH_DEVIATION_OR_TIMEOUT": (
        "high status deviation or timeout response -> high severity"
    ),
    "R2_MEDIUM_DEVIATION": "medium status deviation -> medium severity",
    "R3_LOW_DEVIATION": "low status deviation -> low severity",
    "R4_LOW_DEVIATION_WITH_RESPONSE_SIGNAL": (
        "low status deviation with slow, empty, or large response -> medium severity"
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
        dev = ctrl.Antecedent(np.arange(0, 1.01, 0.01), "status_deviation")
        rtime = ctrl.Antecedent(np.arange(0, 5001, 1), "response_time_ms")
        rsize = ctrl.Antecedent(np.arange(0, 3.01, 0.01), "response_size_signal")
        ascore = ctrl.Consequent(np.arange(0, 1.01, 0.01), "anomaly_score")

        dev["low"] = fuzz.trapmf(dev.universe, [0, 0, 0.2, 0.4])
        dev["medium"] = fuzz.trimf(dev.universe, [0.2, 0.5, 0.8])
        dev["high"] = fuzz.trapmf(dev.universe, [0.6, 0.8, 1, 1])

        rtime["normal"] = fuzz.trapmf(rtime.universe, [0, 0, 200, 500])
        rtime["slow"] = fuzz.trimf(rtime.universe, [200, 800, 2000])
        rtime["timeout"] = fuzz.trapmf(rtime.universe, [1000, 2500, 5000, 5000])

        rsize["expected"] = fuzz.trapmf(rsize.universe, [0, 0, 0.5, 1.5])
        rsize["large"] = fuzz.trimf(rsize.universe, [1, 2, 3])
        rsize["empty"] = fuzz.trimf(rsize.universe, [0, 0, 0.3])

        ascore["low"] = fuzz.trapmf(ascore.universe, [0, 0, 0.2, 0.4])
        ascore["medium"] = fuzz.trimf(ascore.universe, [0.25, 0.5, 0.75])
        ascore["high"] = fuzz.trapmf(ascore.universe, [0.6, 0.8, 1, 1])

        rules = [
            ctrl.Rule(
                dev["high"] | rtime["timeout"],
                ascore["high"],
                label="R1_HIGH_DEVIATION_OR_TIMEOUT",
            ),
            ctrl.Rule(
                dev["medium"],
                ascore["medium"],
                label="R2_MEDIUM_DEVIATION",
            ),
            ctrl.Rule(
                dev["low"],
                ascore["low"],
                label="R3_LOW_DEVIATION",
            ),
            ctrl.Rule(
                dev["low"]
                & (rtime["slow"] | rsize["empty"] | rsize["large"]),
                ascore["medium"],
                label="R4_LOW_DEVIATION_WITH_RESPONSE_SIGNAL",
            ),
        ]

        return ctrl.ControlSystem(rules)

    def _compute_deviation(
        self,
        endpoint: Endpoint,
        result: ExecutionResult,
        expects_rejection: bool = False,
    ) -> float:
        if result.status_code is None:
            return _DEVIATION_NO_STATUS
        actual = result.status_code
        if 500 <= actual < 600:
            return _DEVIATION_SERVER_ERROR
        if expects_rejection and 200 <= actual < 300:
            return _DEVIATION_UNEXPECTED_ACCEPTANCE
        expected = {int(s) for s in endpoint.responses if s.isdigit()}
        if actual in expected:
            return _DEVIATION_EXPECTED
        if not expected:
            return _DEVIATION_NO_REFERENCE
        if 400 <= actual < 500:
            return _DEVIATION_CLIENT_ERROR
        return _DEVIATION_OTHER

    def _compute_response_size_signal(
        self, endpoint: Endpoint, result: ExecutionResult
    ) -> float:
        """
        Map response bytes to a bounded heuristic signal in [0, 3].

        This is not a ratio and does not compare the response against a learned
        or contract-derived expected size. Undocumented statuses receive a 2x
        multiplier before clipping.

        Larger values represent increasingly anomalous responses:
        - 0: empty response
        - 0.5 to 1.5: expected range for the returned status
        - above 1.5: large response and potential data exposure
        """
        if result.response_size is None or result.response_size == 0:
            return 0.0
        size_kb = result.response_size / 1024

        # Documented statuses use the regular size scale.
        if str(result.status_code) in endpoint.responses:
            return min(size_kb, 3.0)
        # Content returned with an undocumented status is more suspicious.
        return min(size_kb * 2, 3.0)

    def assess(
        self,
        endpoint: Endpoint,
        result: ExecutionResult,
        expects_rejection: bool = False,
    ) -> FuzzyAssessment:
        deviation = self._compute_deviation(endpoint, result, expects_rejection)
        response_time = max(0.0, min(float(result.response_time_ms), 5000.0))
        response_size_signal = self._compute_response_size_signal(endpoint, result)
        inputs = {
            "status_deviation": deviation,
            "response_time_ms": response_time,
            "response_size_signal": response_size_signal,
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
            score_val = deviation
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
    ) -> tuple[float, AnomalySeverity]:
        """Return the legacy score tuple while assessment consumers migrate."""
        assessment = self.assess(endpoint, result, expects_rejection)
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
