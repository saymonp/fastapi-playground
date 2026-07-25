from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from core.database import get_db
from models.produto import ProdutoModel
from schemas.produto import ProdutoCreate, ProdutoUpdate, ProdutoResponse

router = APIRouter(prefix="/produtos", tags=["Produtos"])


# 1. CRIAR (POST)
@router.post("/", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
def criar_produto(payload: ProdutoCreate, db: Session = Depends(get_db)):
    # Converte o Pydantic Schema para um dicionário e instancia a Model do ORM
    novo_produto = ProdutoModel(**payload.model_dump())
    
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto) # Recarrega o objeto com o ID gerado pelo Postgres
    return novo_produto


# 2. LISTAR TODOS (GET)
@router.get("/", response_model=List[ProdutoResponse])
def listar_produtos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    query = select(ProdutoModel).offset(skip).limit(limit)
    produtos = db.scalars(query).all()
    return produtos


# 3. BUSCAR POR ID (GET)
@router.get("/{produto_id}", response_model=ProdutoResponse)
def buscar_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.get(ProdutoModel, produto_id)
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Produto com ID {produto_id} não foi encontrado."
        )
    return produto


# 4. ATUALIZAR PARCIAL/TOTAL (PATCH/PUT)
@router.patch("/{produto_id}", response_model=ProdutoResponse)
def atualizar_produto(produto_id: int, payload: ProdutoUpdate, db: Session = Depends(get_db)):
    produto = db.get(ProdutoModel, produto_id)
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Produto não encontrado."
        )

    # Pega apenas os campos enviados no JSON (exclude_unset=True)
    dados_atualizacao = payload.model_dump(exclude_unset=True)
    for chave, valor in dados_atualizacao.items():
        setattr(produto, chave, valor)

    db.commit()
    db.refresh(produto)
    return produto


# 5. DELETAR (DELETE)
@router.delete("/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.get(ProdutoModel, produto_id)
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Produto não encontrado."
        )

    db.delete(produto)
    db.commit()
    return None