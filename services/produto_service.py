from sqlalchemy.orm import Session
from sqlalchemy import select

from core.database import get_db
from models.produto import ProdutoModel
from routers.produtos import buscar_produto
from schemas.produto import ProdutoCreate, ProdutoUpdate, ProdutoResponse

def criar_produto_service(payload: ProdutoCreate, db: Session):
    # ** unpack dict
    novo_produto = ProdutoModel(**payload.model_dump())

    db.add(novo_produto)
    db.commit()
    # Recarrega o objeto com o ID gerado pelo Postgres
    db.refresh(novo_produto)

    return novo_produto

def listar_produtos_service(db: Session, skip: int = 0, limit: int = 10):
    query = select(ProdutoModel).offset(skip).limit(limit)
    produtos = db.scalars(query).all()

    return produtos

def buscar_produto_service(produto_id: int, db: Session):
    produto = db.get(ProdutoModel, produto_id)

    return produto

def atualizar_produto_service(produto_id: int, payload: ProdutoUpdate, db: Session):
    produto = db.get(ProdutoModel, produto_id)
    if not produto:
        return False

    # Pega apenas os campos enviados no JSON (exclude_unset=True)
    dados_atualizacao = payload.model_dump(exclude_unset=True)
    for chave, valor in dados_atualizacao.items():
        setattr(produto, chave, valor)

    db.commit()
    db.refresh(produto)
    return produto

def deletar_produto_service(produto_id: int, db: Session):
    produto = db.get(ProdutoModel, produto_id)
    if not produto:
        return False

    db.delete(produto)
    db.commit()

    return True