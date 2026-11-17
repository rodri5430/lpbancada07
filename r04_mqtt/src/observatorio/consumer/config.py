"""Leitura e validação das configurações do consumidor MQTT."""

from dataclasses import dataclass
import os
from pathlib import Path

from dotenv import load_dotenv


class ConfiguracaoInvalida(ValueError):
    """Configuração obrigatória ausente ou com formato inválido."""


@dataclass(frozen=True)
class MQTTSettings:
    host: str
    port: int
    username: str
    password: str
    topic: str
    client_id: str
    keepalive: int
    output_path: Path


def _obrigatoria(nome: str) -> str:
    valor = os.getenv(nome, "").strip()
    if not valor:
        raise ConfiguracaoInvalida(f"Variável obrigatória não definida: {nome}")
    return valor


def _inteiro(nome: str, valor_por_omissao: str, minimo: int, maximo: int) -> int:
    valor = os.getenv(nome, valor_por_omissao).strip()
    try:
        numero = int(valor)
    except ValueError as erro:
        raise ConfiguracaoInvalida(f"{nome} tem de ser um número inteiro") from erro
    if not minimo <= numero <= maximo:
        raise ConfiguracaoInvalida(
            f"{nome} tem de estar entre {minimo} e {maximo}"
        )
    return numero


def carregar_configuracao(env_path: str | Path | None = None) -> MQTTSettings:
    """Carrega `.env` e valida os valores necessários à ligação.

    As credenciais são obtidas do ambiente; nunca são incluídas nos registos.
    O cliente utiliza TLS com validação do certificado do servidor.
    """
    load_dotenv(dotenv_path=env_path, override=False)

    host = _obrigatoria("MQTT_HOST")
    if "://" in host or "/" in host:
        raise ConfiguracaoInvalida(
            "MQTT_HOST deve conter apenas o hostname, sem protocolo ou caminho"
        )

    topic = _obrigatoria("MQTT_TOPIC")
    if any(character.isspace() for character in topic):
        raise ConfiguracaoInvalida("MQTT_TOPIC não pode conter espaços")
    if not topic.startswith("v3/") or not topic.endswith("/devices/+/up"):
        raise ConfiguracaoInvalida(
            "MQTT_TOPIC deve seguir o formato v3/<aplicacao>/devices/+/up"
        )

    output = os.getenv("MQTT_OUTPUT_PATH", "data/mqtt_received.jsonl").strip()
    if not output:
        output = "data/mqtt_received.jsonl"

    return MQTTSettings(
        host=host,
        port=_inteiro("MQTT_PORT", "8883", 1, 65535),
        username=_obrigatoria("MQTT_USERNAME"),
        password=_obrigatoria("MQTT_PASSWORD"),
        topic=topic,
        client_id=_obrigatoria("MQTT_CLIENT_ID"),
        keepalive=_inteiro("MQTT_KEEPALIVE", "60", 1, 65535),
        output_path=Path(output),
    )
