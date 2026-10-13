"""Dois testes prontos: executáveis antes de implementar as funções."""
import json
import unittest
from pathlib import Path
from gl02_normalizacao.erros import ErroValidacao

RAIZ = Path(__file__).resolve().parents[1]

class TestArranque(unittest.TestCase):
    def test_erro_controlado(self):
        erro = ErroValidacao("value", "tipo_invalido")
        self.assertEqual((erro.campo, erro.motivo), ("value", "tipo_invalido"))
        self.assertEqual(str(erro), "value: tipo_invalido")

    def test_amostra_sintetica(self):
        origem = RAIZ / "dados/mt01/ex02_observacao_valida.json"
        mensagem = json.loads(origem.read_text(encoding="utf-8"))
        self.assertEqual(mensagem["source_kind"], "synthetic")
        self.assertEqual(mensagem["value"], 0)
