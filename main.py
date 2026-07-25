from fastapi import FastAPI
from core.database import Base, engine
from routers import produtos

# Cria as tabelas no PostgreSQL se elas não existirem
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API projeto de estudo com Postgres",
    version="1.0.0",
)

# Registra o Router de Produtos
app.include_router(produtos.router)


@app.get("/", tags=["Health Check"])
def health_check():
    return {"status": "ok", "database": "PostgreSQL conectado!"}
