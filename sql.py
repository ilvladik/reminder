import sqlite3

DATASOURCE = "db.sqlite3"


def __doquery(sql: str, params=()):
    try:
        with sqlite3.connect(DATASOURCE) as conn:
            cursor = conn.execute(sql, params)
            conn.commit()
            return cursor.fetchall()
    except sqlite3.OperationalError:
        raise ValueError


def __doqueries(sql: str):
    try:
        with sqlite3.connect(DATASOURCE) as conn:
            cursor = conn.executescript(sql)
            conn.commit()
            return cursor.fetchall()
    except sqlite3.OperationalError:
        raise ValueError


def create_db():
    script = """
    CREATE TABLE IF NOT EXISTS `chats` (
        `chat_id` varchar(20) PRIMARY KEY,
        `offset` varchar(10) NOT NULL
    );
    CREATE TABLE IF NOT EXISTS `calendars` (
        `calendar_id` varchar(200) PRIMARY KEY
    );
    CREATE TABLE IF NOT EXISTS `chat_cal` (
        `chat_id` varchar(20) NOT NULL,
        `calendar_id` varchar(200) NOT NULL,
        CONSTRAINT `fk_chat_cal_chats` FOREIGN KEY (`chat_id`)
        REFERENCES `chats` (`chat_id`) ON UPDATE CASCADE,
        CONSTRAINT `fk_chat_cal_calendars` FOREIGN KEY (`calendar_id`)
        REFERENCES `calendars` (`calendar_id`) ON UPDATE CASCADE
        CONSTRAINT pk_chat_calendar PRIMARY KEY (`chat_id`, `calendar_id`)
    );
    """
    __doqueries(script)


def clear():
    script = """
        DROP TABLE IF EXISTS `chats`;
        DROP TABLE IF EXISTS `calendars`;
        DROP TABLE IF EXISTS `chat_cal`;
    """
    __doqueries(script)


def add_chat(chat_id: str, offset: str):
    __doquery(
        "INSERT OR IGNORE INTO `chats` VALUES (?, ?);",
        (chat_id, offset),
    )


def add_calendar(link: str):
    __doquery("INSERT OR IGNORE INTO `calendars` VALUES (?);", (link,))


def add_calendar_in_chat(chat_id: str, link: str):
    __doquery(
        "INSERT OR IGNORE INTO `chat_cal` VALUES (?, ?)", (chat_id, link)
    )


def del_calendar_from_chat(chat_id: str, link: str):
    __doquery(
        "DELETE FROM `chat_cal` WHERE `chat_id` = ? AND `calendar_id` = ?",
        (chat_id, link),
    )
