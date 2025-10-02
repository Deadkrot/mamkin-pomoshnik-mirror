from datetime import datetime
import pytz

def now_tz(tz_str: str) -> datetime:
    return datetime.now(pytz.timezone(tz_str))
