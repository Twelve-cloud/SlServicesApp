from pymysql import connect, cursors

try:
    connection = connect(host = 'localhost', user = 'root', password = 'Annieleo1!', charset = 'utf8mb4', cursorclass = cursors.DictCursor)
    cursor = connection.cursor()
    cursor.execute('CREATE DATABASE IF NOT EXISTS BrokerBase')
except Exception as error:
    #logger
finally:
    cursor.close()
    connection.close();

