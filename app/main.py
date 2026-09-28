from fastapi import FastAPI

from app.api.v1.router import api_router


app = FastAPI(
    title="Construction Inventory API",
    version="1.0.0",
)

app.include_router(api_router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}