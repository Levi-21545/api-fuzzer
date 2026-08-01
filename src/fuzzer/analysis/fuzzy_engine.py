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

_HIGH_THRESHOLD = 0.66
_MEDIUM_THRESHOLD = 0.33
FUZZY_MODEL_ID = "mamdani-status-time-response-size-v1"

_RULE_DESCRIPTIONS = {
    "R1_HIGH_DEVIATION_OR_TIMEOUT": (
        "high status deviation or timeout response -> high severity"
    ),
    "R2_MEDIUM_DEVIATION_AND_SLOW": (
        "medium status deviation and slow response -> medium severity"
    ),
    "R3_LOW_DEVIATION_NORMAL_EXPECTED_SIZE": (
        "low status deviation, normal response time, and expected response "
        "size -> low severity"
    ),
    "R4_MEDIUM_DEVIATION_NORMAL_LARGE_RESPONSE": (
        "medium status deviation, normal response time, and large response -> "
        "medium severity"
    ),
    "R5_LOW_DEVIATION_EMPTY_RESPONSE": (
        "low status deviation and empty response -> medium severity"
    ),
    "R6_HIGH_DEVIATION": "high status deviation -> high severity",
    "R7_LARGE_RESPONSE_AND_TIMEOUT": ("large response and timeout -> high severity"),
    "R8_LOW_DEVIATION_LARGE_RESPONSE": (
        "low status deviation and large response -> medium severity"
    ),
    "R9_LOW_DEVIATION_SLOW_RESPONSE": (
        "low status deviation and slow response -> medium severity"
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
                dev["medium"] & rtime["slow"],
                ascore["medium"],
                label="R2_MEDIUM_DEVIATION_AND_SLOW",
            ),
            ctrl.Rule(
                dev["low"] & rtime["normal"] & rsize["expected"],
                ascore["low"],
                label="R3_LOW_DEVIATION_NORMAL_EXPECTED_SIZE",
            ),
            ctrl.Rule(
                dev["medium"] & rtime["normal"] & rsize["large"],
                ascore["medium"],
                label="R4_MEDIUM_DEVIATION_NORMAL_LARGE_RESPONSE",
            ),
            ctrl.Rule(
                dev["low"] & rsize["empty"],
                ascore["medium"],
                label="R5_LOW_DEVIATION_EMPTY_RESPONSE",
            ),
            ctrl.Rule(
                dev["high"],
                ascore["high"],
                label="R6_HIGH_DEVIATION",
            ),
            ctrl.Rule(
                rsize["large"] & rtime["timeout"],
                ascore["high"],
                label="R7_LARGE_RESPONSE_AND_TIMEOUT",
            ),
            ctrl.Rule(
                dev["low"] & rsize["large"],
                ascore["medium"],
                label="R8_LOW_DEVIATION_LARGE_RESPONSE",
            ),
            ctrl.Rule(
                dev["low"] & rtime["slow"],
                ascore["medium"],
                label="R9_LOW_DEVIATION_SLOW_RESPONSE",
            ),
        ]

        return ctrl.ControlSystem(rules)

    def _compute_deviation(self, endpoint: Endpoint, result: ExecutionResult) -> float:
        if result.status_code is None:
            return _DEVIATION_NO_STATUS
        actual = result.status_code
        if 500 <= actual < 600:
            return _DEVIATION_SERVER_ERROR
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

    def assess(self, endpoint: Endpoint, result: ExecutionResult) -> FuzzyAssessment:
        deviation = self._compute_deviation(endpoint, result)
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
        self, endpoint: Endpoint, result: ExecutionResult
    ) -> tuple[float, AnomalySeverity]:
        """Return the legacy score tuple while assessment consumers migrate."""
        assessment = self.assess(endpoint, result)
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
