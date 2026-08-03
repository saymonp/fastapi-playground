from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from schemas.produto import ProdutoCreate, ProdutoUpdate, ProdutoResponse

from services.produto_service import criar_produto_service, listar_produtos_service, buscar_produto_service, \
    atualizar_produto_service, deletar_produto_service

router = APIRouter(prefix="/produtos", tags=["Produtos"])


# 1. CRIAR (POST)
@router.post("/", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
def criar_produto(payload: ProdutoCreate, db: Session = Depends(get_db)):
    novo_produto = criar_produto_service(payload, db)

    return novo_produto


# 2. LISTAR TODOS (GET)
@router.get("/", response_model=List[ProdutoResponse])
def listar_produtos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    produtos = listar_produtos_service(db, skip, limit)

    return produtos


# 3. BUSCAR POR ID (GET)
@router.get("/{produto_id}", response_model=ProdutoResponse)
def buscar_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = buscar_produto_service(produto_id, db)
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Produto com ID {produto_id} não foi encontrado."
        )
    return produto


# 4. ATUALIZAR PARCIAL/TOTAL (PATCH/PUT)
@router.patch("/{produto_id}", response_model=ProdutoResponse)
def atualizar_produto(produto_id: int, payload: ProdutoUpdate, db: Session = Depends(get_db)):
    produto = atualizar_produto_service(produto_id, payload, db)
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado."
        )

    return produto


# 5. DELETAR (DELETE)
@router.delete("/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = deletar_produto_service(produto_id, db)

    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado."
        )

    return None
