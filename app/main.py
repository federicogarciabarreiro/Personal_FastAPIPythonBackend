from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from .routers import router as api_router
from .services import insert_keep_alive
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import logging

logging.basicConfig(level=logging.INFO)

scheduler = AsyncIOScheduler()

def schedule_keep_alive():
    job = scheduler.get_job("keep_alive_task")
    if not job:
        logging.info("Agregando job de keep_alive para las 16:00")
        scheduler.add_job(insert_keep_alive, CronTrigger(hour=16, minute=0), id="keep_alive_task")
        scheduler.start()
    else:
        logging.info("El job 'keep_alive_task' ya está programado.")

app = FastAPI()

allowed_origins = [
    "https://html-classic.itch.zone",
    "https://github.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="")

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

@app.on_event("startup")
async def on_startup():
    logging.info("Aplicación iniciada, programando tarea de keep_alive.")
    schedule_keep_alive()

@app.get("/next-keep-alive")
async def get_next_keep_alive():
    job = scheduler.get_job("keep_alive_task")
    if job:
        next_run_time = job.next_run_time
        return {"next_run_time": next_run_time.strftime('%Y-%m-%d %H:%M:%S')}
    return {"message": "No job scheduled."}
