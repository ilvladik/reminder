from icalendar import Event
from dateutil import rrule
import datetime as dt

LOCAL_TZ = dt.timezone(dt.timedelta(hours=3))
PATTERN_DATETIME = "%Y-%m-%d %H:%M"


def get_alarms(
    event: Event, tz: dt.timezone, min: dt.datetime, max: dt.datetime
):
    alarms = event.walk("VALARM")
    stdt = extend_event(event, tz)[0].astimezone(LOCAL_TZ).replace(tzinfo=None)
    return [
        stdt + alarm.get("TRIGGER").dt
        for alarm in alarms
        if min <= stdt + alarm.get("TRIGGER").dt < max
    ]


def get_message_text(event: Event, tz: dt.timezone):
    dates = extend_event(event, tz)
    stdt = dates[0].strftime(PATTERN_DATETIME)
    endt = dates[1].strftime(PATTERN_DATETIME)
    summary = event.get("SUMMARY")
    description = (
        f'\nДополнительно:\n{event.get("DESCRIPTION")}'
        if event.get("DESCRIPTION") is not None
        else ""
    )
    message_text = f"🕙{stdt} - {endt}\n{summary}{description}"
    return message_text


def extend_event(event: Event, tz: dt.timezone):
    stdt = event.get("DTSTART").dt
    endt = event.get("DTEND").dt
    if not isinstance(stdt, dt.datetime):
        stdt = dt.datetime.combine(stdt, dt.time.min)
        endt = dt.datetime.combine(stdt, dt.time.max)
    if "RRULE" in event:
        stdt, endt = apply_rrule(stdt, endt, event["RRULE"].to_ical().decode())
    stdt = stdt.astimezone(tz)
    endt = endt.astimezone(tz)
    return (stdt, endt)


def apply_rrule(stdt: dt.datetime, endt: dt.datetime, rule: str):
    difference = endt - stdt
    rule = rrule.rrulestr(rule, dtstart=stdt)
    now = (
        dt.datetime.now()
        if stdt.tzinfo is None
        else dt.datetime.now(stdt.tzinfo)
    )
    if rule.after(now) is None:
        stdt = dt.datetime.now().replace(year=1990)
        endt = dt.datetime.now().replace(year=1990)
    else:
        stdt = rule.after(now)
        endt = stdt + difference
    return (stdt, endt)
