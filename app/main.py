from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.routers import router as api_router

app = FastAPI()

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

app.include_router(api_router, prefix="/api")
