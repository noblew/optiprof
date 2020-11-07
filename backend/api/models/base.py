import pymongo
import pymysql


class Database:
    def __init__(self):
        self.app = None
        self.driver = None
    
    def init_app(self, app, uri, user, password, sql=True):
        self.app = app
        self._uri = uri
        self._user = user
        self._password = password
        self._sql = sql
        self.connect()

    def connect(self):
        if self._sql:
            try:
                self.db_driver = pymysql.connect(
                    self._uri, 
                    user=self._user, 
                    port=3306, 
                    password=self._password,
                    database="optiprof"
                )
            except:
                # if the database doesn't exist yet, connect to base RDS 'console'
                self.db_driver = pymysql.connect(
                    self._uri, 
                    user=self._user, 
                    port=3306, 
                    password=self._password,
                ) 
        else:
            self.db_driver = pymongo.MongoClient(
                "mongodb+srv://{}:{}@cluster0.m7ssr.mongodb.net/".format(
                    self._user,
                    self._password
                )
            )

        return self.db_driver

    def get_db(self):
        if not self.db_driver:
            return self.connect()
        
        return self.db_driver

    def close(self):
        self.db_driver.close()

mongo_db = Database()
sql_db = Database()