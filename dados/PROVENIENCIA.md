# Proveniência dos dados
- `mt01/`: cópias byte a byte dos quatro ficheiros incluídos no pacote MT02,
  provenientes dos exemplos MT01. Todos são sintéticos.
- `CONTRATO_MT02_ORIGINAL.md`: cópia inalterada do contrato MT02.
- `lote_gl02.jsonl`: dez linhas construídas para este GL02. A linha 9 é
  deliberadamente JSON malformado; não deve ser corrigida no ficheiro.
  As linhas 1 e 10 reproduzem o mesmo evento. O normalizador NÃO deduplica.
- Resultado depois da implementação: 4 observações aceites e 6 rejeições.
- Não há mensagens físicas do sensor, credenciais, medições reais nem
  validação da disponibilidade de qualquer grandeza no equipamento.
- SHA-256 dos ficheiros herdados: `HASHES_ORIGEM.json`.
