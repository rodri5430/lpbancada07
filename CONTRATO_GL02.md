# GL02 — Contrato de normalização parcial
Versão 1.0 — 30/09/2026. Base: MT02, secções 2–7 e EX03; MP01, R02/R03/R05/R12.

O GL01 selecionava sete campos para apresentação. Aqui verifica-se a projeção
semântica de QUATRO campos do MT02, preservando os restantes. Não se altera
retroativamente o contrato do GL01 nem se resolve o normalizador integral de M1.
As regras S1–S8 são identificadores didáticos locais, não novos requisitos R do MP01.

## Interface, responsabilidades e resultado
- `normalizar_valor(valor: object) -> int | float | None`.
- `normalizar_observacao(mensagem: Mapping[str, object]) -> dict[str, object]`.
- `ErroValidacao(campo, motivo)` fornecida, sem guardar a mensagem recebida.
- Domínio: tipos Python nativos simples ou mapeamentos de campos simples;
  subclasses numéricas personalizadas não integram o exercício.
- Não fazer I/O, instalar pacotes, abrir ligações ou alterar a entrada nas funções.
- Chama-se normalização à verificação e conservação de uma representação
  coerente; não à conversão generalizada de texto, unidades ou números.

## Regras verificáveis
| ID | Regra |
|---|---|
| S1 | Aceitar int, float finito e None. Preservar zero, negativos e tipo numérico; não arredondar. |
| S2 | Rejeitar bool, str (incluindo texto numérico), listas e restantes tipos não admitidos. |
| S3 | Rejeitar float não finito. Criar NaN/inf em testes Python; não declarar que são números JSON válidos. |
| S4 | Exigir um Mapping e a presença de quantity, unit, value e quality. Campo ausente é diferente de value=None. |
| S5 | Exigir quantity='indice_demo' e unit='u_demo', sem deduzir grandezas/unidades reais. |
| S6 | quality='missing' apenas para None; 'valid' para os números aceites. Rejeitar incoerências; não autocorrigir. |
| S7 | Devolver uma cópia superficial; não alterar a entrada. Preservar restantes campos SEM os validar. |
| S8 | Sinalizar ErroValidacao com campo e motivo controlado. Não inserir dados da entrada nos erros. |

## Motivos controlados (mesmos do exemplo MT02)
| Situação | campo | motivo |
|---|---|---|
| Não é um mapeamento | mensagem | formato_invalido |
| Campo obrigatório ausente | nome do campo | campo_em_falta |
| Grandeza diferente | quantity | grandeza_nao_admitida |
| Unidade diferente | unit | unidade_nao_admitida |
| Tipo inválido | value | tipo_invalido |
| Float não finito | value | nao_finito |
| Quality incompatível | quality | incoerente |

Para reduzir ambiguidade, seguir a sequência do exemplo MT02: formato; presença
em quantity/unit/value/quality; grandeza; unidade; valor; quality. Só é necessário
relatar a primeira violação detetada, não construir um relatório de todos os erros.
As chamadas com [] são deliberadas para testar a fronteira, apesar da anotação.

## Adaptador de ficheiros já fornecido
- JSONL pequeno e sintético; uma observação por linha.
- Linha vazia ignorada; números de linha mantêm a contagem física.
- `JSONDecodeError`: motivo json_invalido; `ErroValidacao`: campo e motivo.
- Prosseguir após esses erros previstos; não esconder erros de programação.
- Código de saída 0: lote processado, mesmo com rejeições; 2: falha de leitura.
- Antes da implementação, NotImplementedError é esperado: não o capturar
  para transformar uma tarefa por realizar numa aparente rejeição de dados.
- Lote com dez linhas: 4 aceites e 6 rejeitadas. Repetições permanecem repetições.

## Limites
Sem sensor/TTN/MQTT, validação de identificação/tempos/proveniência, deduplicação,
persistência, segurança de campos adicionais, API ou contentores. Metadados podem
ser preservados sem estar corretos: não confundir transporte com validação.
Cópia superficial não isola objetos aninhados nem torna a saída imutável.
O parser da biblioteca Python não é apresentado como validador JSON estrito.
Não há nota autónoma, percentagem mínima de cobertura nem requisito de serviço pago.
