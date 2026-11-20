# G4: Revisão crítica e utilização de IA

## Candidatos fixos

Os candidatos A/B são exemplos preparados para ensino; não são respostas atribuídas a modelos de IA. O comparador usa dez casos e os resultados abaixo são os observados na execução de `python comparar_candidatos.py` na cópia de trabalho em 18/10/2026.

| Candidato | Contraexemplo analisado | Resultado observado | Regra violada | Decisão |
|---|---|---|---|---|
| A | Entrada `0` | Devolve `0.0` (`float`) em vez de `0` (`int`) | S1: preservar o tipo e o valor | Rejeitar; a mesma implementação também transforma ausência em zero e converte texto numérico. |
| B | Entrada `True` | Devolve `True` (`bool`) sem erro | S2: rejeitar booleanos, apesar de `bool` ser subclasse de `int` | Rejeitar tal como está; precisa de testar o tipo com cuidado. |

Resultado agregado do comparador: A conforme em 1/10 casos; B conforme em 8/10. Isto descreve apenas os dez casos definidos no guião e não demonstra correção universal nem compara qualidade de ferramentas de IA.

## Utilização efetiva de IA (quando os ficheiros propostos forem aproveitados)

- Ferramenta/modelo e data: ChatGPT (GPT-6).
- Finalidade: apoio à implementação das funções de normalização, elaboração dos seis testes do grupo e organização da documentação de contrato.
- Ficheiros influenciados: `gl02_normalizacao/validacao.py`, `tests/test_grupo.py`, `docs/contrato_e_testes.md`, este registo e `docs/plano_m1.md`.
- Contribuições propostas e aplicadas na cópia de trabalho para revisão: validação em sequência do contrato S1–S8; erros controlados sem incluir o valor de entrada; testes de tipos, coerência, cópia superficial e lote.
- Contribuições não feitas: não foi proposta integração MQTT, deduplicação ou validação de campos do sensor real, porque ficam fora do âmbito do GL02 e exigem confirmar o ambiente e o payload autorizado.
- Evidência de teste: `python -m unittest discover -s tests -v` — 14 testes aprovados; o lote apresenta 4 aceites e 6 rejeitadas.
- Revisão independente: **pendente**. Outro elemento do grupo deve rever o diff, questionar pelo menos uma decisão e registar o nome, commit revisto e decisão em `docs/pedido_integracao.md` antes da integração.

## Utilização de IA no R04 (consumidor MQTT)

- Ferramenta/modelo e data: Claude (Anthropic), 17 a 20/11/2026.
- Finalidade: apoio à documentação do módulo `r04_mqtt/`, análise do Payload Formatter, redação de `docs/EVIDENCIA_R04.md` e dos READMEs, orientação da execução no Raspberry Pi e limpeza do repositório para o M1. O código do consumidor MQTT (`r04_mqtt/src/` e testes) foi escrito pelo grupo.
- Ficheiros influenciados: `README.md`, `r04_mqtt/README.md`, `r04_mqtt/docs/`, `docs/EVIDENCIA_R04.md` e este registo.
- Contribuições aceites: texto da documentação e da evidência, análise das dúvidas no formatter, estrutura do README e da limpeza.
- Contribuições não aplicadas: não foi alterado nem reescrito o formatter do docente.
- Evidência de revisão e teste: execução real na bancada 07 em 17/11/2026 (`docs/EVIDENCIA_R04.md`); testes `PYTHONPATH=src python -m unittest discover -s tests` em `r04_mqtt/`. Revisão por outro elemento: [pendente ou NOME e PR].
- Dados enviados à ferramenta: o enunciado, a estrutura do repositório e excertos de uplinks (identificadores e bytes de payload). Nenhuma credencial foi partilhada.

