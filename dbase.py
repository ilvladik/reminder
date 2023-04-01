import psycopg2
from psycopg2.extras import DictCursor

db_name = 'postgres'
user = 'postgres'
password = ''
host = ''
def select_call(call):
    if call[-1] != ';':
        call += ';'
    conn = psycopg2.connect(dbname=db_name, user=user,
                            password=password, host=host)
    cursor = conn.cursor(cursor_factory=DictCursor)
    cursor.execute(call)
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return records

def insert_call(call):
    if call[-1] != ';':
        call += ';'
    conn = psycopg2.connect(dbname=db_name, user=user,
                            password=password, host=host)
    cursor = conn.cursor(cursor_factory=DictCursor)
    cursor.execute(call)
    conn.commit()
    cursor.close()
    conn.close()


def update_call(call, values):
    if call[-1] != ';':
        call += ';'
    conn = psycopg2.connect(dbname=db_name, user=user,
                            password=password, host=host)
    cursor = conn.cursor(cursor_factory=DictCursor)
    cursor.execute(call, values)
    conn.commit()
    cursor.close()
    conn.close()

def delete_call(call):
    conn = psycopg2.connect(dbname=db_name, user=user,
                            password=password, host=host)
    cursor = conn.cursor(cursor_factory=DictCursor)
    cursor.execute(call)
    conn.commit()
    cursor.close()
    conn.close()


def clear():
    conn = psycopg2.connect(dbname=db_name, user=user,
                            password=password, host=host)
    cursor = conn.cursor(cursor_factory=DictCursor)
    delete_call("DELETE FROM users;")
    delete_call("DELETE FROM student_of;")
    delete_call("DELETE FROM pending_payments;")
    delete_call("DELETE FROM month_payment;")
    delete_call("DELETE FROM one_class_payment;")
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    print(select_call("SELECT * FROM users;"))


