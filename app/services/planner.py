from datetime import datetime, timedelta, time
from typing import List, Tuple
from .age_rules import feeds_by_age_months, naps_count_by_age_months, wake_windows_by_age_months

def parse_hhmm(s: str) -> time:
    hh, mm = map(int, s.split(':'))
    return time(hh, mm)

def plan_day(day: datetime, age_months: int, feeds_per_day: int, wake_time: str, night_start: str, night_end: str) -> dict:
    wt = parse_hhmm(wake_time)
    ns = parse_hhmm(night_start)
    ne = parse_hhmm(night_end)

    start_dt = datetime.combine(day.date(), wt)
    night_start_dt = datetime.combine(day.date(), ns)
    if night_start_dt <= start_dt:
        night_start_dt = night_start_dt  # предполагаем, что ночь в тот же календарный день начинается позже подъёма

    # Ночной конец может быть на след. день — пока не используем в раскладке дня
    # night_end_dt = datetime.combine(day.date(), ne)
    # if night_end_dt <= night_start_dt:
    #     night_end_dt += timedelta(days=1)

    day_window_minutes = max(1, int((night_start_dt - start_dt).total_seconds() // 60))
    if feeds_per_day < 1:
        feeds_per_day = feeds_by_age_months(age_months)

    step = day_window_minutes // feeds_per_day
    feeds = []
    for i in range(feeds_per_day):
        t = start_dt + timedelta(minutes=step * i)
        if t >= night_start_dt:
            t = night_start_dt - timedelta(minutes=30)
        feeds.append((t, 'feed'))

    # Сны из окон бодрствования
    ww = wake_windows_by_age_months(age_months)
    naps = []
    cursor = start_dt + timedelta(minutes=60)  # небольшой лаг до первого сна
    for w in ww:
        nap_start = cursor
        nap_dur = 60 if age_months <= 6 else 90
        nap_end = nap_start + timedelta(minutes=nap_dur)
        if nap_end >= night_start_dt:
            break
        naps.append((nap_start, nap_end))
        cursor = nap_end + timedelta(minutes=int(w * 60))

    # Сдвигаем кормления, если попали внутрь сна: переносим за 25 минут до начала сна
    adjusted = []
    for t, k in feeds:
        for s, e in naps:
            if s <= t < e:
                t = s - timedelta(minutes=25)
                break
        adjusted.append((t, k))

    # Убираем дубли по минутам
    uniq = {}
    for t, k in adjusted:
        key = t.replace(second=0, microsecond=0)
        if key not in uniq:
            uniq[key] = (t, k)
    feeds = sorted(uniq.values(), key=lambda x: x[0])

    return {'feeds': feeds, 'naps': naps, 'window': (start_dt, night_start_dt)}

def shift_after_fact(plan: dict, fact_time: datetime, kind: str) -> dict:
    if kind not in ('feed', 'sleep_end'):
        return plan
    feeds = []
    shifted = False
    delta = None
    for t, k in plan.get('feeds', []):
        if not shifted and t > fact_time and kind == 'feed':
            delta = (fact_time - t)
            shifted = True
        if shifted and delta:
            t = t + delta
        feeds.append((t, k))
    plan['feeds'] = feeds
    return plan
