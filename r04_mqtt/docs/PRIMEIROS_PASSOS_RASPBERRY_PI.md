# Primeiros passos no Raspberry Pi

Executar a partir da pasta `r04_mqtt/` depois de esta estar copiada para o repositório de trabalho no Raspberry Pi.

## 1. Preparar o ambiente

```bash
python3 --version
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
```

Se a criação do ambiente ou instalação de dependências estiver bloqueada pelo ambiente institucional, parar e pedir orientação ao docente; não alterar o ambiente GL02 para contornar a restrição.

## 2. Criar configuração local

```bash
cp .env.example .env
nano .env
```

Preencher os valores de `MQTT_HOST`, `MQTT_USERNAME`, `MQTT_PASSWORD`, `MQTT_TOPIC` e `MQTT_CLIENT_ID` com os dados reais fornecidos na consola TTS. Não enviar `.env` para GitHub.

## 3. Executar testes locais

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

Os testes são sintéticos. Registar a versão do Python e o resultado observado.

## 4. Executar o consumidor

```bash
PYTHONPATH=src python -m observatorio.consumer.mqtt_client
```

Numa execução correta, o terminal deverá indicar ligação estabelecida e subscrição ativa. Quando chegar um uplink, deverá indicar `device_id`, `f_cnt`, estado de descodificação e nomes dos campos descodificados (sem imprimir os valores no log).

## 5. Verificar o registo

Noutro terminal, na mesma pasta:

```bash
tail -f data/mqtt_received.jsonl
```

Confirmar que a mensagem foi registada e que o JSON contém a identificação do dispositivo e o `decoded_payload` emitido pelo TTS.

## 6. Parar e conservar evidências

Parar com `Ctrl+C`. Copiar para o relatório apenas a evidência necessária, ocultando credenciais e evitando publicar dados operacionais sem autorização. O ficheiro `data/mqtt_received.jsonl` fica excluído do Git por omissão.
