"""Leitor local fornecido, adaptado de MT02/EX04; não é um consumidor MQTT.

Só para ficheiros sintéticos pequenos. Guarda resultados em memória,
ignora linhas vazias e não elimina repetições. Não imprime os payloads.
"""
import argparse
import json
import sys
from collections.abc import Iterable
from pathlib import Path

from .erros import ErroValidacao
from .validacao import normalizar_observacao


def processar_linhas(linhas: Iterable[str]) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    """Aplica o normalizador; conserva números de linha físicos para rejeições.

    JSON malformado e ErroValidacao são rejeições esperadas. Outros erros,
    incluindo NotImplementedError, permanecem visíveis. Não há sanitização
    dos campos adicionais: usar apenas as amostras sintéticas autorizadas.
    """
    aceites: list[dict[str, object]] = []
    rejeicoes: list[dict[str, object]] = []
    for numero, linha in enumerate(linhas, 1):
        if not linha.strip():
            continue
        try:
            observacao = normalizar_observacao(json.loads(linha))
        except json.JSONDecodeError:
            rejeicoes.append({"linha": numero, "motivo": "json_invalido"})
        except ErroValidacao as erro:
            rejeicoes.append({"linha": numero, "campo": erro.campo,
                              "motivo": erro.motivo})
        else:
            aceites.append(observacao)
    return aceites, rejeicoes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ficheiro", type=Path)
    args = parser.parse_args()
    try:
        with args.ficheiro.open(encoding="utf-8") as origem:
            aceites, rejeicoes = processar_linhas(origem)
    except (OSError, UnicodeError) as erro:
        print(f"Leitura interrompida ({type(erro).__name__}).", file=sys.stderr)
        return 2
    print(json.dumps({"aceites": len(aceites), "rejeitadas": len(rejeicoes),
                      "motivos": rejeicoes}, ensure_ascii=False, allow_nan=False))
    # 0 = lote processado; não significa que todas as linhas foram aceites.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
