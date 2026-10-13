# Ambiente GL02
Adota-se a base GL01: Python >= 3.11 autorizado, módulo venv, Git >= 2.28 e editor.
O MT02 usa sintaxe compatível com 3.10; esta sessão segue o ambiente mínimo GL01.
A compatibilidade projetada não substitui o teste nas versões instaladas.
Sem bibliotecas externas, pip install, Docker, Django, Paho ou serviços de rede.

## Raspberry Pi ou GNU/Linux autorizado
Na raiz da pasta de atividade (README, gl02_normalizacao, tests e dados):
```bash
python3 -m venv .venv
./.venv/bin/python ferramentas/verificar_ambiente.py
./.venv/bin/python -m unittest tests.test_arranque -v
```
Não copiar o ambiente virtual GL01 ou MP02. Usar o mesmo interpretador no editor.
O Pi já deve estar preparado: não reinstalar, alterar rede, firmware ou credenciais.
O acesso SSH segue MP02; verificar a identidade e não desativar essa verificação.

## Windows preparado (PowerShell)
```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe ferramentas\verificar_ambiente.py
.\.venv\Scripts\python.exe -m unittest tests.test_arranque -v
```
Se `py` não estiver instalado, usar o executável Python 3 identificado pelo docente.
Substituir o prefixo ./.venv/bin/python em todos os comandos equivalentes;
os argumentos -m e nomes de módulos não mudam. Não alterar políticas de execução.
Na ferramenta de conflito, usar um caminho novo autorizado fora do repositório,
por exemplo "$HOME\lp\gl02_conflito", cuja pasta-mãe já exista.
Não se declara execução verificada nesta plataforma.

## Contingência
Após cerca de cinco minutos de tentativa acompanhada, usar o ambiente local
preparado pelo docente. Registar a execução como local, não como Pi verificado.
Sem remoto: pedido de integração em ficheiro, revisão e merge locais são suficientes.
Sem Git temporariamente: analisar as duas versões e a resolução em texto e
registar o que ficou NÃO OBSERVADO, a retomar com apoio; não afirmar execução.
Um estudante ausente em GL01 pode usar uma cópia nova do projeto_gl02, com
histórico próprio e origem documentada, sem falsificar um commit GL01.
