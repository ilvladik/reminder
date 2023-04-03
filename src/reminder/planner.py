from apscheduler.schedulers.background import BackgroundScheduler
from telebot import TeleBot
import sql.database as sql
from ical import network, format
import datetime as dt


sched = BackgroundScheduler({"apscheduler.timezone": "Europe/Moscow"})
HOURS = 1
FREQUENCY = dt.timedelta(hours=HOURS)


def start(bot: TeleBot):
    sched.add_job(
        schedule,
        "interval",
        [bot],
        hours=HOURS,
        next_run_time=dt.datetime.now(),
    )
    sched.start()


def schedule(bot: TeleBot):
    stdt = dt.datetime.now()
    endt = stdt + FREQUENCY
    propertys = sql.select_prop()
    for params in propertys:
        try:
            schedule_events(bot, params, stdt, endt)
        except ValueError:
            chat, *other, cal = params
            bot.send_message(
                chat,
                f"Произошла ошибка при работе с календарём по ссылке {cal}",
            )


def schedule_events(bot: TeleBot, params, stdt, endt):
    chat, offset, cal = params
    timezone = dt.datetime.strptime(
        f"12.00.00 {offset}", "%H.%M.%S %Z%z"
    ).tzinfo
    events = network.get_events(cal)
    for event in events:
        alarms = format.get_alarms(event, timezone, stdt, endt)
        message_text = format.get_message_text(event, timezone)

        def send():
            bot.send_message(chat, message_text)

        for alarm in alarms:
            sched.add_job(send, "date", run_date=alarm)
