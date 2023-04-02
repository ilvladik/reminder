from icalendar import Calendar
import requests


def get_events(url: str):
    """Calendar's url: str -> list of events"""
    calendar = get_calendar_by_url(url)
    return calendar.walk("VEVENT")


def get_calendar_by_url(url: str):
    """Calendar's url: str -> object of Calendar class from icalendar lib"""
    request = requests.get(url)
    calendar = Calendar.from_ical(request.text)
    return calendar
