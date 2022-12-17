import pymysql

import os


class directorResource:

    def __int__(self):
        pass

    @staticmethod
    def _get_connection():

        usr = 'admin'
        pw = '12345678'
        h = 'directordb.chtcseno515m.us-east-1.rds.amazonaws.com'

        conn = pymysql.connect(
            user=usr,
            port=3306,
            password=pw,
            host=h,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        return conn

    @staticmethod
    def get_by_key(key):
        conn = directorResource._get_connection()
        sql = "SELECT * FROM director_databases.director_table where guid=%s";
        cur = conn.cursor()
        res = cur.execute(sql, args=key)
        result = cur.fetchone()

        return result

    @staticmethod
    def get_all():
        sql = "SELECT * FROM director_databases.director_table";
        conn = directorResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql)
        result = cur.fetchall()
        return result


    @staticmethod
    def add_director(first_name, middle_name, last_name, gender, birth_year, birth_month, birth_day):
        guid = str(uuid.uuid4())
        sql = " INSERT INTO director_databases.director_table(first_name, middle_name, \
        last_name, gender, birth_year, birth_month, birth_day) VALUES(%s,%s,%s,%s,%s,%s,%s) "
        conn = directorResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, (guid, first_name, middle_name, last_name, gender, birth_year, birth_month, birth_day))
        result = cur.fetchone()
        return result

    @staticmethod
    def update_director(column, new_val):
        sql = "UPDATE director_databases.director_table SET %s=%s WHERE %s=%s"
        conn = directorResource._get_connection()
        cur = conn.cursor()
        result = cur.fetchone()
        return result

    @staticmethod
    def delete_director(column, condition):
        sql = "DELETE FROM director_databases.director_table WHERE %s=%s "
        conn = directorResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, column, condition)
        result = cur.fetchone()
        return result