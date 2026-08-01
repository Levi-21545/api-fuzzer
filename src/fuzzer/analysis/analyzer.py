import json
from jsonschema import validate, ValidationError

from fuzzer.model.api_spec import APISpec
from fuzzer.executor.result import ExecutionResult
from fuzzer.analysis.classification import Anomaly
from fuzzer.analysis.fuzzy_engine import FuzzyEngine
from fuzzer.analysis.result import AnalysisResult
from fuzzer.utils.types import ExecutionPlanEntry


class Analyzer:
    def __init__(self, spec: APISpec):
        self.spec = spec
        self.endpoint_map = {ep.id: ep for ep in spec.endpoints}
        self.fuzzy_engine = FuzzyEngine()

    def analyze_all(
        self,
        execution_results: list[ExecutionResult],
        execution_plan: list[ExecutionPlanEntry],
    ) -> list[AnalysisResult]:

        analyzed_results: list[AnalysisResult] = []
        for entry, result in zip(execution_plan, execution_results):
            analysis = self._analyze_single(entry, result)
            if analysis:
                assessment = self.fuzzy_engine.assess(entry.endpoint, result)
                analysis.severity_score = assessment.score
                analysis.severity = assessment.severity
                analysis.severity_assessment = assessment.to_dict()
                analyzed_results.append(analysis)

        return analyzed_results

    def _analyze_single(
        self,
        plan_entry: ExecutionPlanEntry,
        result: ExecutionResult,
    ) -> AnalysisResult | None:
        endpoint = plan_entry.endpoint
        request_payload = plan_entry.payload
        request_headers = plan_entry.headers

        if result.status_code is None:
            return AnalysisResult(
                case_id=plan_entry.case_id,
                classification=Anomaly.UNEXPECTED_ERROR_STATUS,
                description=(
                    "Request failed before receiving a response: "
                    f"{result.error}"
                ),
                endpoint_id=endpoint.id,
                request_payload=request_payload,
                request_headers=request_headers,
                execution_result=result,
            )

        status_code_str = str(result.status_code)

        # 1. Server errors have the highest analysis priority.
        if 500 <= result.status_code < 600:
            return AnalysisResult(
                case_id=plan_entry.case_id,
                classification=Anomaly.SERVER_ERROR,
                description=f"Server returned a {result.status_code} error.",
                endpoint_id=endpoint.id,
                request_payload=request_payload,
                request_headers=request_headers,
                execution_result=result,
            )

        # Parse JSON before validating the response against the contract.
        try:
            response_body = json.loads(result.raw_response or "null")
        except json.JSONDecodeError:
            # Non-JSON content contradicts an endpoint with JSON responses.
            if any(str(s).startswith("2") for s in endpoint.responses.keys()):
                return AnalysisResult(
                    case_id=plan_entry.case_id,
                    classification=Anomaly.SUCCESS_CONTRADICTION,
                    description=(
                        f"Status {result.status_code} was returned, but the "
                        "response was not valid JSON."
                    ),
                    endpoint_id=endpoint.id,
                    request_payload=request_payload,
                    request_headers=request_headers,
                    execution_result=result,
                )
            return None

        # 2. Analyze successful responses.
        if 200 <= result.status_code < 300:
            expected_schema = endpoint.responses.get(status_code_str)
            if not expected_schema:
                return AnalysisResult(
                    case_id=plan_entry.case_id,
                    classification=Anomaly.SUCCESS_CONTRADICTION,
                    description=(
                        "API returned undocumented success status code "
                        f"{result.status_code}."
                    ),
                    endpoint_id=endpoint.id,
                    request_payload=request_payload,
                    request_headers=request_headers,
                    execution_result=result,
                )

            try:
                validate(instance=response_body, schema=expected_schema.to_jsonschema())
            except ValidationError as e:
                return AnalysisResult(
                    case_id=plan_entry.case_id,
                    classification=Anomaly.SUCCESS_CONTRADICTION,
                    description=(
                        f"Response body for {result.status_code} does not match "
                        f"the contract. Details: {e.message}"
                    ),
                    endpoint_id=endpoint.id,
                    request_payload=request_payload,
                    request_headers=request_headers,
                    execution_result=result,
                )

            if plan_entry.expects_rejection:
                return AnalysisResult(
                    case_id=plan_entry.case_id,
                    classification=Anomaly.UNEXPECTED_SUCCESS,
                    description=(
                        "Server accepted a mutated payload and returned "
                        f"{result.status_code}. "
                        f"The API should have rejected the invalid input."
                    ),
                    endpoint_id=endpoint.id,
                    request_payload=request_payload,
                    request_headers=request_headers,
                    execution_result=result,
                )

            return None

        # 3. Analyze client-error responses.
        if 400 <= result.status_code < 500:
            if status_code_str not in endpoint.responses:
                return AnalysisResult(
                    case_id=plan_entry.case_id,
                    classification=Anomaly.UNEXPECTED_ERROR_STATUS,
                    description=(
                        "API returned an undocumented error status code: "
                        f"{result.status_code}."
                    ),
                    endpoint_id=endpoint.id,
                    request_payload=request_payload,
                    request_headers=request_headers,
                    execution_result=result,
                )

            expected_schema = endpoint.responses[status_code_str]
            try:
                validate(instance=response_body, schema=expected_schema.to_jsonschema())
                return AnalysisResult(
                    case_id=plan_entry.case_id,
                    classification=Anomaly.EXPECTED_FAILURE,
                    description=(
                        "API correctly rejected with documented "
                        f"{result.status_code} error."
                    ),
                    endpoint_id=endpoint.id,
                    request_payload=request_payload,
                    request_headers=request_headers,
                    execution_result=result,
                )
            except ValidationError as e:
                return AnalysisResult(
                    case_id=plan_entry.case_id,
                    classification=Anomaly.ERROR_CONTRADICTION,
                    description=(
                        f"Error response body for {result.status_code} does not "
                        f"match contract. Details: {e.message}"
                    ),
                    endpoint_id=endpoint.id,
                    request_payload=request_payload,
                    request_headers=request_headers,
                    execution_result=result,
                )

        return None
