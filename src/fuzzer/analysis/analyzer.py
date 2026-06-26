import json
from typing import Any
from jsonschema import validate, ValidationError

from fuzzer.model.api_spec import APISpec
from fuzzer.model.endpoint import Endpoint
from fuzzer.executor.result import ExecutionResult
from fuzzer.analysis.classification import Anomaly
from fuzzer.analysis.fuzzy_engine import FuzzyEngine
from fuzzer.analysis.result import AnalysisResult
from fuzzer.generator.valid_generator import generate_valid_value
from fuzzer.types import ExecutionPlanEntry

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
        for (endpoint, _path, payload, headers), result in zip(execution_plan, execution_results):
            analysis = self._analyze_single(endpoint, payload, headers, result)
            if analysis:
                score, severity = self.fuzzy_engine.score(endpoint, result)
                analysis.severity_score = score
                analysis.severity = severity
                analyzed_results.append(analysis)

        return analyzed_results

    def _analyze_single(
        self,
        endpoint: Endpoint,
        request_payload: Any | None,
        request_headers: dict[str, str],
        result: ExecutionResult,
    ) -> AnalysisResult | None:

        if result.status_code is None:
            return AnalysisResult(
                classification=Anomaly.UNEXPECTED_ERROR_STATUS,
                description=f"Request failed before receiving a response: {result.error}",
                endpoint_id=endpoint.id,
                request_payload=request_payload,
                request_headers=request_headers,
                execution_result=result,
            )

        status_code_str = str(result.status_code)

        # 1. Prioridade Máxima: Erro de servidor (5xx)
        if 500 <= result.status_code < 600:
            return AnalysisResult(
                classification=Anomaly.SERVER_ERROR,
                description=f"Server returned a {result.status_code} error.",
                endpoint_id=endpoint.id,
                request_payload=request_payload,
                request_headers=request_headers,
                execution_result=result,
            )

        # Tenta parsear a resposta como JSON. Se falhar, é uma anomalia por si só.
        try:
            response_body = json.loads(result.raw_response or "null")
        except json.JSONDecodeError:
            # Se o contrato ESPERAVA JSON e não veio, é uma contradição.
            if any(str(s).startswith("2") for s in endpoint.responses.keys()):
                return AnalysisResult(
                    classification=Anomaly.SUCCESS_CONTRADICTION,
                    description=(
                        f"Status {result.status_code} was returned, but the response was not valid JSON."
                    ),
                    endpoint_id=endpoint.id,
                    request_payload=request_payload,
                    request_headers=request_headers,
                    execution_result=result,
                )
            return None

        # 2. Análise de Respostas de Sucesso (2xx)
        if 200 <= result.status_code < 300:
            expected_schema = endpoint.responses.get(status_code_str)
            if not expected_schema:
                return AnalysisResult(
                    classification=Anomaly.SUCCESS_CONTRADICTION,
                    description=(
                        f"API returned undocumented success status code {result.status_code}."
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
                    classification=Anomaly.SUCCESS_CONTRADICTION,
                    description=(
                        f"Response body for {result.status_code} does not match the contract. Details: {e.message}"
                    ),
                    endpoint_id=endpoint.id,
                    request_payload=request_payload,
                    request_headers=request_headers,
                    execution_result=result,
                )

            baseline = (
                generate_valid_value(endpoint.request_body.schema)
                if endpoint.request_body and endpoint.request_body.schema
                else None
            )
            if baseline is not None and request_payload != baseline:
                return AnalysisResult(
                    classification=Anomaly.UNEXPECTED_SUCCESS,
                    description=(
                        f"Server accepted a mutated payload and returned {result.status_code}. "
                        f"The API should have rejected the invalid input."
                    ),
                    endpoint_id=endpoint.id,
                    request_payload=request_payload,
                    request_headers=request_headers,
                    execution_result=result,
                )

            return None

        # 3. Análise de Respostas de Erro do Cliente (4xx)
        if 400 <= result.status_code < 500:
            if status_code_str not in endpoint.responses:
                return AnalysisResult(
                    classification=Anomaly.UNEXPECTED_ERROR_STATUS,
                    description=f"API returned an undocumented error status code: {result.status_code}.",
                    endpoint_id=endpoint.id,
                    request_payload=request_payload,
                    request_headers=request_headers,
                    execution_result=result,
                )

            expected_schema = endpoint.responses[status_code_str]
            try:
                validate(instance=response_body, schema=expected_schema.to_jsonschema())
                return AnalysisResult(
                    classification=Anomaly.EXPECTED_FAILURE,
                    description=f"API correctly rejected with documented {result.status_code} error.",
                    endpoint_id=endpoint.id,
                    request_payload=request_payload,
                    request_headers=request_headers,
                    execution_result=result,
                )
            except ValidationError as e:
                return AnalysisResult(
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
