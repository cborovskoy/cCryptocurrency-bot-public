import datetime
import logging
import yfinance as yf
from requests import Session
from requests_cache import CacheMixin, SQLiteCache
from requests_ratelimiter import LimiterMixin, MemoryQueueBucket
from pyrate_limiter import Duration, RequestRate, Limiter
import pandas as pd

logger = logging.getLogger(__name__)


class CachedLimiterSession(CacheMixin, LimiterMixin, Session):
    pass


async def get_historical_price(period_in_days: int, interval: str) -> pd.DataFrame:
    session = CachedLimiterSession(
        limiter=Limiter(RequestRate(1, Duration.SECOND * 2)),  # max 1 requests per 2 seconds
        bucket_class=MemoryQueueBucket,
        backend=SQLiteCache("yfinance.cache"))

    btc_usd = yf.Ticker("BTC-USD", session=session)

    end_date = datetime.datetime.now(datetime.timezone.utc)
    start_date = end_date - datetime.timedelta(days=period_in_days)

    result = btc_usd.history(start=start_date, end=end_date, interval=interval)
    result = pd.concat([result, btc_usd.history(period="1d", interval="1m").iloc[-1].to_frame().T])
    return result
