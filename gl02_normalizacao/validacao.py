"""A completar no GL02: duas funções sem entrada/saída ou acesso à rede.

Base conceptual: MT02, EX03. Consultar CONTRATO_GL02.md antes de alterar.
O normalizador verifica apenas quantity, unit, value e quality.
"""
from collections.abc import Mapping
from math import isfinite

from .erros import ErroValidacao

Valor = int | float | None


def normalizar_valor(valor: object) -> Valor:
    """Completar: entradas admitidas, rejeições e preservação de tipo/valor."""
    # G2a: None; exclusão de bool/tipos inválidos; finitude dos floats.
    # Não converter em float, arredondar, imprimir ou corrigir silenciosamente.
    raise NotImplementedError("G2a: implementar normalizar_valor")


def normalizar_observacao(mensagem: Mapping[str, object]) -> dict[str, object]:
    """Completar: quatro campos verificados, cópia superficial e limites."""
    # G2b: formato; campos obrigatórios; grandeza/unidade; valor; coerência.
    # Preservar todos os restantes campos, sem afirmar que foram validados.
    raise NotImplementedError("G2b: implementar normalizar_observacao")
