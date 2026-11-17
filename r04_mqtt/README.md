# R04 — Consumidor MQTT do The Things Stack

> **Estado:** implementação preparada e testada apenas com mensagens sintéticas. A ligação ao broker e a receção do sensor físico ainda têm de ser demonstradas no ambiente autorizado.

Este módulo é uma pasta autónoma para preparar o requisito R04 do MP01. Recebe eventos JSON publicados pelo The Things Stack (TTS) através de MQTT, identifica a aplicação/dispositivo, preserva `received_at`, `f_cnt`, `f_port`, `frm_payload` e `decoded_payload` quando disponíveis e acrescenta um registo por mensagem a um ficheiro JSONL.

## Relação com o repositório atual

O repositório `lpbancada07` disponível atualmente está identificado no seu README como atividade GL02. O GL02 exclui explicitamente hardware, MQTT, serviços de rede e deduplicação. Por isso:

- colocar esta pasta `r04_mqtt/` na raiz do repositório apenas como **área temporária de preparação**;
- não colocar estes ficheiros em `gl02_normalizacao/`;
- não alterar os ficheiros existentes de GL02;
- quando o repositório global GL01/MP01 estiver disponível, transferir `r04_mqtt/src/observatorio/consumer/` para a estrutura `src/observatorio/consumer/` desse projeto e mover a documentação/testes correspondentes;
- não afirmar que o módulo temporário na raiz do repositório GL02 é a integração final da arquitetura MP01.

Ver `docs/INTEGRACAO_TEMPORARIA.md`.

## O que o módulo faz

- Usa MQTT 3.1.1 com TLS, normalmente na porta 8883.
- Usa as credenciais apresentadas em **The Things Stack > Integrations > MQTT**.
- Subscreve o tópico de uplinks configurado em `MQTT_TOPIC`, normalmente `v3/{application_id}@{tenant_id}/devices/+/up` em instalações multi-tenant.
- Valida a coerência entre o tópico recebido e `application_id` / `device_id` no JSON.
- Preserva os campos descodificados pelo TTS em `uplink_message.decoded_payload` sem voltar a descodificar o payload binário.
- Preserva `frm_payload` em Base64 para rastreabilidade.
- Regista `received_at` apenas quando fornecido pelo TTS e cria `ingested_at` para o instante de receção/processamento pelo consumidor.
- Regista cada mensagem recebida, sem deduplicação: a política R06 é uma tarefa separada.

## Instalação no Raspberry Pi

Executar os comandos a partir desta pasta `r04_mqtt/`:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
nano .env
```

Preencher `.env` com os valores reais da consola TTS. Não partilhar o ficheiro nem o carregar para o GitHub.

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

Foi incluído em `payload_formatter/HKT_IAQ_1000_original_for_review.js` o ficheiro recebido do utilizador, sem alterações. **Não o publicar automaticamente no TTS sem validação.** O cabeçalho identifica HKT-IAQ-1000, enquanto o MP01 identifica o equipamento da bancada como HKT IAQ-900 O3. A compatibilidade tem de ser confirmada pelo docente/fabricante.

A análise das questões encontradas está em `docs/ANALISE_PAYLOADER.md`. Até o formatter produzir `decoded_payload`, o consumidor regista que a descodificação está ausente e conserva o Base64; isso, por si só, não demonstra a relação pedida entre os campos descodificados e a observação real.

## Limites em relação ao MP01

Este módulo não implementa R05 (contrato/normalização integral), R06 (idempotência), persistência relacional, Django/API, dashboard ou modelo digital. Não associa gateway a origem física exclusiva; uma transmissão pode ser recebida por mais de um gateway.

## Evidência necessária para considerar R04 demonstrado

Preencher `docs/EVIDENCIA_R04.md` após a execução real. A evidência deve mostrar uma mensagem real recebida por MQTT, o dispositivo, a aplicação, os campos de evento e os campos descodificados devolvidos pelo TTS. Os testes sintéticos não substituem esta demonstração.
