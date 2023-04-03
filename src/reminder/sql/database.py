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
        `cal_id` varchar(200) PRIMARY KEY
    );
    CREATE TABLE IF NOT EXISTS `property` (
        `chat_id` varchar(20) NOT NULL,
        `cal_id` varchar(200) NOT NULL,
        CONSTRAINT `fk_property_chats` FOREIGN KEY (`chat_id`)
        REFERENCES `chats` (`chat_id`) ON UPDATE CASCADE,
        CONSTRAINT `fk_property_calendars` FOREIGN KEY (`cal_id`)
        REFERENCES `calendars` (`cal_id`) ON UPDATE CASCADE
        CONSTRAINT pk_chat_cal PRIMARY KEY (`chat_id`, `cal_id`)
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


def select_tz(chat_id: str):
    return __doquery(
        "SELECT `offset` FROM `chats` WHERE `chat_id` = ?", (chat_id,)
    )[0][0]


def select_cal(chat_id: str):
    return [
        element[0]
        for element in __doquery(
            "SELECT `cal_id` FROM `property` WHERE `chat_id` = ?",
            (chat_id,),
        )
    ]


def select_prop():
    return __doquery(
        """
        SELECT property.chat_id, chats.offset, property.cal_id
        FROM `property` INNER JOIN `chats`
        ON (property.chat_id = chats.chat_id);
        """
    )


def insert_chat(chat_id: str, offset: str):
    __doquery(
        "INSERT OR IGNORE INTO `chats` VALUES (?, ?);",
        (chat_id, offset),
    )


def insert_cal(cal_id: str):
    __doquery("INSERT OR IGNORE INTO `calendars` VALUES (?);", (cal_id,))


def insert_prop(chat_id: str, cal_id: str):
    return __doquery(
        "INSERT OR IGNORE INTO `property` VALUES (?, ?)", (chat_id, cal_id)
    )


def update_offset(chat_id: str, offset: str):
    __doquery(
        "UPDATE `chats` SET `offset` = ? WHERE `chat_id` = ?",
        (offset, chat_id),
    )


def delete_prop(chat_id: str, cal_id: str):
    __doquery(
        "DELETE FROM `property` WHERE `chat_id` = ? AND `cal_id` = ?",
        (chat_id, cal_id),
    )
