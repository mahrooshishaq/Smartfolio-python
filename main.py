from fastapi import FastAPI
from routers import extraction

app = FastAPI(title="Smartfolio Python Service", version="1.0.0")

app.include_router(extraction.router)


@app.get("/health")
def health():
    return {"status": "ok"}
