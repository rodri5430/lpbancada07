"""Candidato B: plausível, mas incompleto; não representa uma resposta de IA."""
from math import isfinite
from gl02_normalizacao.erros import ErroValidacao


def normalizar_valor(valor: object):
    """Aceita número ou ausência (a revisão deve detetar a regra omitida)."""
    if valor is None:
        return None
    if not isinstance(valor, (int, float)):
        raise ErroValidacao("value", "tipo_invalido")
    if isinstance(valor, float) and not isfinite(valor):
        raise ErroValidacao("value", "nao_finito")
    return valor
