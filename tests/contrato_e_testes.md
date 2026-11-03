# G1: Previsões e resultados dos testes
Grupo: preencher pelo grupo. Data: preencher na execução. Versão inicial: registar o commit de base.
Origem do contrato: MT02, projeção de quatro campos; formalização GL02/S1–S8.

| Caso | Entrada | Resultado esperado | Regra | Teste associado |
|---|---|---|---|---|
| Zero | `0` | Aceite como `int`, sem conversão para `float` | S1 | `test_zero` |
| Ausência | `None` com `quality="missing"` | Aceite; `value` permanece `None` | S1, S6 | `test_ausencia` |
| Negativo | `-2.5` | Aceite como `float`, sem arredondamento | S1 | `test_negativos_e_tipo` |
| Texto numérico | `"12"` | Rejeitado: `value / tipo_invalido` | S2 | `test_texto_numerico` |
| Booleano | `False` | Rejeitado: `value / tipo_invalido` | S2 | `test_booleanos` |
| Não finito | `float("inf")` | Rejeitado: `value / nao_finito` | S3 | `test_nao_finitos` |
| Campo value ausente | mapeamento sem `value` | Rejeitado: `value / campo_em_falta` | S4 | `test_value_em_falta` |
| Coerência | `None` com `quality="valid"` | Rejeitado: `quality / incoerente`; entrada não corrigida | S6 | `test_coerencia_quality` |
| Metadados | observação válida com campo adicional | Aceite; saída é cópia superficial e preserva o campo adicional | S7 | `test_copia_e_preservacao` |
| Formato | lista em vez de mapeamento | Rejeitado: `mensagem / formato_invalido` | S4, S8 | `test_formato` |
| Unidade | `unit="outra"` | Rejeitado: `unit / unidade_nao_admitida` | S5 | `test_unidade` |

## Interpretação do lote

O ficheiro `dados/lote_gl02.jsonl` contém dez linhas físicas: esperam-se quatro observações aceites e seis rejeições. A primeira e a décima linhas representam o mesmo evento e permanecem ambas na saída, porque esta aplicação didática não implementa deduplicação. A linha de JSON malformado deverá ser rejeitada sem impedir o processamento das linhas seguintes.

## Limites

Esta atividade valida apenas `quantity`, `unit`, `value` e `quality`. Não verifica a validade dos metadados adicionais, a identidade real do dispositivo, os tempos, a proveniência, a deduplicação, MQTT, a persistência ou uma API.
