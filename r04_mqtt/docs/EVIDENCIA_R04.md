# Evidência de aceitação — R04

## Identificação da demonstração

- Data/hora local da demonstração: 2026-11-17, receção entre 10:52 e 10:58 (UTC, igual à hora de Lisboa)
- Grupo/bancada: bancada 07
- Raspberry Pi utilizado: `lp-b07`
- Versão do código (branch e commit): `r04/preparacao-mqtt`, commit `336c827`
- Host MQTT (hostname, sem credenciais): `eu1.cloud.thethings.network` (TLS, porta 8883)
- Aplicação TTS: `estgoh-lp-2627-b07`
- Dispositivo (`device_id`): `estgoh-lp-2627-b07`
- `dev_eui` (se disponibilizado): `009569060001B5F2`

## Mensagem recebida (uplink de referência)

- Tópico efetivamente recebido: `v3/estgoh-lp-2627-b07@ttn/devices/estgoh-lp-2627-b07/up`
- `received_at` fornecido pelo TTS: `2026-11-17T10:52:21.957294174Z`
- `ingested_at` (consumidor): `2026-11-17T10:52:22.069576Z`
- `f_cnt`: 3
- `f_port`: 10
- `frm_payload` (Base64): `aGt0AAIJAGMHCgDthSAJchoAIQAZA70bARwAEx0AFh4AAA==`
- `decoded_payload`: `{"co2": 2409, "hcho": 0, "humidity": 60.568, "light_level": 1, "pir": 0, "pm10": 22, "pm2_5": 19, "pressure": 954, "temperature": 25.252, "tvoc": 0}`
- Gateway(s) em `rx_metadata`: estgoh-lp-2627-gw-b01, gw-b02-01, gw-b03, gtw-b04, gw-b06, gw-b07, gw-b08 (os 7 receberam o mesmo uplink)

Segundo uplink descodificado, `f_cnt` 5, `received_at` `2026-11-17T10:58:29.346468229Z`:
`{"co2": 2318, "hcho": 0.039, "humidity": 59.963, "light_level": 2, "pir": 1, "pm10": 18, "pm2_5": 18, "pressure": 954, "temperature": 25.05, "tvoc": 0}`

## Resultado do consumidor

- Ligação MQTT estabelecida: SIM
- Subscrição aceite: SIM
- Mensagem recebida: SIM
- Mensagem registada no JSONL: SIM
- `decode_status`: `decoded` (uplinks anteriores à ativação do formatter ficaram `decoded_payload_em_falta`)
- Caminho do ficheiro de registo: `r04_mqtt/docs/evidencia/uplinks_reais_completo.jsonl` (cópia de `data/mqtt_received.jsonl`)

## Relação entre origem e campos

O dispositivo é identificado por `device_id` e `dev_eui`, ambos presentes na mensagem. O `frm_payload` (34 bytes, porta 10) foi descodificado pelo Payload Formatter configurado no TTS, que produziu `decoded_payload`. O consumidor não descodifica: guarda o que o TTS publica. `received_at` é o instante fornecido pelo TTS; `ingested_at` é o instante em que o consumidor processou a mensagem (cerca de 0,11 s depois). O sensor não fornece instante de medição nestes uplinks, por isso não é registado.

## Limitações e problemas observados

- Os primeiros uplinks registados (antes de o formatter estar ativo) não têm `decoded_payload`.
- Uma medição chegou fragmentada em dois uplinks (`f_cnt` 1 com 8 bytes e `f_cnt` 2 com 26 bytes, sem o cabeçalho `686b74`). O formatter não descodifica fragmentos: `f_cnt` 1 ficou sem `decoded_payload` e `f_cnt` 2 com `{}`.
- O `f_cnt` reiniciou (valor ausente, que corresponde a 0, depois 1, 2, 3...). O TTS omite o valor 0 no JSON e o consumidor regista-o como `null`. `(device_id, f_cnt)` não é, só por si, único ao longo do tempo (relevante para R06).
- O uplink de configuração (`f_cnt` ausente) tem `temperature` = 32,0792 e `sync_interval` = 783, valores não verificados que não se usam como medições.
- Valores a 0 logo após o arranque (`hcho`, `tvoc`) podem ser aquecimento do sensor; não são tratados como válidos sem validação (R05).
- Os uplinks recebidos não contêm campo de ozono.
- Ao reiniciar o consumidor podem perder-se uplinks (QoS 0). Não foi medida a taxa de perda.
- O código do formatter instalado no TTS não está incluído neste commit.
- Compatibilidade do formatter com o sensor: formatter fornecido pelo docente e por este confirmado como adequado ao HKT IAQ-900 O3. Não foi feita comparação com um instrumento de referência.

## Estado da aceitação

- [x] Foi recebida uma observação real através de MQTT.
- [x] O dispositivo foi identificado.
- [x] A mensagem foi relacionada com os campos descodificados.
- [x] Foi conservada evidência reproduzível e sem credenciais.
