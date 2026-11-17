"""Consumidor MQTT do The Things Stack; executar como processo independente."""

import logging
import ssl

import paho.mqtt.client as mqtt

from .config import ConfiguracaoInvalida, carregar_configuracao
from .event import UplinkInvalido, interpretar_uplink, resumo_payload
from .storage import guardar_jsonl


LOGGER = logging.getLogger("observatorio.consumer.mqtt")


def executar() -> None:
    configuracao = carregar_configuracao()
    cliente = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        client_id=configuracao.client_id,
        protocol=mqtt.MQTTv311,
    )
    cliente.username_pw_set(configuracao.username, configuracao.password)
    cliente.tls_set_context(ssl.create_default_context())
    cliente.tls_insecure_set(False)

    def ao_ligar(client, userdata, flags, reason_code, properties) -> None:
        if reason_code.is_failure:
            LOGGER.error("Ligação MQTT recusada: %s", reason_code)
            return

        resultado, _ = client.subscribe(configuracao.topic, qos=0)
        if resultado != mqtt.MQTT_ERR_SUCCESS:
            LOGGER.error("Falha ao subscrever tópico (código %s)", resultado)
            return
        LOGGER.info("Ligação estabelecida; subscrição ativa em %s", configuracao.topic)

    def ao_receber(client, userdata, mensagem) -> None:
        try:
            registo = interpretar_uplink(mensagem.topic, mensagem.payload)
            guardar_jsonl(configuracao.output_path, registo)
        except (UplinkInvalido, OSError, TypeError, ValueError) as erro:
            # Não imprimir o conteúdo da mensagem nem credenciais.
            LOGGER.warning("Mensagem não registada (%s); tópico=%s", erro, mensagem.topic)
            return

        device_id = registo["device"]["device_id"]
        f_cnt = registo["event"]["f_cnt"]
        decode_status = registo["payload"]["decode_status"]
        campos = resumo_payload(registo["payload"])
        LOGGER.info(
            "Uplink registado: dispositivo=%s f_cnt=%s descodificacao=%s campos=%s",
            device_id,
            f_cnt,
            decode_status,
            campos,
        )
        if decode_status != "decoded":
            LOGGER.warning(
                "Uplink recebido sem decoded_payload. Verificar o Payload Formatter no TTS."
            )

    def ao_desligar(client, userdata, disconnect_flags, reason_code, properties) -> None:
        if reason_code.is_failure:
            LOGGER.warning("Ligação MQTT interrompida: %s", reason_code)
        else:
            LOGGER.info("Cliente MQTT desligado")

    cliente.on_connect = ao_ligar
    cliente.on_message = ao_receber
    cliente.on_disconnect = ao_desligar

    LOGGER.info(
        "A iniciar consumidor MQTT em %s:%s; destino=%s",
        configuracao.host,
        configuracao.port,
        configuracao.output_path,
    )
    cliente.connect(configuracao.host, configuracao.port, configuracao.keepalive)
    # loop_forever mantém o processamento e trata reconexões após a ligação inicial.
    cliente.loop_forever()


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    try:
        executar()
    except (ConfiguracaoInvalida, OSError, ValueError) as erro:
        LOGGER.error("Não foi possível iniciar o consumidor: %s", erro)
        return 1
    except KeyboardInterrupt:
        LOGGER.info("Execução interrompida pelo utilizador")
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
