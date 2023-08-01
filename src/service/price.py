from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging
import requests
import datetime

from src.db.sqlite_db import add_price_sql

logger = logging.getLogger(__name__)


async def save_price():
    coindesk_api_url = 'https://api.coindesk.com/v1/bpi/currentprice.json'
    response = requests.get(coindesk_api_url).json()
    price = response['bpi']['USD']['rate_float']
    date_time = datetime.datetime.utcnow()
    add_price_sql(price=price, date_time_now=date_time)


async def schedule_jobs(scheduler: AsyncIOScheduler):
    job_id = f'get_price'
    if scheduler.get_job(job_id=job_id):
        scheduler.remove_job(job_id=job_id)
    scheduler.add_job(func=save_price, trigger='interval', seconds=2, id=job_id)
