from fastapi import FastAPI 

from fastapi_utils.tasks import repeat_every
import logging
import os
import datetime
import models
import config.database as database

from routers import authRoutes, userRoutes

# create database tables
database.db.connect()

database.db.create_tables([models.User])

database.db.close()

# get root logger
logger = logging.getLogger(__name__)

# setup loggers
logging.config.fileConfig('./config/logging.conf', disable_existing_loggers=False)
logging.basicConfig(filename='logfile.log',
                    filemode='w',
                    level=logging.INFO)

# create app 
app = FastAPI(
    title="myApp",
    version="1.0"
)

# include routers
app.include_router(authRoutes.router)
app.include_router(userRoutes.router)


# cron job that run every 24 hours to change the log file
@app.on_event("startup")
@repeat_every(wait_first=True, seconds=24 * 60 * 60)  # 24 hours
async def changeLogfileName():
    currentDate = datetime.datetime.today().strftime('%d-%b-%Y')
    os.rename(r'./logs/logfile.log', r'./logs/logfile_' +
              str(currentDate) + '.log')






