import json
from typing import Any
from jsonschema import validate, ValidationError

from fuzzer.model.api_spec import APISpec
from fuzzer.model.endpoint import Endpoint
from fuzzer.executor.result import ExecutionResult
from fuzzer.analysis.classification import Anomaly
from fuzzer.analysis.result import AnalysisResult

class Analyzer:
    def __init__(self, spec: APISpec):
        self.spec = spec
        self.endpoint_map = {ep.id: ep for ep in spec.endpoints}

    def analyze_all(
        self,
        execution_results: list[ExecutionResult],
        execution_plan: list[tuple[Endpoint, str, Any | None, dict[str, str]]],
    ) -> list[AnalysisResult]:

        analyzed_results: list[AnalysisResult] = []
        for (endpoint, _path, payload, headers), result in zip(execution_plan, execution_results):
            analysis = self._analyze_single(endpoint, payload, headers, result)
            if analysis:
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
                # Se chegou aqui, está em conformidade.
                # Poderíamos ter um `Anomaly.CONFORMANT_SUCCESS` se quiséssemos relatar sucessos também.
                return None 
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
            # TODO: Adicionar lógica para validar o corpo do erro contra o schema de erro, similar à validação de sucesso.
        
        return None
