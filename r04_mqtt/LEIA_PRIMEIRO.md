# Antes de integrar R04

1. Esta pasta é uma preparação isolada do R04, não a aplicação MP01 completa.
2. No repositório atual, colocar `r04_mqtt/` na raiz, sem alterar as pastas GL02.
3. Criar `.env` local a partir de `.env.example`; nunca publicar credenciais.
4. O formatter fornecido identifica HKT-IAQ-1000 e o enunciado identifica HKT IAQ-900 O3. Confirmar compatibilidade antes de o instalar.
5. Os testes são sintéticos. Só uma receção no Raspberry Pi, com uplink real e `decoded_payload` confirmado, serve como evidência de aquisição real R04.

Consultar `README.md` e `docs/` para instruções completas.
