from enum import Enum, auto

class Anomaly(Enum):
    # Categoria 1: Erros Críticos do Servidor
    SERVER_ERROR = auto()  # Resposta 5xx - Sempre um bug grave.

    # Categoria 2: Violação de Contrato em Resposta de Sucesso
    SUCCESS_CONTRADICTION = auto() # Status 2xx, mas o corpo da resposta não bate com o schema.

    # Categoria 3: Sucesso Inesperado (Falha de Segurança/Robustez)
    UNEXPECTED_SUCCESS = auto() # Enviamos um payload inválido e recebemos 2xx. Perigoso!

    # Categoria 4: Inconsistência em Respostas de Erro
    ERROR_CONTRADICTION = auto() # Status 4xx, mas o corpo do erro não bate com o schema de erro.
    UNEXPECTED_ERROR_STATUS = auto() # Um status 4xx que não estava documentado no contrato.

    # (Opcional) Categoria 5: Comportamento Esperado
    EXPECTED_FAILURE = auto() # Enviamos payload inválido, recebemos um 4xx documentado. OK.
    CONFORMANT_SUCCESS = auto() # Enviamos payload válido, recebemos 2xx em conformidade. OK.
