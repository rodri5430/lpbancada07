"""Observa versões locais; não altera contas, rede ou equipamentos."""
import json
import platform
import shutil
import subprocess
import sys

info = {"python": platform.python_version(), "sistema": platform.system(),
        "arquitetura": platform.machine(),
        "ambiente_virtual": sys.prefix != sys.base_prefix,
        "versao_compativel_gl02": sys.version_info >= (3, 11)}
git = shutil.which("git")
info["git"] = subprocess.check_output([git, "--version"], text=True).strip() if git else "não observado"
print(json.dumps(info, ensure_ascii=False, indent=2))
raise SystemExit(0 if info["versao_compativel_gl02"] else 2)
