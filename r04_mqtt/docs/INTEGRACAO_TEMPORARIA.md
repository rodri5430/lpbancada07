# Como acrescentar R04 ao repositório atualmente disponível

## Decisão de organização

O repositório disponível (`lpbancada07`) é identificado pelo README como atividade GL02 e declara que não inclui MQTT, hardware ou serviços de rede. Como ainda não está disponível o repositório global GL01/MP01, esta pasta deve ser acrescentada apenas como módulo temporário e isolado na raiz:

```text
lpbancada07/
├── candidatos/
├── dados/
├── docs/
├── ferramentas/
├── gl02_normalizacao/
├── tests/
├── ...ficheiros GL02 existentes...
└── r04_mqtt/        # nova pasta; não misturar com GL02
```

Não substituir nem mover ficheiros existentes. Não copiar o `.venv` para GitHub.

## Passos recomendados no GitHub

1. Criar/selecionar um ramo de trabalho separado, por exemplo `r04/preparacao-mqtt`.
2. A partir do ZIP, carregar apenas a pasta `r04_mqtt/` para a raiz do repositório.
3. Confirmar que `.env.example` foi carregado, mas que `.env` NÃO existe no GitHub.
4. Rever o diff e confirmar que nenhum ficheiro de GL02 foi alterado.
5. Guardar o commit com uma mensagem clara, por exemplo `Adiciona preparação isolada do consumidor MQTT R04`.
6. Não fazer merge para `main` como se esta fosse a integração global MP01 sem primeiro confirmar com o docente/elementos do grupo.

## Transferência para o projeto global MP01

Quando o repositório principal estiver disponível, transferir o módulo para a raiz desse projeto. O conteúdo `src/observatorio/consumer/` passa a integrar o `src/observatorio/` global. Os testes vão para `tests/` global e a documentação para `docs/` global. A localização temporária `r04_mqtt/` deixa de ser necessária.

Antes de transferir, confirmar se já existem pacotes `observatorio`, `consumer`, configuração comum ou convenções de logging no projeto global. Integrar sem duplicar módulos.
