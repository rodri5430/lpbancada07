# Análise do Payload Formatter recebido

## Proveniência e compatibilidade

O ficheiro original foi fornecido pelo grupo/docente como `payloader_formatter.js` e foi copiado sem alterações para `payload_formatter/HKT_IAQ_1000_original_for_review.js`.

O cabeçalho do código identifica:

- fabricante/direitos: HKT SmartHard, 2023;
- produto: `HKT-IAQ-1000`.

O enunciado MP01 identifica o equipamento disponibilizado à bancada como `HKT IAQ-900 O3`. A informação disponível não prova que o formatter do IAQ-1000 seja compatível com o IAQ-900 O3. Confirmar com o docente/fabricante antes de o instalar como decoder do sensor atribuído.

## Questões técnicas a verificar antes de utilizar

1. **Conversões de 16 bits:** `byteToUint16()` calcula `bytes[0] * 0xFF + bytes[1]`. Em representação big-endian convencional, o fator do primeiro byte é `0x100`. Não alterar sem confirmar a ordem de bytes do protocolo.
2. **Conversões de 24 bits:** `byteToInt32()` usa `0xFF * 0xFF` e `0xFF`. É necessário confirmar a base aritmética e o sinal previsto no protocolo. A variável `temp` é calculada, mas o resultado utilizado para `temperature` é calculado novamente.
3. **Nome da função de leitura:** `readUInt16LE()` tem um nome que sugere little-endian, mas o cálculo `(bytes[0] << 8) + bytes[1]` corresponde a big-endian. A regra correta deve ser confirmada no protocolo.
4. **ID do dispositivo:** `hexToString()` converte a lista através de `bytes.toString(16)` e não aplica preenchimento a dois dígitos por byte. Confirmar o formato do identificador esperado.
5. **Tipo `0x2B`:** o código lê até três bytes a partir da posição do valor, mas avança apenas um byte. Confirmar o layout deste campo e se a temperatura deve ser lida antes/depois do indicador de unidade.
6. **Tipo `0x2C`:** o comentário indica modo de visualização, mas o resultado é guardado em `temperature_unit`. Confirmar se o nome do campo está correto.
7. **Código duplicado:** o ficheiro inclui blocos para TTN e ChirpStack, funções auxiliares repetidas e wrappers diferentes. Para TTS deve existir uma única função `decodeUplink(input)` adequada ao runtime JavaScript do TTS.
8. **Limites do parser:** confirmar comprimentos mínimos/máximos antes de aceder a cada byte, comportamento perante tipos desconhecidos e tratamento de payload incompleto.

## O que fazer

- Não corrigir estes pontos por suposição.
- Pedir uma mensagem real (bytes/hex ou `frm_payload`) e documentação do layout ao docente/fabricante.
- Testar cada tipo de campo com vetores confirmados.
- Verificar que uma mensagem inválida devolve `errors` e não um objeto de medições aparentemente válido.
- Só depois colocar a versão validada em The Things Stack > Payload formatters > Uplink.
- Guardar a versão original e documentar as alterações, respetiva origem e testes.

O consumidor MQTT não reimplementa este decoder. O TTS executa `decodeUplink(input)` e publica a saída em `uplink_message.decoded_payload`. Se o decoder falhar, o evento pode continuar a chegar com `frm_payload` sem `decoded_payload`.
