"""Interpretação estrutural de uplinks JSON publicados pelo The Things Stack.

Este módulo não descodifica o payload binário do sensor e não valida grandezas
ou unidades (R05). Usa o `decoded_payload` gerado pelo Payload Formatter do
The Things Stack, quando esse campo está disponível.
"""

from collections.abc import Mapping
from datetime import datetime, timezone
import json
from typing import Any


class UplinkInvalido(ValueError):
    """Mensagem recebida que não corresponde à estrutura mínima de um uplink."""


_CAMPOS_SENSIVEIS = {
    "api_key",
    "access_key",
    "authorization",
    "password",
    "session_key",
    "session_key_id",
    "uplink_token",
}


def _agora_utc() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _rejeitar_constante_json(valor: str) -> None:
    raise ValueError(f"Constante JSON não permitida: {valor}")


def _remover_campos_sensiveis(valor: Any) -> Any:
    """Copia estruturas sem campos conhecidos como credenciais/tokens."""
    if isinstance(valor, Mapping):
        return {
            str(chave): _remover_campos_sensiveis(conteudo)
            for chave, conteudo in valor.items()
            if str(chave).lower() not in _CAMPOS_SENSIVEIS
        }
    if isinstance(valor, list):
        return [_remover_campos_sensiveis(elemento) for elemento in valor]
    return valor


def _validar_topico_e_identificadores(
    topic: str,
    application_id: str,
    device_id: str,
) -> None:
    """Confirma que o tópico é um uplink da aplicação/dispositivo do JSON."""
    partes = topic.split("/")
    if (
        len(partes) != 5
        or partes[0] != "v3"
        or partes[2] != "devices"
        or partes[4] != "up"
    ):
        raise UplinkInvalido("topico_uplink_invalido")

    # O segmento do tópico pode conter `application_id@tenant_id`.
    application_no_topico = partes[1].split("@", maxsplit=1)[0]
    if application_no_topico != application_id:
        raise UplinkInvalido("application_id_incoerente_com_topico")
    if partes[3] != device_id:
        raise UplinkInvalido("device_id_incoerente_com_topico")


def interpretar_uplink(
    topic: str,
    payload: bytes,
    *,
    ingested_at: str | None = None,
) -> dict[str, Any]:
    """Valida a estrutura do uplink e prepara um registo JSON serializável.

    `received_at` só é preenchido com o valor enviado pelo TTS. `ingested_at`
    indica quando o consumidor recebeu/processou a mensagem; não é apresentado
    como instante de medição.
    """
    try:
        mensagem = json.loads(
            payload.decode("utf-8"),
            parse_constant=_rejeitar_constante_json,
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as erro:
        raise UplinkInvalido("json_invalido") from erro

    if not isinstance(mensagem, dict):
        raise UplinkInvalido("raiz_json_invalida")

    ids = mensagem.get("end_device_ids")
    uplink = mensagem.get("uplink_message")
    if not isinstance(ids, dict) or not isinstance(uplink, dict):
        raise UplinkInvalido("estrutura_uplink_em_falta")

    device_id = ids.get("device_id")
    application_ids = ids.get("application_ids")
    if not isinstance(device_id, str) or not device_id.strip():
        raise UplinkInvalido("device_id_em_falta")
    if not isinstance(application_ids, dict):
        raise UplinkInvalido("application_ids_em_falta")

    application_id = application_ids.get("application_id")
    if not isinstance(application_id, str) or not application_id.strip():
        raise UplinkInvalido("application_id_em_falta")

    _validar_topico_e_identificadores(topic, application_id, device_id)

    decoded_payload = uplink.get("decoded_payload")
    if decoded_payload is not None and not isinstance(decoded_payload, dict):
        raise UplinkInvalido("decoded_payload_nao_e_objeto")

    rx_metadata = uplink.get("rx_metadata", [])
    gateways: list[dict[str, Any]] = []
    if isinstance(rx_metadata, list):
        for item in rx_metadata:
            if not isinstance(item, dict):
                continue
            gateway_ids = item.get("gateway_ids")
            if not isinstance(gateway_ids, dict):
                gateway_ids = {}
            gateways.append(
                {
                    "gateway_id": gateway_ids.get("gateway_id"),
                    "eui": gateway_ids.get("eui"),
                    "time": item.get("time"),
                    "rssi": item.get("rssi"),
                    "snr": item.get("snr"),
                }
            )

    correlation_ids = mensagem.get("correlation_ids", [])
    if not isinstance(correlation_ids, list):
        correlation_ids = []

    return {
        "source": "the_things_stack_mqtt",
        "topic": topic,
        "received_at": mensagem.get("received_at"),
        "ingested_at": ingested_at or _agora_utc(),
        "device": {
            "application_id": application_id,
            "device_id": device_id,
            "dev_eui": ids.get("dev_eui"),
            "dev_addr": ids.get("dev_addr"),
        },
        "event": {
            "f_cnt": uplink.get("f_cnt"),
            "f_port": uplink.get("f_port"),
            "correlation_ids": correlation_ids,
        },
        "payload": {
            "decoded_payload": decoded_payload,
            "frm_payload_base64": uplink.get("frm_payload"),
            "decode_status": (
                "decoded" if decoded_payload is not None else "decoded_payload_em_falta"
            ),
        },
        "gateways": gateways,
        "raw_event_sanitized": _remover_campos_sensiveis(mensagem),
    }


def resumo_payload(payload: Mapping[str, Any]) -> str:
    """Devolve nomes de campos descodificados, sem apresentar valores."""
    decoded = payload.get("decoded_payload")
    if isinstance(decoded, dict):
        return ", ".join(sorted(str(chave) for chave in decoded)) or "(objeto vazio)"
    return "não disponível"
