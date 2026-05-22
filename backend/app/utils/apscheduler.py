from apscheduler.schedulers.background import BackgroundScheduler

from app.services.forecast_service import auto_generate_forecast


scheduler = BackgroundScheduler()


scheduler.add_job(

    auto_generate_forecast,

    "interval",

    minutes=10
    #seconds = 10 (For testing purpose) 
)

scheduler.start()