# Contrato didático MT02 — alcance e continuidade

## Função nuclear
- normalizar_valor recebe um objeto Python; aceita int/float finito/None.
- None é ausência, não zero; zero e negativos mantêm-se válidos.
- bool, str (incluindo '12'), listas e restantes tipos são rejeitados.
- ErroValidacao.campo é 'value'; motivo é 'tipo_invalido' ou 'nao_finito'.
- Não existem conversões numéricas, arredondamento ou efeitos externos.
- As entradas do contrato são tipos nativos simples; subclasses numéricas
  personalizadas não fazem parte dos exercícios.

## Adaptador de demonstração — não confundir com normalizador completo
normalizar_observacao verifica APENAS quantity, unit, value e quality.
Campos ausentes são erros; value=None é diferente de campo em falta.
Aceita apenas quantity='indice_demo' e unit='u_demo'. quality é 'missing'
para None e 'valid' para os restantes valores aceites. Usa uma cópia superficial
e preserva os outros campos sem os validar. Os dados MT01 são objetos planos.
Não valida identificadores, marcas temporais, proveniência, segurança de campos
adicionais ou identidade dos eventos. Não elimina repetições. Esses aspetos
serão especificados no projeto e nas sessões posteriores.

## Limites que não podem ser inferidos
Não se inventam tempos de medição, unidades, campos do sensor ou chave de evento.
A mesma mensagem reproduzida pode aparecer várias vezes neste exemplo: não se
reivindica a idempotência exigida pelo futuro R06. Não é uma solução de M1 pronta.
Na MA02 os booleanos estavam fora do domínio de entrada; aqui são incluídos
deliberadamente como dados a rejeitar. Os instrumentos não têm o mesmo contrato.

## JSON e execução
Dados MT01 são copiados dos ficheiros anteriores, sem alteração. No lote MT02,
cinco linhas produzem três observações aceites e duas rejeições.
NaN e Infinity não são números de JSON normalizado: os contraexemplos não
finitos são construídos em Python nos testes. O parser Python pode aceitar
extensões numéricas; esta demonstração não substitui um validador JSON completo.
