import psycopg2
import db_settings as db

host = db.host
port = db.port
user = db.user
password = db.password
db_name = db.db_name


class Parser_connection:
    def __init__(self):
        with psycopg2.connect(host=host, port=port, user=user, password=password, dbname=db_name) as self.db:
            self.cur = self.db.cursor()

    def add_data_to_database(self, name, number, number_of_passes, notices, difficulty, url):
        self.cur.execute("INSERT INTO topic (name, number, number_of_passes, notices, difficulty, url)"
                         " VALUES (%s, %s, %s, %s, %s, %s)",
                         (name, number, number_of_passes, notices, difficulty, url))
        self.db.commit()

