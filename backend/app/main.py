from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.controllers.data_controller import router
from app.services.generate_data import create_sensor_object
from apscheduler.schedulers.background import BackgroundScheduler
from app.models.schemas import Notification


app = FastAPI(tittle='Data and Hook')
scheduler = BackgroundScheduler(job_defaults={'max_instances': 10})
scheduler.add_job(create_sensor_object, 'interval',
                  seconds=20)


@app.on_event("startup")
def start_scheduler():
    scheduler.start()


@app.on_event("shutdown")
def stop_scheduler():
    scheduler.shutdown()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.webhooks.post("new-notification")
def notification(body: Notification):
    """
    When a new user subscribes to your service we'll send you a POST request with this
    data to the URL that you register for the event `http://localhost:8800/new-notification` in the dashboard.
    """


app.include_router(router)
