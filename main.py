from fastapi import FastAPI

app = FastAPI(
    title="Minha API Profissional",
    description="API desenvolvida com FastAPI e gerenciada pelo UV",
    version="1.0.0",
    docs_url="/docs",      # Swagger UI
    redoc_url="/redoc",    # ReDoc
)

@app.get("/", tags=["Health Check"])
async def health_check():
    return {"status": "ok", "message": "API operacional!"}