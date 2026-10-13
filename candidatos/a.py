"""Candidato A: inadequado; ficheiro apenas para revisão, não integrar."""

def normalizar_valor(valor: object):
    """Limpa o valor (descrição deliberadamente insuficiente)."""
    try:
        return float(valor or 0)
    except Exception:
        return 0.0
