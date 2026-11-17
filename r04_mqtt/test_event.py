"""Testes unitários sintéticos; não ligam ao TTS nem ao sensor físico."""

import json
import tempfile
import unittest
from pathlib import Path

from observatorio.consumer.event import UplinkInvalido, interpretar_uplink
from observatorio.consumer.storage import guardar_jsonl


TOPIC = "v3/aplicacao-exemplo-nao-real@ttn/devices/sensor-exemplo-nao-real/up"


def uplink_sintetico(com_decoded_payload: bool = True) -> dict:
    uplink = {
        "f_cnt": 17,
        "f_port": 10,
        "frm_payload": "AQIDBA==",
        "rx_metadata": [
            {
                "gateway_ids": {"gateway_id": "gateway-exemplo", "eui": "0102030405060708"},
                "time": "2026-11-17T10:00:00Z",
                "rssi": -81,
                "snr": 7.5,
                "uplink_token": "token-sintetico",
            }
        ],
    }
    if com_decoded_payload:
        uplink["decoded_payload"] = {"campo_de_teste": 12.5}
    return {
        "end_device_ids": {
            "device_id": "sensor-exemplo-nao-real",
            "application_ids": {"application_id": "aplicacao-exemplo-nao-real"},
            "dev_eui": "0011223344556677",
            "dev_addr": "26000001",
        },
        "received_at": "2026-11-17T10:00:01Z",
        "correlation_ids": ["gs:uplink:fixture-sintetica"],
        "uplink_message": uplink,
    }


class TestInterpretarUplink(unittest.TestCase):
    def test_extrai_dispositivo_evento_e_payload(self):
        mensagem = json.dumps(uplink_sintetico()).encode("utf-8")
        registo = interpretar_uplink(TOPIC, mensagem, ingested_at="2026-11-17T10:00:02Z")

        self.assertEqual(registo["device"]["device_id"], "sensor-exemplo-nao-real")
        self.assertEqual(registo["device"]["dev_eui"], "0011223344556677")
        self.assertEqual(registo["event"]["f_cnt"], 17)
        self.assertEqual(registo["payload"]["decoded_payload"], {"campo_de_teste": 12.5})
        self.assertEqual(registo["payload"]["decode_status"], "decoded")
        self.assertEqual(registo["received_at"], "2026-11-17T10:00:01Z")
        self.assertEqual(registo["ingested_at"], "2026-11-17T10:00:02Z")

    def test_nao_inventa_received_at(self):
        evento = uplink_sintetico()
        del evento["received_at"]
        registo = interpretar_uplink(TOPIC, json.dumps(evento).encode())
        self.assertIsNone(registo["received_at"])

    def test_regista_payload_descodificado_em_falta(self):
        evento = uplink_sintetico(com_decoded_payload=False)
        registo = interpretar_uplink(TOPIC, json.dumps(evento).encode())
        self.assertIsNone(registo["payload"]["decoded_payload"])
        self.assertEqual(registo["payload"]["decode_status"], "decoded_payload_em_falta")
        self.assertEqual(registo["payload"]["frm_payload_base64"], "AQIDBA==")

    def test_rejeita_json_invalido(self):
        with self.assertRaisesRegex(UplinkInvalido, "json_invalido"):
            interpretar_uplink(TOPIC, b"{nao-json")

    def test_rejeita_device_id_ausente(self):
        evento = uplink_sintetico()
        del evento["end_device_ids"]["device_id"]
        with self.assertRaisesRegex(UplinkInvalido, "device_id_em_falta"):
            interpretar_uplink(TOPIC, json.dumps(evento).encode())

    def test_rejeita_device_id_incoerente_com_topico(self):
        evento = uplink_sintetico()
        topic = "v3/aplicacao-exemplo-nao-real@ttn/devices/outro-dispositivo/up"
        with self.assertRaisesRegex(UplinkInvalido, "device_id_incoerente_com_topico"):
            interpretar_uplink(topic, json.dumps(evento).encode())

    def test_rejeita_application_id_incoerente_com_topico(self):
        evento = uplink_sintetico()
        topic = "v3/outra-aplicacao@ttn/devices/sensor-exemplo-nao-real/up"
        with self.assertRaisesRegex(UplinkInvalido, "application_id_incoerente_com_topico"):
            interpretar_uplink(topic, json.dumps(evento).encode())

    def test_nao_regista_token_de_gateway(self):
        registo = interpretar_uplink(TOPIC, json.dumps(uplink_sintetico()).encode())
        serializado = json.dumps(registo)
        self.assertNotIn("token-sintetico", serializado)
        self.assertNotIn("uplink_token", serializado)

    def test_rejeita_decoded_payload_com_formato_incorreto(self):
        evento = uplink_sintetico()
        evento["uplink_message"]["decoded_payload"] = ["nao", "e", "objeto"]
        with self.assertRaisesRegex(UplinkInvalido, "decoded_payload_nao_e_objeto"):
            interpretar_uplink(TOPIC, json.dumps(evento).encode())

    def test_persiste_registo_em_jsonl(self):
        registo = interpretar_uplink(TOPIC, json.dumps(uplink_sintetico()).encode())
        with tempfile.TemporaryDirectory() as pasta:
            destino = Path(pasta) / "dados" / "uplinks.jsonl"
            guardar_jsonl(destino, registo)
            linhas = destino.read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(linhas), 1)
            self.assertEqual(json.loads(linhas[0])["device"]["device_id"], "sensor-exemplo-nao-real")


if __name__ == "__main__":
    unittest.main()
