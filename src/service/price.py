import logging
import yfinance as yf
from requests import Session
from requests_cache import CacheMixin, SQLiteCache
from requests_ratelimiter import LimiterMixin, MemoryQueueBucket
from pyrate_limiter import Duration, RequestRate, Limiter


logger = logging.getLogger(__name__)


class CachedLimiterSession(CacheMixin, LimiterMixin, Session):
    pass


async def get_historical_price(period: str, interval: str):
    session = CachedLimiterSession(
        limiter=Limiter(RequestRate(1, Duration.SECOND * 2)),  # max 1 requests per 2 seconds
        bucket_class=MemoryQueueBucket,
        backend=SQLiteCache("yfinance.cache"),
    )

    btc_usd = yf.Ticker("BTC-USD", session=session)
    hist = btc_usd.history(period=period, interval=interval)
    return hist

