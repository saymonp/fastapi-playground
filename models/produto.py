from datetime import datetime, timezone
from sqlalchemy import String, Text, Float, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from core.database import Base


class ProdutoModel(Base):
    __tablename__ = "produtos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    descricao: Mapped[str | None] = mapped_column(Text, nullable=True)
    preco: Mapped[float] = mapped_column(Float, nullable=False)
    em_estoque: Mapped[bool] = mapped_column(Boolean, default=True)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc)
    )