import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

from fuzzer.analysis.classification import AnomalySeverity
from fuzzer.executor.result import ExecutionResult
from fuzzer.model.endpoint import Endpoint


class FuzzyEngine:
    def __init__(self) -> None:
        self._build_fis()

    def _build_fis(self) -> None:
        status_deviation = ctrl.Antecedent(np.arange(0, 1.01, 0.01), "status_deviation")
        response_time = ctrl.Antecedent(np.arange(0, 5001, 1), "response_time")
        payload_ratio = ctrl.Antecedent(np.arange(0, 3.01, 0.01), "payload_ratio")
        anomaly_score = ctrl.Consequent(np.arange(0, 1.01, 0.01), "anomaly_score")

        status_deviation["low"] = fuzz.trapmf(status_deviation.universe, [0, 0, 0.2, 0.4])
        status_deviation["medium"] = fuzz.trimf(status_deviation.universe, [0.2, 0.5, 0.8])
        status_deviation["high"] = fuzz.trapmf(status_deviation.universe, [0.6, 0.8, 1, 1])

        response_time["normal"] = fuzz.trapmf(response_time.universe, [0, 0, 200, 500])
        response_time["slow"] = fuzz.trimf(response_time.universe, [200, 800, 2000])
        response_time["timeout"] = fuzz.trapmf(response_time.universe, [1000, 2500, 5000, 5000])

        payload_ratio["expected"] = fuzz.trapmf(payload_ratio.universe, [0, 0, 0.5, 1.5])
        payload_ratio["large"] = fuzz.trimf(payload_ratio.universe, [1, 2, 3])
        payload_ratio["empty"] = fuzz.trimf(payload_ratio.universe, [0, 0, 0.3])

        anomaly_score["low"] = fuzz.trapmf(anomaly_score.universe, [0, 0, 0.2, 0.4])
        anomaly_score["medium"] = fuzz.trimf(anomaly_score.universe, [0.25, 0.5, 0.75])
        anomaly_score["high"] = fuzz.trapmf(anomaly_score.universe, [0.6, 0.8, 1, 1])

        rule1 = ctrl.Rule(
            status_deviation["high"] | response_time["timeout"],
            anomaly_score["high"],
        )
        rule2 = ctrl.Rule(
            status_deviation["medium"] & response_time["slow"],
            anomaly_score["medium"],
        )
        rule3 = ctrl.Rule(
            status_deviation["low"] & response_time["normal"],
            anomaly_score["low"],
        )
        rule4 = ctrl.Rule(
            status_deviation["medium"] & response_time["normal"] & payload_ratio["large"],
            anomaly_score["medium"],
        )
        rule5 = ctrl.Rule(
            status_deviation["low"] & payload_ratio["empty"],
            anomaly_score["medium"],
        )
        rule6 = ctrl.Rule(
            status_deviation["high"],
            anomaly_score["high"],
        )
        rule7 = ctrl.Rule(
            payload_ratio["large"] & response_time["timeout"],
            anomaly_score["high"],
        )

        system = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7])
        self._sim = ctrl.ControlSystemSimulation(system)

    def _compute_deviation(self, endpoint: Endpoint, result: ExecutionResult) -> float:
        if result.status_code is None:
            return 1.0
        actual = result.status_code
        if 500 <= actual < 600:
            return 1.0
        expected = {int(s) for s in endpoint.responses if s.isdigit()}
        if actual in expected:
            return 0.0
        if not expected:
            return 0.5
        if 400 <= actual < 500:
            return 0.6
        return 0.4

    def _compute_payload_ratio(self, endpoint: Endpoint, result: ExecutionResult) -> float:
        if result.response_size is None or result.response_size == 0:
            return 0.0
        expected = {int(s) for s in endpoint.responses if s.isdigit()}
        if not expected:
            return 0.5
        ref = endpoint.responses.get(str(result.status_code))
        if ref is None:
            return 0.5
        return min(result.response_size / 1024, 3.0)

    def score(self, endpoint: Endpoint, result: ExecutionResult) -> tuple[float, AnomalySeverity]:
        deviation = self._compute_deviation(endpoint, result)
        time_ms = result.response_time_ms
        pr = self._compute_payload_ratio(endpoint, result)
        self._sim.input["status_deviation"] = deviation
        self._sim.input["response_time"] = time_ms
        self._sim.input["payload_ratio"] = pr
        try:
            self._sim.compute()
            score_val = float(self._sim.output["anomaly_score"])
        except Exception:
            score_val = deviation

        score_val = max(0.0, min(1.0, score_val))

        if score_val >= 0.66:
            severity = AnomalySeverity.HIGH
        elif score_val >= 0.33:
            severity = AnomalySeverity.MEDIUM
        else:
            severity = AnomalySeverity.LOW

        return round(score_val, 2), severity
