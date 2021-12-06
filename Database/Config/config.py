import os
from pymysql import connect, cursors
from Logger.logger import Logger

logger = Logger('logs', 'config_logger.txt')

try:
    connection = connect(
        host = 'localhost', 
        user = 'root', 
        password = 'Annieleo1!', 
        charset = 'utf8mb4', 
        cursorclass = cursors.DictCursor
    )
    cursor = connection.cursor()
    cursor.execute('CREATE DATABASE IF NOT EXISTS BrokerBase')
    cursor.close()
    connection.close()

    path = os.path.join('Database', 'AccKeys')
    if not os.path.isdir(path):
        os.mkdir(path)

except Exception as error:
    logger.write(f'Cannot create database with error {error}')

