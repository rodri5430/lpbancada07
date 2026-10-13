# GL02 — Normalização de mensagens e revisão de código
## 1. Continuidade com GL01 (percurso principal)
1. No repositório GL01, verificar que o trabalho anterior está guardado e o estado
   está limpo: `git status --short`. Registar `git rev-parse --short HEAD`.
   Com alterações pendentes, parar e combinar como as guardar; não apagar.
2. Copiar SOMENTE o conteúdo desta pasta para uma pasta nova `atividades/gl02`
   dentro daquele repositório. Não sobrepor gl01_demo, tests ou docs da raiz.
3. Na nova pasta, confirmar `git rev-parse --show-toplevel`. Não executar git init.
4. Criar .venv segundo AMBIENTE.md. Registar a base fornecida, sem .venv:
```bash
git add .
git diff --cached --stat
git diff --cached
git commit -m "Acrescenta base didatica GL02 sem alterar GL01"
git switch -c gl02/normalizacao
```
`git add .` é executado APENAS dentro da pasta de atividade, após revisão do
.gitignore. Não adicionar pastas reservadas, segredos ou ficheiros de outro grupo.
Configurar a identidade local real se necessário, sem alterar a configuração global.
Os ramos main e gl02/normalizacao só são usados se não houver nomes incompatíveis;
não reutilizar nem apagar um ramo existente sem revisão com o docente.

## 2. Alternativa autónoma
Sem GL01 disponível, trabalhar numa pasta nova autorizada e sem repositório pai.
Após confirmar `git rev-parse --show-toplevel` (não deve encontrar repositório),
executar `git init -b main`, configurar a identidade local e registar a base.
Nunca criar um repositório aninhado. Registar o motivo desta alternativa.

## 3. Contrato, implementação e testes
Ler CONTRATO_GL02.md e preencher docs/contrato_e_testes.md antes de executar os casos.
Completar gl02_normalizacao/validacao.py, preservando interfaces e regras.
MT02 pode ser consultado/reutilizado com identificação; explicar as adaptações.
```bash
./.venv/bin/python -m unittest tests.test_arranque -v
./.venv/bin/python -m unittest tests.test_contrato -v
./.venv/bin/python -m unittest tests.test_grupo -v
./.venv/bin/python -m unittest discover -s tests -v
./.venv/bin/python -m gl02_normalizacao dados/lote_gl02.jsonl
```
Completar seis métodos em test_grupo.py. Não remover testes ou trocar falhas
por skip/pass para obter OK. A aprovação de casos não prova correção universal.
Estados previstos com a estrutura fornecida:
- Arranque: 2 testes aprovados, mesmo com funções incompletas.
- Tudo, antes da tarefa: 14 testes, com 6 errors (NotImplementedError) e 6 failures
  (self.fail deliberados). Os erros/falhas não são um defeito de instalação.
- Funções concluídas e testes do grupo ainda por fazer: 8 aprovados, 6 falhas.
- Funções e testes concluídos: 14 aprovados (ou mais, se criados outros testes).
- Lote concluído: 4 aceites; 6 rejeitadas; não deduplica as linhas 1 e 10.

## 4. Comparação e revisão
```bash
./.venv/bin/python comparar_candidatos.py
```
Prever pelo menos um contraexemplo para cada candidato antes de executar.
A e B são exemplos preparados para ensino, não respostas de IA. Não os integrar.
A atividade é realizável sem Internet. Uso opcional de IA requer o registo do MP01.
Preencher docs/ia_e_candidatos.md e docs/pedido_integracao.md, ou a ficha Word.
Na revisão por outro elemento, relacionar cada observação com regra, diff e teste.
```bash
git add gl02_normalizacao tests docs
git diff --cached
git commit -m "Implementa normalizacao e testes GL02"
git diff main...gl02/normalizacao -- .
```
Após apreciação e correções, registar a decisão no ramo, voltar a testar e integrar:
```bash
git add docs gl02_normalizacao tests
git diff --cached
git commit -m "Regista revisao e decisoes GL02"
git status --short
git switch main
git merge --no-ff gl02/normalizacao -m "Integra GL02 apos revisao"
./.venv/bin/python -m unittest discover -s tests -v
git log --oneline -5
```
Se a revisão pedir alteração, corrigir no ramo antes do merge. Não criar PR remoto
fictício: o registo local é suficiente na ausência de plataforma autorizada.

## 5. Conflito de treino: OUTRO repositório
A pasta-mãe $HOME/lp deve existir. A pasta de destino tem de ser NOVA e estar
fora de qualquer repositório. Executar primeiro na pasta da atividade:
```bash
./.venv/bin/python ferramentas/preparar_conflito.py --destino "$HOME/lp/gl02_conflito"
```
Depois, no terminal do cenário (não no projeto):
```bash
cd "$HOME/lp/gl02_conflito"
git config --local user.name "NOME_DO_AUTOR"
git config --local user.email "EMAIL_INSTITUCIONAL"
git status --short
git log --oneline --all --graph
git merge proposta-b
```
Substituir os dados do autor pelos reais autorizados. A saída de conflito e o
código não nulo do merge são esperados. Editar politica.py e preservar as duas
intenções: preservar None; não substituir por zero. Não conservar os marcadores.
```bash
git diff --name-only --diff-filter=U
python3 verificar_resolucao.py
git diff --check
git add politica.py
git commit -m "Resolve conflito preservando ambas as intencoes"
git status --short
```
Usar o Python preparado do ambiente; em Windows, `py -3` ou caminho aprovado.
Verificar 2 testes aprovados e nenhum caminho por resolver. Não editar o verificador.
A ferramenta só prepara ramos, não resolve o conflito. Não apaga pastas, não faz
push, não modifica o projeto e não configura o utilizador global.
Para desistir do merge de treino ainda não concluído: `git merge --abort` naquele
repositório, após confirmar com o docente. Não usar reset --hard, clean -fd ou push
--force. O cenário não tem remotos. Guardar no projeto apenas a síntese do exercício,
nunca a pasta .git do cenário nem um repositório inteiro dentro de outro.

## 6. Fecho
Conservar evidências, decidir o que está concluído/por retomar, responder à síntese
individual e registar a versão final. O hash é obtido após o commit; não se coloca
no próprio commit que se pretende identificar. Os modelos Markdown e a ficha Word
são alternativas. Não há nota autónoma neste guião.

## Proveniência e limites
Contrato e classe de erro: MT02; dados: MT01 através do pacote MT02, com hashes.
App fornecida adaptada do MT02; funções a concluir e guiões são elaboração GL02.
Não há hardware, MQTT, deduplicação, base de dados, segurança dos metadados ou
validação integral. Consultar CONTRATO_GL02.md e AMBIENTE.md.
