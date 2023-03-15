from icalendar import Calendar
import requests


def get_events(url):
    calendar = get_calendar_by_url(url)
    return calendar.walk('VEVENT')


def get_calendar_by_url(url):
    request = requests.get(url)
    calendar = Calendar.from_ical(request.text)
    return calendar
