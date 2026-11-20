# R04 — Consumidor MQTT do The Things Stack

> **Estado:** receção real demonstrada na bancada 07 (Raspberry Pi `lp-b07`, 2026-11-17), com uplinks recebidos por MQTT e `decoded_payload` produzido pelo formatter do TTS. Ver `docs/EVIDENCIA_R04.md`. Os testes automáticos incluídos continuam a ser sintéticos.

Este módulo implementa o requisito R04 do MP01. Recebe eventos JSON publicados pelo The Things Stack (TTS) através de MQTT, identifica a aplicação/dispositivo, preserva `received_at`, `f_cnt`, `f_port`, `frm_payload` e `decoded_payload` quando disponíveis e acrescenta um registo por mensagem a um ficheiro JSONL.

## Relação com o resto do repositório

Este módulo vive em `r04_mqtt/`, separado de `gl02_normalizacao/` (normalização GL02, sem rede). Ainda não está ligado ao normalizador: o consumidor só recebe e regista. Se a estrutura do projeto passar a ter `src/` na raiz, `r04_mqtt/src/observatorio/consumer/` pode ser movido para lá sem alterações de código.

## O que o módulo faz

- Usa MQTT 3.1.1 com TLS, normalmente na porta 8883.
- Usa as credenciais apresentadas em **The Things Stack > Integrations > MQTT**.
- Subscreve o tópico de uplinks configurado em `MQTT_TOPIC`, normalmente `v3/{application_id}@{tenant_id}/devices/+/up` em instalações multi-tenant.
- Valida a coerência entre o tópico recebido e `application_id` / `device_id` no JSON.
- Preserva os campos descodificados pelo TTS em `uplink_message.decoded_payload` sem voltar a descodificar o payload binário.
- Preserva `frm_payload` em Base64 para rastreabilidade.
- Regista `received_at` apenas quando fornecido pelo TTS e cria `ingested_at` para o instante de receção/processamento pelo consumidor.
- Regista cada mensagem recebida, incluindo entregas repetidas.

## Instalação no Raspberry Pi

Executar os comandos a partir desta pasta `r04_mqtt/`:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
nano .env
```

## Executar testes locais

Os 15 testes incluídos são sintéticos e não precisam de ligação ao broker nem do sensor:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

## Iniciar o consumidor

```bash
PYTHONPATH=src python -m observatorio.consumer.mqtt_client
```

Parar com `Ctrl+C`. O consumidor subscreve novamente o tópico quando o callback de ligação confirma uma ligação/religação. A primeira ligação depende de host, credenciais, DNS e rede corretos.

As mensagens são acrescentadas a `data/mqtt_received.jsonl`. O ficheiro está excluído do Git.

## Configuração TTS

Consultar `docs/CONFIGURAR_TTS.md`. Não assumir o host, tenant, application ID ou permissões: usar exatamente os dados apresentados na consola da instituição.

O TTS suporta MQTT 3.1.1 e QoS 0. QoS 0 não garante entrega nem recuperação de uplinks perdidos durante interrupções; o consumidor apenas pode registar as mensagens que efetivamente recebe.

## Payload Formatter do sensor

O formatter foi fornecido pelo docente, que o confirmou como adequado ao sensor. `payload_formatter/HKT_IAQ_1000_original_for_review.js` é o ficheiro original recebido, sem alterações, e o seu cabeçalho identifica HKT-IAQ-1000 (o equipamento da bancada é o HKT IAQ-900 O3). O código efetivamente instalado no TTS deve ser guardado nesta pasta, com a origem indicada.

As questões técnicas encontradas no formatter estão em `docs/ANALISE_PAYLOADER.md`. O consumidor não descodifica: quando o TTS não envia `decoded_payload`, regista `decode_status = decoded_payload_em_falta` e conserva o Base64.

## Âmbito do módulo

O módulo recebe e regista mensagens num ficheiro JSONL. Não normaliza valores, não persiste numa base de dados e não inclui Django/API, dashboard ou modelo digital. Não associa gateway a origem física exclusiva; uma transmissão pode ser recebida por mais de um gateway.

## Evidência necessária para considerar R04 demonstrado

`docs/EVIDENCIA_R04.md` regista a execução real (mensagem recebida por MQTT, dispositivo, aplicação, campos de evento, campos descodificados e limitações observadas). Os registos completos estão em `docs/evidencia/uplinks_reais_completo.jsonl`. Os testes sintéticos não substituem esta demonstração.
