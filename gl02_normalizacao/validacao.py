"""A completar no GL02: duas funções sem entrada/saída ou acesso à rede.

Base conceptual: MT02, EX03. Consultar CONTRATO_GL02.md antes de alterar.
O normalizador verifica apenas quantity, unit, value e quality.
"""
from collections.abc import Mapping
import math
from math import isfinite
from math import isnan

from .erros import ErroValidacao

Valor = int | float | None


def normalizar_valor(valor: object) -> Valor:
    #TODO: """Completar: entradas admitidas, rejeições e preservação de tipo/valor."""
    if valor is None:
        return None
    
    #G2a: exclusao de bool/tipos invalidos
    #command isinstance from https://www.geeksforgeeks.org/python/python-isinstance-method/
    if isinstance(valor, bool):
        raise ErroValidacao("value", "tipo_invalido")

    if isinstance(valor, float):
        #check if value is infinit, if it is dont concerve it
        #ass: Flower
        if not isfinite(valor):
            raise ErroValidacao("value" ,"nao_finito")
        #took from https://stackoverflow.com/questions/944700/how-to-check-for-nan-values
        #and https://docs.python.org/3/library/math.html#math.isnan
        #ass: Flower
        if math.isnan(valor):
            raise ErroValidacao("value", "tipo_invalido")
        #value assumed as valid ass: Flower
        return valor

    if isinstance(valor, int):
        #Int values are allowed so pass that
        #Plus booleans are a subclass of int so this check must be bellow boolean or else it will pass
        #The above can be obsserved on one of the examples of the geeksforgeeks page i gave on the bool check
        #ass: Flower
        return valor;
    
    # Não converter em float, arredondar, imprimir ou corrigir silenciosamente.
    #Yes Sir I wont do any of that :3 ass: Flower
    
    #IDK HOW THE FUCK IT WOULD REACH HERE BUT IT SURE IT AINT VALID IF IT DID
    raise ErroValidacao("value" ,"tipo_invalido")

    #I mean I dont know if this raise is necessary or was just a thing left here for implementation purposses.... ._. ass: Flower


def normalizar_observacao(mensagem: Mapping[str, object]) -> dict[str, object]:
    #TODO: """Completar: quatro campos verificados, cópia superficial e limites."""
    #its given a dictionary ig and it will have four parameters AS A MAPPING
    # - quantity
    # - unit
    # - value
    # - quality

    if not isinstance(mensagem, Mapping):
        #I mean ig this is checked when the func is called but anyway, just delete this if I'm wrong ._.
        raise ErroValidacao("mensagem", "formato_invalido")

    resultado = dict(mensagem)

    # G2b: formato; campos obrigatórios; grandeza/unidade; valor; coerência.
    campos_obrigatorios = {"quantity", "unit", "value", "quality"}
    for campo in campos_obrigatorios:
        #verify each section of resultado to cheack if its respective campo is there
        if campo not in resultado:
            #Erm this wont show the entered value so to not break S8 rule
            raise ErroValidacao(campo, "campo_em_falta")
    
    #verify if section "value" is valid, obey S1 S2 and S3 (Dont know if its applicable here too but fuck it Im too tired to think about this rn it 2am, just remove it if not)
    resultado["value"] = normalizar_valor(resultado["value"])

    #S5 
    #quantity="indice_demo" e unit="u_demo" exclusivamente neste exemplo sintetico ?????? FUCK DOES THAT MEAN ???????
    #https://pt.pinterest.com/pin/1041598220082430653/  <-  literally me rn
    if resultado["quantity"] != "indice_demo":
        raise ErroValidacao("quantity", "grandeza_nao_admitida")

    if resultado["unit"] != "u_demo":
        raise ErroValidacao("unit" ,"unidade_nao_admitida")

    #S6
    #quality="missing" apenas para None
    #"Valid" apenas para numeros aceites
    #Rejeitar restantes incoerencias

    if resultado["value"] is None:
        if resultado["quality"] != "missing":
            raise ErroValidacao("quality", "incoerente")
    else:
        if resultado["quality"] != "valid":
            raise ErroValidacao("quality", "incoerente")
    
    #S7
    #devolver uma copia superficial aka resultado sem alterar a entrada
    return resultado
    
    # Preservar todos os restantes campos, sem afirmar que foram validados.
    raise NotImplementedError("G2b: implementar normalizar_observacao")
