from rethinkdb import RethinkDB
from config import APP_CONFIG

class DB():
    def __init__(self):
        self.dbname = APP_CONFIG['DB']['DB_NAME']
        self.tbmovie= 'movies'

        self.r = RethinkDB()
        try:
            self.conn = self.r.connect(
                host=APP_CONFIG['DB']['DB_HOST'],
                db=APP_CONFIG['DB']['DB_NAME'],
                user=APP_CONFIG['DB']['DB_USER'],
                password=APP_CONFIG['DB']['DB_PASS'],
                port=APP_CONFIG['DB']['DB_PORT']
            )
            self.create_db()
        except Exception as ex:
            print('DB_ERROR', ex )

    def create_db(self):
        if not self.r.db_list().contains(self.dbname).run(self.conn):
            self.r.db_create(self.dbname).run(self.conn)
            
    def create_table(self):
        if not self.r.db(self.dbname).table_list().contains(self.tbmovie).run(self.conn):
            self.r.db(self.dbname).table_create(self.tbmovie).run(self.conn)

    def get_conn(self):
        return self.conn
    
    def get_r(self):
        return self.r