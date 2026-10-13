"""Erro controlado, reutilizado do exemplo MT02 (classe fornecida)."""

class ErroValidacao(ValueError):
    """Indica o campo e o motivo; não incorpora o conteúdo da mensagem."""

    def __init__(self, campo: str, motivo: str) -> None:
        self.campo = campo
        self.motivo = motivo
        super().__init__(f"{campo}: {motivo}")
