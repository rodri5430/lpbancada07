# G1: Previsões antes da implementação
Grupo: ___  Data: ___  Versão inicial: ___
Origem do contrato: MT02, projeção de quatro campos; formalização GL02/S1–S8.

| Caso | Entrada | Resultado ou campo/motivo esperado | Regra | Teste associado |
|---|---|---|---|---|
| Zero | `0` | A preencher antes de executar | S1 | |
| Ausência | `None` | | S1 | |
| Negativo | `-2.5` | | S1 | |
| Texto numérico | `"12"` | | S2 | |
| Booleano | `False` | | S2 | |
| Não finito | `float("inf")` | | S3 | |
| Campo value ausente | objeto sem `value` | | S4 | |
| Coerência | `None` com `quality="valid"` | | S6 | |
| Metadados | objeto válido com campos adicionais | | S7 | |

Uma linha pode ligar-se a mais de um teste. Não obter os resultados esperados
copiando a saída de um candidato. Atualizar a tabela se for esclarecida uma
ambiguidade com o docente, deixando registada a decisão.
