"""Testes à configuração sem utilizar credenciais ou acesso ao broker."""

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from observatorio.consumer.config import ConfiguracaoInvalida, carregar_configuracao


CONFIG_BASE = {
    "MQTT_HOST": "eu1.cloud.thethings.network",
    "MQTT_PORT": "8883",
    "MQTT_USERNAME": "aplicacao@ttn",
    "MQTT_PASSWORD": "api-key-de-teste",
    "MQTT_TOPIC": "v3/aplicacao@ttn/devices/+/up",
    "MQTT_CLIENT_ID": "teste-r04",
    "MQTT_KEEPALIVE": "60",
    "MQTT_OUTPUT_PATH": "data/teste.jsonl",
}


class TestCarregarConfiguracao(unittest.TestCase):
    def test_carrega_configuracao_valida(self):
        with patch.dict(os.environ, CONFIG_BASE, clear=True):
            configuracao = carregar_configuracao(env_path=Path("ficheiro-inexistente.env"))
        self.assertEqual(configuracao.host, "eu1.cloud.thethings.network")
        self.assertEqual(configuracao.port, 8883)
        self.assertEqual(configuracao.topic, "v3/aplicacao@ttn/devices/+/up")
        self.assertEqual(configuracao.output_path, Path("data/teste.jsonl"))

    def test_rejeita_credencial_em_falta(self):
        valores = dict(CONFIG_BASE)
        valores.pop("MQTT_PASSWORD")
        with patch.dict(os.environ, valores, clear=True):
            with self.assertRaisesRegex(ConfiguracaoInvalida, "MQTT_PASSWORD"):
                carregar_configuracao(env_path=Path("ficheiro-inexistente.env"))

    def test_rejeita_porta_fora_do_intervalo(self):
        valores = dict(CONFIG_BASE, MQTT_PORT="70000")
        with patch.dict(os.environ, valores, clear=True):
            with self.assertRaisesRegex(ConfiguracaoInvalida, "MQTT_PORT"):
                carregar_configuracao(env_path=Path("ficheiro-inexistente.env"))

    def test_rejeita_topico_incompativel(self):
        valores = dict(CONFIG_BASE, MQTT_TOPIC="aplicacao/devices/+/up")
        with patch.dict(os.environ, valores, clear=True):
            with self.assertRaisesRegex(ConfiguracaoInvalida, "MQTT_TOPIC"):
                carregar_configuracao(env_path=Path("ficheiro-inexistente.env"))

    def test_rejeita_host_com_protocolo(self):
        valores = dict(CONFIG_BASE, MQTT_HOST="mqtts://eu1.cloud.thethings.network")
        with patch.dict(os.environ, valores, clear=True):
            with self.assertRaisesRegex(ConfiguracaoInvalida, "MQTT_HOST"):
                carregar_configuracao(env_path=Path("ficheiro-inexistente.env"))


if __name__ == "__main__":
    unittest.main()
