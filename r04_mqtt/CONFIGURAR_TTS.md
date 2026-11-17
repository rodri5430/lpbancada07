# Configurar The Things Stack para MQTT

Os valores concretos dependem da instância e da aplicação atribuídas à bancada. Não copiar host, application ID, tenant ou credenciais de exemplos da Internet.

1. Abrir a consola The Things Stack usada pela unidade curricular.
2. Abrir a aplicação à qual está associado o HKT.
3. Abrir **Integrations > MQTT**.
4. Consultar o hostname/servidor MQTT indicado pela consola.
5. Criar uma API Key com as permissões mínimas necessárias para ler os eventos da aplicação, de acordo com a configuração disponibilizada pelo docente.
6. Registar o username indicado pela integração. Em ambientes multi-tenant, o formato documentado é `application_id@tenant_id`; em The Things Stack Open Source o tenant pode não existir.
7. Preencher localmente o ficheiro `.env` a partir de `.env.example`.
8. Usar TLS na porta 8883, salvo indicação explícita diferente da instalação institucional.
9. Usar QoS 0, suportado pelo serviço de integração MQTT do TTS.
10. Subscrever o tópico de uplinks de todos os dispositivos da aplicação. Em multi-tenant, o formato é `v3/{application_id}@{tenant_id}/devices/+/up`; em Open Source, normalmente `v3/{application_id}/devices/+/up`.
11. Confirmar que o dispositivo tem um Uplink Payload Formatter configurado e que os eventos contêm `uplink_message.decoded_payload`.

## Variáveis do `.env`

| Variável | Origem/uso |
|---|---|
| `MQTT_HOST` | Host indicado na integração MQTT, sem protocolo. |
| `MQTT_PORT` | Normalmente `8883` para TLS. |
| `MQTT_USERNAME` | Username fornecido/indicado pela integração. |
| `MQTT_PASSWORD` | API Key criada; apenas no `.env` local. |
| `MQTT_TOPIC` | Tópico de uplinks da aplicação. |
| `MQTT_CLIENT_ID` | Identificador único desta instância do consumidor. |
| `MQTT_KEEPALIVE` | Intervalo keepalive, por omissão 60 segundos. |
| `MQTT_OUTPUT_PATH` | Ficheiro JSONL local onde ficam os eventos recebidos. |

Não enviar capturas que mostrem a API Key. Se uma credencial for publicada acidentalmente, revogá-la e criar outra.
