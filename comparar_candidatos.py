"""G4: executa dez casos fixos; não mede produtividade nem qualidade de IA.

Os resultados esperados são independentes das implementações. Os dois
candidatos são exemplos didáticos conhecidos, sem chamadas externas.
"""
import json
from candidatos import a, b
from gl02_normalizacao.erros import ErroValidacao

CASOS = [
    ("zero_int", 0, 0, None),
    ("negativo", -2.5, -2.5, None),
    ("ausencia", None, None, None),
    ("texto_numerico", "12", None, "tipo_invalido"),
    ("texto", "erro", None, "tipo_invalido"),
    ("booleano_false", False, None, "tipo_invalido"),
    ("booleano_true", True, None, "tipo_invalido"),
    ("lista", [], None, "tipo_invalido"),
    ("infinito", float("inf"), None, "nao_finito"),
    ("nan", float("nan"), None, "nao_finito"),
]


def avaliar(funcao):
    resultados = []
    for nome, entrada, esperado, erro_esperado in CASOS:
        try:
            obtido = funcao(entrada)
        except ErroValidacao as erro:
            cumpre = (erro_esperado is not None and erro.campo == "value"
                      and erro.motivo == erro_esperado)
            observacao = f"ErroValidacao:{erro.campo}:{erro.motivo}"
        except Exception as erro:
            # Neste comparador isolado, relatar a divergência e seguir nos casos;
            # não é a política de tratamento do normalizador ou da aplicação.
            cumpre = False
            observacao = type(erro).__name__
        else:
            cumpre = (erro_esperado is None and type(obtido) is type(esperado)
                      and obtido == esperado)
            observacao = f"{type(obtido).__name__}:{obtido!r}"
        resultados.append({"caso": nome, "cumpre": cumpre, "observado": observacao})
    return resultados


def main():
    for nome, funcao in (("A", a.normalizar_valor), ("B", b.normalizar_valor)):
        resultados = avaliar(funcao)
        print(json.dumps({"candidato": nome,
                          "conformes": sum(r["cumpre"] for r in resultados),
                          "total": len(resultados), "resultados": resultados},
                         ensure_ascii=False))
    return 0  # Conclusão da comparação, não aprovação dos candidatos.


if __name__ == "__main__":
    raise SystemExit(main())
