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
        self.fail("G3.1: completar asserções para negativos e tipos")

    def test_booleanos(self):
        """G3.2: True e False rejeitados; verificar campo e motivo."""
        self.fail("G3.2: completar asserções para booleanos")

    def test_nao_finitos(self):
        """G3.3: float('nan'), float('inf') e -float('inf') rejeitados."""
        self.fail("G3.3: completar asserções para não finitos")

    def test_coerencia_quality(self):
        """G3.4: (None, valid) e (0, missing) rejeitados, sem autocorreção."""
        self.fail("G3.4: completar asserções para quality")

    def test_copia_e_preservacao(self):
        """G3.5: entrada intacta, saída distinta, metadados preservados."""
        self.fail("G3.5: completar teste de ausência de mutação")

    def test_lote_e_repeticao(self):
        """G3.6: 4 aceites/6 rejeitadas; zero final é aceite e repetido."""
        self.fail("G3.6: completar teste do lote e da repetição")
