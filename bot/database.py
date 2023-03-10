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

    def get_data(self, id, difficulty):
        self.cur.execute("SELECT notices FROM collections WHERE id = %s", (id,))
        notices = self.cur.fetchone()[0]
        self.cur.execute("SELECT * FROM collections WHERE dif = %s and notices = %s", (difficulty, notices))
        return self.cur.fetchall()

    def get_all_notices(self):
        self.cur.execute("SELECT notices, id FROM collections")
        return self.cur.fetchall()

    def get_dif(self, id):
        self.cur.execute("SELECT notices FROM collections WHERE id = %s", (id,))
        notices = self.cur.fetchone()[0]
        self.cur.execute("SELECT DISTINCT(dif) FROM collections WHERE notices = %s ORDER BY dif", (notices,))
        return self.cur.fetchall()

    def get_collection_info(self, id):
        self.cur.execute("SELECT * FROM collections WHERE id = %s", (id,))
        return self.cur.fetchone()

    def get_topic_info(self, id):
        self.cur.execute("SELECT * FROM topic WHERE id = %s", (id,))
        return self.cur.fetchone()



