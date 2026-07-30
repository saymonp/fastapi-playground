from sqlalchemy.orm import Session
from sqlalchemy import select

from core.database import get_db
from models.produto import ProdutoModel
from schemas.produto import ProdutoCreate, ProdutoUpdate, ProdutoResponse


def criar_produto_service(payload: ProdutoCreate, db: Session):
    # ** unpack dict
    novo_produto = ProdutoModel(**payload.model_dump())

    db.add(novo_produto)
    db.commit()
    # Recarrega o objeto com o ID gerado pelo Postgres
    db.refresh(novo_produto)

    return novo_produto