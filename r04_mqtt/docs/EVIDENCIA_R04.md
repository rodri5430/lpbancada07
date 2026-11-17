# Evidência de aceitação — R04 (preencher após ensaio real)

> Não preencher com os dados da fixture dos testes. Usar apenas evidência obtida na bancada ou uma alternativa autorizada pelo docente e devidamente identificada.

## Identificação da demonstração

- Data/hora local da demonstração:
- Grupo/bancada:
- Raspberry Pi utilizado:
- Versão do código (branch e commit):
- Host MQTT (hostname, sem credenciais):
- Aplicação TTS:
- Dispositivo (`device_id`):
- `dev_eui` (se disponibilizado):

## Mensagem recebida

- Tópico efetivamente recebido:
- `received_at` fornecido pelo TTS:
- `f_cnt`:
- `f_port`:
- `frm_payload` (Base64, se autorizado):
- `decoded_payload` (copiar exatamente os campos/valores apresentados pelo TTS):
- Gateway(s) em `rx_metadata`, se disponíveis:

## Resultado do consumidor

- Ligação MQTT estabelecida: SIM / NÃO
- Subscrição aceite: SIM / NÃO
- Mensagem recebida: SIM / NÃO
- Mensagem registada no JSONL: SIM / NÃO
- `decode_status`: decoded / decoded_payload_em_falta
- Caminho do ficheiro de registo:
- Capturas/evidências associadas:

## Relação entre origem e campos

Explicar como o `device_id`/`dev_eui` identifica o dispositivo e como a mensagem recebida contém os campos que o Payload Formatter do TTS descodificou. Distinguir `received_at` de `ingested_at`; não declarar um instante de medição que não esteja presente/confirmado.

## Limitações e problemas observados

- Perdas/interrupções/reconexões observadas:
- Ausência de `decoded_payload`, se aplicável:
- Compatibilidade do formatter com o modelo do sensor confirmada por:
- Outras limitações:

## Estado da aceitação

- [ ] Foi recebida uma observação real através de MQTT.
- [ ] O dispositivo foi identificado.
- [ ] A mensagem foi relacionada com os campos descodificados.
- [ ] Foi conservada evidência reproduzível e sem credenciais.

Se foi usada alternativa autorizada, identificar a autorização e não a apresentar como aquisição física demonstrada.
