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


class FuzzyEngine:
    def __init__(self) -> None:
        self._system = self._build_system()

    def _build_system(self) -> ControlSystem:
        dev = ctrl.Antecedent(np.arange(0, 1.01, 0.01), "status_deviation")
        rtime = ctrl.Antecedent(np.arange(0, 5001, 1), "response_time")
        psize = ctrl.Antecedent(np.arange(0, 3.01, 0.01), "payload_ratio")
        ascore = ctrl.Consequent(np.arange(0, 1.01, 0.01), "anomaly_score")

        dev["low"] = fuzz.trapmf(dev.universe, [0, 0, 0.2, 0.4])
        dev["medium"] = fuzz.trimf(dev.universe, [0.2, 0.5, 0.8])
        dev["high"] = fuzz.trapmf(dev.universe, [0.6, 0.8, 1, 1])

        rtime["normal"] = fuzz.trapmf(rtime.universe, [0, 0, 200, 500])
        rtime["slow"] = fuzz.trimf(rtime.universe, [200, 800, 2000])
        rtime["timeout"] = fuzz.trapmf(rtime.universe, [1000, 2500, 5000, 5000])

        psize["expected"] = fuzz.trapmf(psize.universe, [0, 0, 0.5, 1.5])
        psize["large"] = fuzz.trimf(psize.universe, [1, 2, 3])
        psize["empty"] = fuzz.trimf(psize.universe, [0, 0, 0.3])

        ascore["low"] = fuzz.trapmf(ascore.universe, [0, 0, 0.2, 0.4])
        ascore["medium"] = fuzz.trimf(ascore.universe, [0.25, 0.5, 0.75])
        ascore["high"] = fuzz.trapmf(ascore.universe, [0.6, 0.8, 1, 1])

        rules = [
            ctrl.Rule(dev["high"] | rtime["timeout"], ascore["high"]),
            ctrl.Rule(dev["medium"] & rtime["slow"], ascore["medium"]),
            ctrl.Rule(dev["low"] & rtime["normal"] & psize["expected"], ascore["low"]),
            ctrl.Rule(dev["medium"] & rtime["normal"] & psize["large"], ascore["medium"]),
            ctrl.Rule(dev["low"] & psize["empty"], ascore["medium"]),
            ctrl.Rule(dev["high"], ascore["high"]),
            ctrl.Rule(psize["large"] & rtime["timeout"], ascore["high"]),
            ctrl.Rule(dev["low"] & psize["large"], ascore["medium"]),
            ctrl.Rule(dev["low"] & rtime["slow"], ascore["medium"]),
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

    def _compute_payload_input(self, endpoint: Endpoint, result: ExecutionResult) -> float:
        """
        Map response size in bytes to the FIS payload_ratio universe [0, 3].
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

    def score(self, endpoint: Endpoint, result: ExecutionResult) -> tuple[float, AnomalySeverity]:
        deviation = self._compute_deviation(endpoint, result)
        pr = self._compute_payload_input(endpoint, result)

        sim = ctrl.ControlSystemSimulation(self._system)
        sim.input["status_deviation"] = deviation
        sim.input["response_time"] = result.response_time_ms
        sim.input["payload_ratio"] = pr

        try:
            sim.compute()
            score_val = float(sim.output["anomaly_score"])
        except (ValueError, KeyError, TypeError):
            score_val = deviation

        score_val = max(0.0, min(1.0, score_val))

        if score_val >= _HIGH_THRESHOLD:
            severity = AnomalySeverity.HIGH
        elif score_val >= _MEDIUM_THRESHOLD:
            severity = AnomalySeverity.MEDIUM
        else:
            severity = AnomalySeverity.LOW

        return round(score_val, 2), severity
