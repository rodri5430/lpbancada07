# Observatório ambiental — Bancada 07 (LP 2026/27, M1)

Projeto integrador MP01: aquisição de mensagens de um sensor HKT IAQ-900 O3 (LoRaWAN) através do The Things Stack (MQTT), normalização e validação das observações. Finalidade pedagógica; não é um sistema de certificação da qualidade do ar.

Este repositório corresponde ao marco **M1 (aquisição e normalização)**. Django, persistência relacional, modelo digital e contentores ficam para M2 e M3.

## Estrutura

```text
README.md              execução, testes e acesso à documentação
AMBIENTE.md            requisitos do ambiente (Python, Git, venv)
CONTRATO_GL02.md       contrato de normalização (quatro campos)
gl02_normalizacao/     normalização e validação de observações (sem rede)
tests/                 testes da normalização
dados/                 dados sintéticos de teste e proveniência
ferramentas/           verificação do ambiente
r04_mqtt/              consumidor MQTT do The Things Stack (R04)
docs/                  diagramas, plano M1, contratos de teste, registo de IA
```

## Executar os testes

A partir da raiz do repositório:

```bash
python3 -m venv .venv
./.venv/bin/python ferramentas/verificar_ambiente.py
./.venv/bin/python -m unittest discover -s tests -v          # normalização (14 testes)
./.venv/bin/python -m gl02_normalizacao dados/lote_gl02.jsonl # lote sintético: 4 aceites, 6 rejeitadas
```

Testes do consumidor MQTT (sintéticos, sem ligação ao broker):

```bash
cd r04_mqtt
python3 -m venv .venv && . .venv/bin/activate
python -m pip install -r requirements.txt
PYTHONPATH=src python -m unittest discover -s tests -v       # 15 testes
```

## Executar o consumidor MQTT (R04)

Requer acesso à aplicação no The Things Stack. Instruções completas em `r04_mqtt/README.md` e `r04_mqtt/docs/CONFIGURAR_TTS.md`.

```bash
cd r04_mqtt
cp .env.example .env      # preencher localmente; nunca publicar
PYTHONPATH=src python -m observatorio.consumer.mqtt_client
```

As credenciais ficam só em `.env` (ignorado pelo Git). `.env.example` contém apenas nomes de variáveis.

## Documentação e evidências

| Tema | Ficheiro |
|---|---|
| Plano, requisitos e arquitetura (M1) | `docs/plano_m1.md`, `docs/Diagrama de Contexto LP.drawio` |
| Contrato de normalização e testes | `CONTRATO_GL02.md`, `docs/contrato_e_testes.md` |
| Contrato da mensagem MQTT (R04) | `r04_mqtt/docs/CONTRATO_MENSAGEM_R04.md` |
| Evidência de receção real (R04) | `r04_mqtt/docs/EVIDENCIA_R04.md` |
| Análise do Payload Formatter | `r04_mqtt/docs/ANALISE_PAYLOADER.md` |
| Fontes e proveniência | `r04_mqtt/docs/FONTES_E_PROVENIENCIA.md`, `dados/PROVENIENCIA.md` |
| Revisão de código e utilização de IA | `docs/ia_e_candidatos.md`, `docs/pedido_integracao.md` |
| Guião GL02 original | `docs/GL02_guiao.md` |

## Notas

- A receção real por MQTT foi demonstrada na bancada 07; as limitações observadas estão em `r04_mqtt/docs/EVIDENCIA_R04.md`.
- O MQTT do The Things Stack usa QoS 0: não se promete entrega garantida nem recuperação de mensagens perdidas.
