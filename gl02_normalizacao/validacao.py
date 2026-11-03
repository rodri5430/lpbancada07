"""Normalização parcial de observações para a atividade GL02.

A validação limita-se aos campos ``quantity``, ``unit``, ``value`` e
``quality``. Os restantes campos são preservados numa cópia superficial, mas
não são validados. Não há I/O, conversão de unidades, deduplicação ou acesso à
rede neste módulo.
"""
from collections.abc import Mapping
from math import isfinite

from .erros import ErroValidacao

Valor = int | float | None

def normalizar_valor(valor: object) -> Valor:
    """Valida e conserva um valor numérico ou a ausência.

    Aceita apenas ``None``, ``int`` e ``float`` nativos. Os inteiros, incluindo
    zero e negativos, mantêm o tipo; os floats têm de ser finitos e não são
    arredondados. Booleanos, texto, listas e outros tipos são rejeitados.

    Raises:
        ErroValidacao: campo ``value`` com motivo ``tipo_invalido`` ou
            ``nao_finito``. A exceção não inclui o valor recebido.
    """
    if valor is None:
        return None

    # Usamos type em vez de isinstance porque bool é uma subclasse de int
    if type(valor) is int:
        return valor

    if type(valor) is float:
        if not isfinite(valor):
            raise ErroValidacao("value", "nao_finito")
        return valor

    raise ErroValidacao("value", "tipo_invalido")


def normalizar_observacao(mensagem: Mapping[str, object]) -> dict[str, object]:
    """Valida os quatro campos do contrato e devolve uma cópia superficial.

    A sequência de validação é: formato, presença dos campos obrigatórios,
    grandeza, unidade, valor e coerência entre ``value`` e ``quality``. Os
    campos adicionais são copiados sem validação; a entrada não é alterada.

    Raises:
        ErroValidacao: primeiro campo inválido e respetivo motivo controlado.
    """
    if not isinstance(mensagem, Mapping):
        raise ErroValidacao("mensagem", "formato_invalido")

    obrigatorios = ("quantity", "unit", "value", "quality")
    for campo in obrigatorios:
        if campo not in mensagem:
            raise ErroValidacao(campo, "campo_em_falta")

    if mensagem["quantity"] != "indice_demo":
        raise ErroValidacao("quantity", "grandeza_nao_admitida")

    if mensagem["unit"] != "u_demo":
        raise ErroValidacao("unit", "unidade_nao_admitida")

    valor = normalizar_valor(mensagem["value"])
    qualidade = mensagem["quality"]

    if valor is None:
        if qualidade != "missing":
            raise ErroValidacao("quality", "incoerente")
    elif qualidade != "valid":
        raise ErroValidacao("quality", "incoerente")

    resultado = dict(mensagem)
    resultado["value"] = valor
    return resultado
