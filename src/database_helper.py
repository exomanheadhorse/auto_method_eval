import pymysql
import logging

class DatabaseHelper(object):
    def __init__(self, **kwargs) -> None:
        self.host = kwargs.get("host", "localhost")
        self.user = kwargs.get("user", "tvm")
        self.passwd = kwargs.get("password", "")
        self.database = kwargs.get("database", "tvm_oss")
        self.port = kwargs.get("port", 3306)
        self.db = None
        self.connect()

    def connect(self):
        self.db = pymysql.connect(host=self.host, user=self.user, passwd=self.passwd, 
                                  db=self.database, port=self.port, charset='utf8')

    def ping(self):
        try:
            self.db.ping()
            self.db.commit()
        except Exception as e:
            try:
                self.db.ping(True)
                self.db.commit()
            except Exception as e:
                self.connect()
    
    def escape_string(self, s) -> str:
        if isinstance(s, str):
            ret = self.db.escape_string(s)
        else:
            ret = ""
        return ret
    
    def insert_and_get_id(self, sql):
        self.ping()
        cursor = self.db.cursor()
        id = 0
        try:
            cursor.execute(sql)
            id = int(self.db.insert_id())
            self.db.commit()
        finally:
            cursor.close()
        return id
    
    def query(self, sql, args=None):
        self.ping()
        cursor = self.db.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute(sql, args)
            return cursor.fetchall()
        finally:
            cursor.close()

    def add(self, sql):
        self.ping()
        cursor = self.db.cursor()
        try:
            cursor.execute(sql)
            self.db.commit()
        finally:
            cursor.close()

    def update(self, sql, args=None):
        self.ping()
        cursor = self.db.cursor()
        affected = 0
        try:
            cursor.execute(sql, args)
            affected = cursor.rowcount
            self.db.commit
        finally:
            cursor.close()
        return affected
    
    def delete(self, sql, args=None):
        self.ping()
        cursor = self.db.cursor()
        affected = 0
        try:
            cursor.execute(sql)
            self.db.commit()
            affected = cursor.rowcount
        finally:
            cursor.close()
        return affected
    
    def insert(self, table, values):
        self.ping()
        cursor = self.db.cursor()
        try:
            fields = {}
            fields.update(values)
            insert_keys = fields.keys()

            insert_key_string = ', '.join([
                '`%s`' % key for key in insert_keys
            ])
            insert_value_string = ', '.join([
                '%%(%s)' % key for key in insert_keys
            ])

            sql = """
                insert into `%s`(%s)
                values (%s)
            """ % (
                table,
                insert_key_string, 
                insert_value_string,
            )
            cursor.execute(sql, fields)
            self.db.commit()
        finally:
            cursor.close()
    
    def insert_many(self, sql, dataArray):
        self.ping()
        cursor = self.db.cursor()
        try:
            cursor.executemany(sql, dataArray)
            self.db.commit()
        finally:
            cursor.close()
    
    def close(self):
        self.db.close()

    def exec_transaction(self, sql_list = list()):
        self.ping()
        cursor = self.db.cursor()
        try:
            for sql in sql_list:
                cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
        finally:
            cursor.close()