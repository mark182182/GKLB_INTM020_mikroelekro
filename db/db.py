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

    self.conn = mysql.connector.connect(
      host=dbConfig["host"],
      user=resolvedUsername,
      password=resolvedPassword,
      database=dbConfig["database"]
    )

  def teardown(self):
    if (self.conn == None):
      raise ValueError('Connection is not configured!')
    self.conn.close()
