import time

import mysql.connector
from mysql.connector import MySQLConnection, CMySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

from app import config
from env_var import read_env_var
from typing import Union


class Database:
  conn: Union[PooledMySQLConnection, MySQLConnection, CMySQLConnection] = None

  def setup(self):
    resolvedUsername = read_env_var(config.get_content()['mysql']['User'])
    resolvedPassword = read_env_var(config.get_content()['mysql']['Password'])

    self.__create_init_db(resolvedUsername, resolvedPassword)
    # it would be a better idea to await the transaction instead of sleeping the main thread
    time.sleep(2)
    self.conn = mysql.connector.connect(
      host=config.get_content()["host"],
      user=resolvedUsername,
      password=resolvedPassword,
      database=config.get_content()["database"]
    )

  def teardown(self):
    if self.conn is None:
      raise ValueError('Connection is not configured!')
    self.conn.close()

  def __create_init_db(self, resolvedUsername: str, resolvedPassword: str):
    initConn = mysql.connector.connect(
      host=config.get_content()["host"],
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
