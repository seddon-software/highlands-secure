############################################################
#
#    Highlands Server
#
#    © Highlands Negotiations, June 2018, v0.5
#
############################################################

import pymysql.cursors, sys, os
import pandas as pd


def execute(connection, sql):
    # connection is not autocommit by default. So you must commit to save your changes.
    try:
        with connection.cursor() as cursor:
            pymysql.cursors.Cursor._defer_warnings = True

            cursor.execute(sql)
        connection.commit()    
    finally:
        connection.close()
        

def connect(user, password, database=""):
    connection = pymysql.connect(host='localhost',
                                 user=user,
                                 password=password,
                                 db=database,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection

def printTable(manager, managerPassword, database, table):
    connection = connect(manager, managerPassword, database)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT `*` FROM `{}`".format(table)
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                print(row)
    finally:
        connection.close()

def getNamesAndPasswords():
    pd.set_option('display.width', 1000)
    table = pd.read_excel(excelFile, 'setup')
    rootFrame = table[(table.TYPE == "user") & (table.NAME == "root")]
    managerFrame = table[(table.TYPE == "user") & (table.NAME == "manager")]
    databaseFrame = table[table.TYPE == "database"]
    usersFrame = table[table.TYPE == "users"]

    root = rootFrame["NAME"].tolist()[0]
    rootPassword = rootFrame["OPTION"].tolist()[0]
    manager = managerFrame["NAME"].tolist()[0]
    managerPassword = managerFrame["OPTION"].tolist()[0]
    database = databaseFrame["NAME"].tolist()[0]
    table = databaseFrame["OPTION"].tolist()[0]
    usersTable = usersFrame["OPTION"].tolist()[0]

    return [root, rootPassword, manager, managerPassword, database, table, usersTable]

def createDatabase(root, rootPassword, database):
    connection = connect(root, rootPassword)
    sql = "CREATE DATABASE IF NOT EXISTS {}".format(database)
    execute(connection, sql)

def createManagerUser(root, rootPassword, manager, managerPassword):
    connection = connect(root, rootPassword)
    sql = "CREATE USER IF NOT EXISTS '{}'@'localhost' IDENTIFIED BY '{}'".format(manager, managerPassword)
    execute(connection, sql)

def grantPrivilegesToManager(root, rootPassword, manager, database):
    connection = connect(root, rootPassword, database)
    sql = "GRANT ALL PRIVILEGES ON {}.* TO '{}'@'localhost'".format(database, manager)
    execute(connection, sql)
    
def dropTable(table, manager, managerPassword, database):
    connection = connect(manager, managerPassword, database)
    sql = "DROP TABLE IF EXISTS {}".format(table)
    execute(connection, sql)

def createTable(table, manager, managerPassword, database):
    connection = connect(manager, managerPassword, database)
    sql = """CREATE TABLE IF NOT EXISTS {} (
        id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        guid VARCHAR(36) NOT NULL,
        timestamp TIMESTAMP NOT NULL,
        email VARCHAR(40) NOT NULL,
        headers VARCHAR(1000) NOT NULL,
        result VARCHAR(5000) NOT NULL
        )""".format(table)
    execute(connection, sql)

def createUsersTable(table, manager, managerPassword, database):
    connection = connect(manager, managerPassword, database)
    sql = """CREATE TABLE IF NOT EXISTS {} (
        email VARCHAR(40) NOT NULL,
        password VARCHAR(40),
        code VARCHAR(20),
        PRIMARY KEY (`email`)
        )""".format(table)
    execute(connection, sql)

def showTables(user, password, database):
    connection = connect(user, password, database)
    try:
        with connection.cursor() as cursor:
            sql = "SHOW TABLES"
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results: print(row)
    finally:
        connection.close()

def showUsers(user, password, database):
    connection = connect(user, password, database)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT user FROM mysql.user GROUP BY user"
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results: print(row)
    finally:
        connection.close()

def parseCommandLine():
    # default excel file is "highlands.xlsx", but can be changed on command line:
    #    python server.py [excel-file]
    if len(sys.argv) > 2:
        print("Useage: python server.py [excel-file]")
        sys.exit()
    if len(sys.argv) == 1:
        excelFile = "highlands.xlsx"
    else:
        excelFile = sys.argv[1].replace(".xlsx", "") + ".xlsx"
    
    if not os.path.isfile(excelFile):
        print("{} does not exist".format(excelFile))
        sys.exit()

    return excelFile

if __name__ == "__main__":
    global excelFile
    excelFile = parseCommandLine()
    root, rootPassword, manager, managerPassword, database, table, usersTable = getNamesAndPasswords()
    createDatabase(root, rootPassword, database)
    createManagerUser(root, rootPassword, manager, managerPassword)
    grantPrivilegesToManager(root, rootPassword, manager, database)
    dropTable(table, manager, managerPassword, database)
    dropTable(usersTable, manager, managerPassword, database)
    createTable(table, manager, managerPassword, database)
    createUsersTable(usersTable, manager, managerPassword, database)
    showTables(manager, managerPassword, database)
    showUsers(root, rootPassword, database)
#    printTable(manager, managerPassword, database, table)
