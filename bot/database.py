import psycopg2
import db_settings as db

host = db.host
port = db.port
user = db.user
password = db.password
db_name = db.db_name


class Bot_connection:
    def __init__(self):
        with psycopg2.connect(host=host, port=port, user=user, password=password, dbname=db_name) as self.db:
            self.cur = self.db.cursor()

    def get_data(self, notices, difficulty):
        self.cur.execute("SELECT * FROM topic WHERE difficulty = %s and notices = %s LIMIT 10", (difficulty, notices))
        return self.cur.fetchall()

    def get_all_notices(self):
        self.cur.execute("SELECT DISTINCT(notices) FROM topic")
        return self.cur.fetchall()

    def get_dif(self, notices):
        self.cur.execute("SELECT DISTINCT(difficulty) FROM topic WHERE notices = %s", (notices,))
        return self.cur.fetchall()



