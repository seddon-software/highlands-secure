import pymysql.cursors
import os
from myglobals import MyGlobals

if __name__ == "__main__": os.chdir("..")

g = MyGlobals()

class Database:
    def __init__(self):
        pass
    
    def connect(self):
        connection = pymysql.connect(host='localhost',
                                     user=g.get("manager"),
                                     password=g.get("managerPassword"),
                                     db=g.get("database"),
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        return connection

    def getDatabaseResults(self):
        connection = self.connect()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT `*` FROM `{}`".format(g.get("table"))
                cursor.execute(sql)
                results = cursor.fetchall()
        finally:
            connection.close()
        return results

    def createUser(self, email, password, code):
        # This routine will create a user if it doesn't exist or update the user otherwise
        connection = self.connect()
        try:
            with connection.cursor() as cursor:
                try:
                    sql = """REPLACE INTO {} SET email = '{}', password = '{}', code = '{}'
                    """.format(g.get("usersTable"), email, password, code)
                    cursor.execute(sql)
                    connection.commit()
                except Exception as e:
                    connection.rollback()
                    print(e)
        finally:
            connection.close()

    def getPassword(self, email):
        connection = self.connect()
        try:
            with connection.cursor() as cursor:
                try:
                    sql = """SELECT password FROM {} WHERE email = '{}'
                    """.format(g.get("usersTable"), email)
                    cursor.execute(sql)
                    result = cursor.fetchone()
                    
                except Exception as e:
                    connection.rollback()
                    print(e)
        finally:
            connection.close()
        return result['password']

    def getCode(self, email):
        connection = self.connect()
        try:
            with connection.cursor() as cursor:
                try:
                    sql = """SELECT code FROM {} WHERE email = '{}'
                    """.format(g.get("usersTable"), email)
                    cursor.execute(sql)
                    result = cursor.fetchone()
                    
                except Exception as e:
                    connection.rollback()
                    print(e)
        finally:
            connection.close()
        return result['password']

    def getField(self, fieldName, fieldValue):
        connection = self.connect()
        try:
            with connection.cursor() as cursor:
                try:
                    sql = """SELECT code FROM {} WHERE email = '{}'
                    """.format(g.get("usersTable"), fieldName, fieldValue)
                    cursor.execute(sql)
                    result = cursor.fetchone()
                    
                except Exception as e:
                    connection.rollback()
                    print(e)
        finally:
            connection.close()
        return result['password']

    def printUsers(self):
        connection = self.connect()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT `*` FROM `{}`".format(g.get("usersTable"))
                cursor.execute(sql)
                results = cursor.fetchall()
                for result in results:
                    print(result)
        finally:
            connection.close()

if __name__ == "__main__": 
    db = Database()
    print(g.get("usersTable"))
    db.createUser("John", "Highway", "123")
    db.createUser("John", "Highways", "123")
    db.createUser("Peter", "S", "123")
    db.createUser("Peter", "Smith", "456")
    print(db.getPassword("John"))
    db.printUsers()
    
    