from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from .routers import router as api_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://html-classic.itch.zone"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

app.include_router(api_router, prefix="")
