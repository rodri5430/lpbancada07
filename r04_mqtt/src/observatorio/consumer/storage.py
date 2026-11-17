"""Registo acrescentado de mensagens recebidas em formato JSON Lines."""

import json
from pathlib import Path
from threading import Lock
from typing import Any


_WRITE_LOCK = Lock()


def guardar_jsonl(caminho: str | Path, registo: dict[str, Any]) -> None:
    """Acrescenta um registo sem substituir linhas anteriores."""
    destino = Path(caminho)
    destino.parent.mkdir(parents=True, exist_ok=True)
    linha = json.dumps(registo, ensure_ascii=False, allow_nan=False)
    with _WRITE_LOCK:
        with destino.open("a", encoding="utf-8") as ficheiro:
            ficheiro.write(linha + "\n")
            ficheiro.flush()
