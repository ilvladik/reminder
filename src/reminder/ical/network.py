from icalendar import Calendar
import requests


def get_events(url: str):
    """Calendar's url: str -> list of events"""
    try:
        calendar = get_calendar_by_url(url)
        return calendar.walk("VEVENT")
    except Exception:
        ValueError


def get_calendar_by_url(url: str):
    """Calendar's url: str -> object of Calendar class from icalendar lib"""
    try:
        request = requests.get(url)
        calendar = Calendar.from_ical(request.text)
        return calendar
    except Exception:
        raise ValueError
