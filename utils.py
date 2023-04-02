from icalendar import Event
from dateutil import rrule
import datetime as dt
from pytz import tzinfo, timezone


LOCAL_TZ = timezone("Europe/Moscow")
PATTERN_DATETIME = "%Y-%m-%d %H:%M"


def get_alarms(
    event: Event, tz: tzinfo, start=dt.datetime.min, end=dt.datetime.max
):
    alarms = event.walk("VALARM")
    local_start_dt = (
        extend_event_dt(event, tz)[0].astimezone(LOCAL_TZ).replace(tzinfo=None)
    )
    return [
        local_start_dt + alarm.get("TRIGGER").dt
        for alarm in alarms
        if start <= local_start_dt + alarm.get("TRIGGER").dt < end
    ]


def get_message_text(event: Event, tz: tzinfo):
    event_dt = extend_event_dt(event, tz)

    start = event_dt[0].strftime(PATTERN_DATETIME)
    end = event_dt[1].strftime(PATTERN_DATETIME)
    summary = event.get("SUMMARY")
    description = (
        f'\nДополнительно:\n{event.get("DESCRIPTION")}'
        if event.get("DESCRIPTION") is not None
        else ""
    )
    message_text = f"🕰{start} - {end}\n{summary}{description}"
    return message_text


def extend_event_dt(event: Event, tz: tzinfo):
    start = event.get("DTSTART").dt
    end = event.get("DTEND").dt

    if isinstance(start, dt.datetime):
        start = start.astimezone(tz)
        end = end.astimezone(tz)
    else:
        start = tz.localize(dt.datetime.combine(start, dt.time.min))
        end = tz.localize(dt.datetime.combine(start, dt.time.max))

    if "RRULE" in event:
        difference = end - start
        rule_text = event["RRULE"].to_ical().decode()
        rule = rrule.rrulestr(rule_text, dtstart=start)
        start = rule.after(dt.datetime.now(tz=tz))
        end = start + difference
    return (start, end)
