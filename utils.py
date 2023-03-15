from icalendar import Event
from dateutil import rrule
import datetime as dt
from pytz import tzinfo, timezone


local_timezone = timezone('Europe/Moscow')


def get_alarms(event: Event, tz: tzinfo, start=dt.datetime.min, end=dt.datetime.max):
    alarms = event.walk('VALARM')
    try:
        datetime = extend_event_datetime(event, tz) \
            .get('DTSTART') \
            .astimezone(local_timezone) \
            .replace(tzinfo=None)
    except ValueError:
        return []
    return [datetime + alarm.get("TRIGGER").dt for alarm in alarms
            if start <= datetime + alarm.get("TRIGGER").dt < end]


def get_message_text(event: Event, tz: tzinfo):
    try:
        event_dates = extend_event_datetime(event, tz)
    except ValueError:
        return ''
    format_datetime = "%Y-%m-%d %H:%M"
    start = event_dates.get("DTSTART").strftime(format_datetime)
    end = event_dates.get("DTEND").strftime(format_datetime)
    description = f'\nДополнительно:\n{event.get("DESCRIPTION")}' \
        if event.get('DESCRIPTION') is not None else ''
    message_text = f'🕰{start} - {end}\n' \
                   f'{event.get("SUMMARY")}' \
                   f'{description}'
    return message_text


def extend_event_datetime(event: Event, tz: tzinfo):
    start = event.get('DTSTART').dt
    end = event.get('DTEND').dt

    if isinstance(start, dt.datetime):
        start = start.astimezone(tz)
        end = end.astimezone(tz)
    else:
        start = tz.localize(dt.datetime.combine(start, dt.time.min))
        end = tz.localize(dt.datetime.combine(start, dt.time.max))

    if 'RRULE' in event:
        difference = end - start
        rule_text = event['RRULE'].to_ical().decode()
        rule = rrule.rrulestr(rule_text, dtstart=start)
        start = rule.after(dt.datetime.now(tz=tz))
        end = start + difference
    return {'DTSTART': start, 'DTEND': end}
