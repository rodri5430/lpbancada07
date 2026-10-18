"""Seis famílias de testes do grupo para as regras GL02 G3.1-G3.6."""
import unittest
from copy import deepcopy
from pathlib import Path

from gl02_normalizacao.erros import ErroValidacao
from gl02_normalizacao.validacao import normalizar_valor, normalizar_observacao
from gl02_normalizacao.app import processar_linhas
from tests.test_contrato import mensagem

RAIZ = Path(__file__).resolve().parents[1]


class TestGrupo(unittest.TestCase):
    def test_negativos_e_tipo(self):
        """G3.1: -4 e -2.5 preservados, incluindo os tipos int e float."""
        inteiro = normalizar_valor(-4)
        decimal = normalizar_valor(-2.5)
        self.assertEqual(inteiro, -4)
        self.assertIs(type(inteiro), int)
        self.assertEqual(decimal, -2.5)
        self.assertIs(type(decimal), float)

    def test_booleanos(self):
        """G3.2: True e False rejeitados com campo e motivo corretos."""
        for valor in (True, False):
            with self.subTest(valor=valor):
                with self.assertRaises(ErroValidacao) as contexto:
                    normalizar_valor(valor)
                self.assertEqual(
                    (contexto.exception.campo, contexto.exception.motivo),
                    ("value", "tipo_invalido"),
                )

    def test_nao_finitos(self):
        """G3.3: NaN e infinitos originam value/nao_finito."""
        for valor in (float("nan"), float("inf"), -float("inf")):
            with self.subTest(valor=repr(valor)):
                with self.assertRaises(ErroValidacao) as contexto:
                    normalizar_valor(valor)
                self.assertEqual(
                    (contexto.exception.campo, contexto.exception.motivo),
                    ("value", "nao_finito"),
                )

    def test_coerencia_quality(self):
        """G3.4: None/valid e zero/missing são incoerências, sem correção."""
        casos = ((None, "valid"), (0, "missing"))
        for valor, qualidade in casos:
            with self.subTest(valor=valor, qualidade=qualidade):
                entrada = mensagem(valor, qualidade)
                with self.assertRaises(ErroValidacao) as contexto:
                    normalizar_observacao(entrada)
                self.assertEqual(
                    (contexto.exception.campo, contexto.exception.motivo),
                    ("quality", "incoerente"),
                )
                self.assertEqual(entrada["value"], valor)
                self.assertEqual(entrada["quality"], qualidade)

    def test_copia_e_preservacao(self):
        """G3.5: entrada intacta, nova saída e metadados adicionais preservados."""
        entrada = mensagem(-2.5, "valid")
        entrada["metadata_extra"] = {"origem": "teste", "marcador": 7}
        original = deepcopy(entrada)

        saida = normalizar_observacao(entrada)

        self.assertEqual(entrada, original)
        self.assertIsNot(saida, entrada)
        self.assertEqual(saida, original)
        self.assertEqual(saida["metadata_extra"], entrada["metadata_extra"])
        # A cópia é superficial: o objeto aninhado é preservado, não copiado em profundidade.
        self.assertIs(saida["metadata_extra"], entrada["metadata_extra"])

    def test_lote_e_repeticao(self):
        """G3.6: quatro aceites/seis rejeições; repetir um evento não deduplica."""
        caminho = RAIZ / "dados" / "lote_gl02.jsonl"
        with caminho.open(encoding="utf-8") as ficheiro:
            aceites, rejeicoes = processar_linhas(ficheiro)

        self.assertEqual(len(aceites), 4)
        self.assertEqual(len(rejeicoes), 6)
        self.assertEqual(aceites[0]["event_id"], "demo-001")
        self.assertEqual(aceites[-1]["event_id"], "demo-001")
        self.assertEqual(aceites[0], aceites[-1])
        self.assertEqual(aceites[-1]["value"], 0)
        self.assertIs(type(aceites[-1]["value"]), int)
