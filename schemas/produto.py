from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


# 1. Base Schema: Campos comuns compartilhados
class ProdutoBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=100, description="Nome do produto")
    descricao: Optional[str] = Field(None, max_length=500, description="Descrição detalhada")
    preco: float = Field(..., gt=0, description="Preço do produto (deve ser maior que zero)")
    em_estoque: bool = Field(default=True, description="Status de disponibilidade")


# 2. Request Schema (Criar): Usado no POST
# Herda tudo do Base. Se precisasse de campos exclusivos de criação, colocaria aqui.
class ProdutoCreate(ProdutoBase):
    pass


# 3. Request Schema (Atualizar): Usado no PUT/PATCH
# Todos os campos viram opcionais para permitir atualização parcial.
class ProdutoUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=3, max_length=100)
    descricao: Optional[str] = Field(None, max_length=500)
    preco: Optional[float] = Field(None, gt=0)
    em_estoque: Optional[bool] = None


# 4. Response Schema: Usado nas respostas da API (Output DTO)
# Adiciona o ID e carimbos de data/hora que são gerados pelo sistema/banco.
class ProdutoResponse(ProdutoBase):
    id: int
    criado_em: datetime

    # Permite que o Pydantic leia diretamente atributos de objetos ORM (ex: SQLAlchemy)
    model_config = ConfigDict(from_attributes=True)