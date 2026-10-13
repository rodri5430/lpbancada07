"""Cria um cenário Git local numa pasta NOVA, fora de qualquer repositório.

Não modifica o repositório do projeto, não configura identidade global,
não cria remotos e não apaga nem substitui pastas. Requer Git >= 2.28.
Os commits de preparação são identificados como material didático.
"""
import argparse
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

VERIFICADOR = '"""Verifica a resolução da mensagem, não o normalizador do projeto."""\nimport unittest\nfrom pathlib import Path\n\nclass TestResolucao(unittest.TestCase):\n    def test_sem_marcadores(self):\n        texto = Path("politica.py").read_text(encoding="utf-8")\n        self.assertNotIn("<<<<<<<", texto)\n        self.assertNotIn(">>>>>>>", texto)\n\n    def test_duas_intencoes(self):\n        from politica import MENSAGEM_AUSENCIA\n        self.assertIn("preservar None", MENSAGEM_AUSENCIA)\n        self.assertIn("não substituir por zero", MENSAGEM_AUSENCIA)\n\nif __name__ == "__main__":\n    unittest.main()\n'


def preparar(destino: Path) -> None:
    git = shutil.which("git")
    if not git:
        raise RuntimeError("Git não encontrado; solicitar ambiente preparado.")
    versao = subprocess.check_output([git, "--version"], text=True)
    numeros = re.search(r"(\d+)\.(\d+)", versao)
    if not numeros or tuple(map(int, numeros.groups())) < (2, 28):
        raise RuntimeError("O exercício requer Git 2.28 ou posterior.")
    destino = destino.expanduser().absolute()
    if destino.exists() or destino.is_symlink():
        raise ValueError("O destino já existe; escolher outra pasta nova.")
    if not destino.parent.is_dir():
        raise ValueError("A pasta-mãe deve existir; prepará-la com o docente.")
    if any(k in os.environ for k in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE")):
        raise ValueError("Variáveis especiais Git ativas; usar um terminal normal.")
    estado = subprocess.run([git, "-C", str(destino.parent), "rev-parse", "--git-dir"],
                            capture_output=True, text=True)
    if estado.returncode == 0:
        raise ValueError("Escolher uma pasta FORA de qualquer repositório existente.")
    destino.mkdir()
    # Impedir execução de hooks herdados nesta preparação; âmbito só deste processo.
    hooks = destino / "hooks_vazios"
    hooks.mkdir()
    env = os.environ.copy()
    # Fixar finais de linha para o ensaio, independentemente da plataforma.
    comum = [git, "-c", "core.hooksPath=" + str(hooks),
             "-c", "core.autocrlf=false", "-c", "commit.gpgsign=false"]

    def executar(*args):
        subprocess.run(comum + list(args), cwd=destino, env=env,
                       text=True, capture_output=True, check=True)

    def registar(mensagem):
        executar("-c", "user.name=GL02 - preparacao didatica",
                 "-c", "user.email=gl02@exemplo.invalid", "commit", "-m", mensagem)

    executar("init", "-b", "main", "--template=")
    (destino / ".gitignore").write_text("__pycache__/\nhooks_vazios/\n", encoding="utf-8")
    (destino / ".gitattributes").write_text("*.py text eol=lf\n", encoding="utf-8")
    (destino / "politica.py").write_text('MENSAGEM_AUSENCIA = "Por especificar."\n', encoding="utf-8")
    (destino / "verificar_resolucao.py").write_text(VERIFICADOR, encoding="utf-8")
    executar("add", ".gitignore", ".gitattributes", "politica.py", "verificar_resolucao.py")
    registar("Base do cenario didatico GL02")
    executar("switch", "-c", "proposta-a")
    (destino / "politica.py").write_text('MENSAGEM_AUSENCIA = "Ausência: preservar None."\n', encoding="utf-8")
    executar("add", "politica.py")
    registar("Proposta A: preservar ausencia")
    executar("switch", "main")
    executar("switch", "-c", "proposta-b")
    (destino / "politica.py").write_text('MENSAGEM_AUSENCIA = "Ausência: não substituir por zero."\n', encoding="utf-8")
    executar("add", "politica.py")
    registar("Proposta B: distinguir zero")
    executar("switch", "proposta-a")
    print("Cenário criado. Proposta A ativa; nenhuma integração ainda executada.")
    print("Destino:", destino)
    print("Configurar identidade LOCAL real antes de registar a resolução.")
    print("Próximo passo manual: git merge proposta-b")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--destino", required=True, type=Path)
    args = parser.parse_args()
    try:
        preparar(args.destino)
    except (ValueError, RuntimeError, OSError, subprocess.CalledProcessError) as erro:
        print(f"Preparação não concluída: {erro}", file=sys.stderr)
        print("Não foi executada qualquer limpeza automática; rever com o docente.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
