"""Seis tarefas de teste. Substituir cada self.fail por asserções verificáveis.

Os nomes identificam famílias de comportamento. Pode utilizar subTest ou
separar os métodos: a quantidade de testes não constitui uma classificação.
"""
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
        """G3.1: -4 e -2.5 preservados, incluindo o tipo numérico."""
        saida_int = normalizar_valor(-4)
        #confirm if its the same
        self.assertEqual(saida_int, -4)
        #confirm if its the same data type
        self.assertIs(type(saida_int), int)
        
        saida_float = normalizar_valor(-2.5)
        #confirm if its the same
        self.assertEqual(saida_float, -2.5)
        #confirm if its the same data type
        self.assertIs(type(saida_float), float)

    def test_booleanos(self):
        """G3.2: True e False rejeitados; verificar campo e motivo."""
        for val in (True, False):
            with self.assertRaises(ErroValidacao) as ctx:
                normalizar_valor(val)
            self.assertEqual(ctx.exception.campo, "value")
            self.assertEqual(ctx.exception.motivo, "tipo_invalido")
        #self.fail("G3.2: completar asserções para booleanos")

    def test_nao_finitos(self):
        """G3.3: float('nan'), float('inf') e -float('inf') rejeitados."""
        for val in (float('nan'), float('inf'), -float('inf')):
            with self.assertRaises(ErroValidacao) as ctx:
                normalizar_valor(val)
            self.assertEqual(ctx.exception.campo, "value")
            self.assertEqual(ctx.exception.motivo, "nao_finito")
        #self.fail("G3.3: completar asserções para não finitos")

    def test_coerencia_quality(self):
        """G3.4: (None, valid) e (0, missing) rejeitados, sem autocorreção."""
        obs1 = mensagem(valor=None, qualidade="valid")
        with self.assertRaises(ErroValidacao) as ctx:
            normalizar_valor(obs1)
        self.assertEqual(ctx.exception.campo, "quality")
        self.assertEqual(ctx.exception.motivo, "incoerente")

        obs2 = mensagem(valot=0, quality="missing")
        with self.assertRaises(ErroValidacao) as ctx:
            normalizar_valor(obs2)
        self.assertEqual(ctx.exception.campo, "quality")
        self.assertEqual(ctx.exception.campo, "missing")

        #self.fail("G3.4: completar asserções para quality")

    def test_copia_e_preservacao(self):
        """G3.5: entrada intacta, saída distinta, metadados preservados."""
        original = mensagem(valor=10, qualidade="valid")
        original["outro_campo"] = "dado_aleatorio"
        copia_original = deepcopy(original)

        saida = normalizar_observacao(original)

        # A entrada não pode ser mutada
        self.assertEqual(original, copia_original)
        # A saída deve ser um objeto dicionário diferente (cópia superficial)
        self.assertIsNot(saida, original)
        # Campos remanescentes/metadados devem ser preservados sem alteração
        self.assertIn("outro_campo", saida)
        self.assertEqual(saida["outro_campo"], "dado_aleatorio")
        #self.fail("G3.5: completar teste de ausência de mutação")

    def test_lote_e_repeticao(self):
        """G3.6: 4 aceites/6 rejeitadas; zero final é aceite e repetido."""
        self.fail("G3.6: completar teste do lote e da repetição")
