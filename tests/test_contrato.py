"""Seis testes fornecidos. Não alterar para esconder incumprimento das regras."""
import unittest
from gl02_normalizacao.erros import ErroValidacao
from gl02_normalizacao.validacao import normalizar_valor, normalizar_observacao


def mensagem(valor=0, qualidade="valid"):
    return {"quantity": "indice_demo", "unit": "u_demo",
            "value": valor, "quality": qualidade, "event_id": "demo-teste"}

class TestContrato(unittest.TestCase):
    def test_zero(self):
        saida = normalizar_valor(0)
        self.assertEqual(saida, 0)
        self.assertIs(type(saida), int)

    def test_ausencia(self):
        saida = normalizar_observacao(mensagem(None, "missing"))
        self.assertIsNone(saida["value"])
        self.assertEqual(saida["quality"], "missing")

    def test_texto_numerico(self):
        with self.assertRaises(ErroValidacao) as ctx:
            normalizar_valor("12")
        self.assertEqual((ctx.exception.campo, ctx.exception.motivo),
                         ("value", "tipo_invalido"))

    def test_value_em_falta(self):
        entrada = mensagem()
        del entrada["value"]
        with self.assertRaises(ErroValidacao) as ctx:
            normalizar_observacao(entrada)
        self.assertEqual((ctx.exception.campo, ctx.exception.motivo),
                         ("value", "campo_em_falta"))

    def test_unidade(self):
        entrada = mensagem()
        entrada["unit"] = "outra"
        with self.assertRaises(ErroValidacao) as ctx:
            normalizar_observacao(entrada)
        self.assertEqual((ctx.exception.campo, ctx.exception.motivo),
                         ("unit", "unidade_nao_admitida"))

    def test_formato(self):
        # Chamada deliberadamente fora da anotação, para verificar a fronteira.
        with self.assertRaises(ErroValidacao) as ctx:
            normalizar_observacao([])
        self.assertEqual((ctx.exception.campo, ctx.exception.motivo),
                         ("mensagem", "formato_invalido"))
