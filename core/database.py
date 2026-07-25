from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from dotenv import load_dotenv
import os

load_dotenv()
# URL de Conexão: postgresql+psycopg://usuario:senha@host:porta/nome_banco
DATABASE_URL = os.getenv("DATABASE_URL")

# Engine de conexão do SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    echo=True, # Log das queries SQL no terminal (útil em dev)
)

# Fabrica sessões para interagir com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe Base para criar os Models ORM
Base = declarative_base()


# Dependência injetada nas rotas: Abre conexão -> Entrega a sessão -> Fecha conexão
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()