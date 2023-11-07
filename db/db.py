import time

import jsonpickle
import mysql.connector
from mysql.connector import MySQLConnection, CMySQLConnection
from mysql.connector.pooling import PooledMySQLConnection
from env_var import read_env_var
from typing import Union


class Database:
  conn: Union[PooledMySQLConnection, MySQLConnection, CMySQLConnection] = None

  def setup(self):
    serializedDbCfg = ''
    with open('./db/db.json', 'r', encoding='utf-8') as f:
      serializedDbCfg += f.read()
    dbConfig = jsonpickle.decode(serializedDbCfg)

    resolvedUsername = read_env_var(dbConfig["user"])
    resolvedPassword = read_env_var(dbConfig["password"])

    self.__create_init_db(dbConfig, resolvedUsername, resolvedPassword)
    # it would be a better idea to await the transaction instead of sleeping the main thread
    time.sleep(2)
    self.conn = mysql.connector.connect(
      host=dbConfig["host"],
      user=resolvedUsername,
      password=resolvedPassword,
      database=dbConfig["database"]
    )

  def teardown(self):
    if self.conn is None:
      raise ValueError('Connection is not configured!')
    self.conn.close()

  def __create_init_db(self, dbConfig, resolvedUsername: str, resolvedPassword: str):
    initConn = mysql.connector.connect(
      host=dbConfig["host"],
      user=resolvedUsername,
      password=resolvedPassword
    )
    print('Creating sample database')
    initSql = ''
    with open('./db/create_db_with_sample_data.sql', 'r', encoding='utf-8') as f:
      initSql += f.read()
    cursor = initConn.cursor()
    cursor.execute(initSql, multi=True)
    print('Sample database created successfully')
    initConn.close()
