import pymysql
import uuid
import os


class DirectorResource:

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
    def get_all(limit=None, offset=None):
        sql = "SELECT * FROM director_databases.director_table"
        if limit:
            sql += " limit " + str(limit)
        if offset:
            sql += " offset " + str(offset)
        conn = DirectorResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql)
        result = cur.fetchall()
        return result

    @staticmethod
    def get_by_template(field_list, template, limit=None, offset=None):
        sql = "select " \
              + ",".join(field_list) \
              + " from director_databases.director_table where " \
              + " and ".join(["%s = '%s'" % (key, val) if not type(val) == int
                              else "%s = %s" % (key, val)
                              for (key, val) in template.items()])
        if limit:
            sql += " limit " + str(limit)
        if offset:
            sql += " offset " + str(offset)

        conn = DirectorResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql)
        result = cur.fetchall()
        return result

    @staticmethod
    def create_director(first_name, middle_name, last_name, gender, birth_year, birth_month, birth_day):
        guid = str(uuid.uuid4())
        sql = "INSERT INTO director_databases.director_table(guid, first_name, middle_name, \
        last_name, gender, birth_year, birth_month, birth_day) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
        conn = DirectorResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, (guid, first_name, middle_name, last_name, gender, birth_year, birth_month, birth_day))
        return res

    @staticmethod
    def update_director(guid, first_name, middle_name, last_name, gender, birth_year, birth_month, birth_day):
        sql = "UPDATE director_databases.director_table SET first_name=%s, middle_name=%s, last_name=%s, gender=%s, \
        birth_year=%s, birth_month=%s, birth_day=%s WHERE guid=%s"
        conn = DirectorResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, (first_name, middle_name, last_name, gender, birth_year, birth_month, birth_day, guid))
        return res

    @staticmethod
    def delete_director(guid):
        sql = "DELETE FROM director_databases.director_table WHERE guid=%s"
        conn = DirectorResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, guid)
        return res
