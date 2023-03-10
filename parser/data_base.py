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


class Collection_connect:
    def __init__(self):
        with psycopg2.connect(host=host, port=port, user=user, password=password, dbname=db_name) as self.db:
            self.cur = self.db.cursor()

    def get_topic_without_collection(self):
        self.cur.execute("SELECT id, notices, difficulty FROM topic WHERE in_collection = 0")
        return self.cur.fetchall()

    def get_collections(self):
        self.cur.execute("SELECT * FROM collections")
        return self.cur.fetchall()

    def create_collection(self, topic_id, notices, dif):
        self.cur.execute("INSERT INTO collections (notices, topic_id, dif) "
                         "VALUES (%s, %s, %s)", (notices, topic_id, dif))
        self.db.commit()

    def get_inc_collection(self, notices, dif):
        self.cur.execute("SELECT * FROM collections WHERE notices = %s AND dif = %s AND is_full = 0 LIMIT 1", (notices, dif))
        return self.cur.fetchone()

    def update_collection(self, id, topic_id):
        if len(topic_id.split('*')) < 10:
            self.cur.execute("UPDATE collections SET topic_id = %s WHERE id = %s", (topic_id, id))
        else:
            self.cur.execute("UPDATE collections SET topic_id = %s, is_full = 1 WHERE id = %s", (topic_id, id))
        self.db.commit()

    def set_topic_status(self, id):
        self.cur.execute("UPDATE topic SET in_collection = 1 WHERE id = %s", (id,))
        self.db.commit()

