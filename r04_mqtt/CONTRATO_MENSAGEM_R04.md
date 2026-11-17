# Contrato estrutural de mensagem — R04

Este contrato descreve apenas a estrutura de transporte do evento do The Things Stack. Não define ainda as unidades, limites físicos ou regras de qualidade das grandezas do sensor; isso pertence ao contrato de domínio/normalização R05 e depende da documentação confirmada do dispositivo.

| Informação | Origem na mensagem TTS | Representação neste módulo |
|---|---|---|
| Aplicação | `end_device_ids.application_ids.application_id` | `device.application_id` |
| Dispositivo | `end_device_ids.device_id` | `device.device_id` |
| Identificador EUI | `end_device_ids.dev_eui`, quando disponível | `device.dev_eui` |
| Endereço LoRaWAN | `end_device_ids.dev_addr`, quando disponível | `device.dev_addr` |
| Tempo do TTS | `received_at`, quando disponível | `received_at` |
| Momento de ingestão | Criado pelo consumidor em UTC | `ingested_at` |
| Contador | `uplink_message.f_cnt` | `event.f_cnt` |
| Porta | `uplink_message.f_port` | `event.f_port` |
| Payload binário | `uplink_message.frm_payload` | `payload.frm_payload_base64` |
| Payload descodificado | `uplink_message.decoded_payload`, se disponível | `payload.decoded_payload` |
| Gateway/rádio | `uplink_message.rx_metadata[]` | `gateways[]` (gateway_id, eui, time, rssi, snr) |
| Proveniência | Evento recebido no tópico TTS | `source`, `topic`, `raw_event_sanitized` |

`received_at` não é renomeado como instante de medição. `ingested_at` representa o momento de processamento local. O consumidor preserva a ausência de `decoded_payload`; não inventa medições ou unidades.

O módulo regista cada entrega recebida. Não aplica deduplicação, ordenação temporal, validação física ou normalização R05. O mesmo evento pode aparecer repetido no JSONL até existir a política R06.
