import jsonpickle
import mysql.connector
from mysql.connector import MySQLConnection, CMySQLConnection
from mysql.connector.pooling import PooledMySQLConnection
from env_var import read_env_var
from typing import Union

from user import User


class Database:
  conn: Union[PooledMySQLConnection, MySQLConnection, CMySQLConnection] = None

  def setup(self):
    serializedDbCfg = ''
    with open('db.json', 'r', encoding='utf-8') as f:
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

  def get_user_by_id(self, fhId: str) -> User:
    cursor = self.conn.cursor()

    cursor.execute("SELECT fhId, fhNev FROM belepteto.felhasznalok WHERE fhId = %s", [fhId])
    existingUser = self.__create_user_from_results(cursor.fetchall())
    if existingUser is None:
      raise ValueError(f'User with id: {fhId} does not exist!')

    self.conn.commit()
    cursor.close()
    return existingUser

  def get_users(self) -> list[User]:
    cursor = self.conn.cursor()

    cursor.execute("SELECT fhId, fhNev FROM belepteto.felhasznalok")
    results = cursor.fetchall()

    users = []
    for row in results:
      fhId = row[0]
      fhNev = row[1]
      user = User()
      user.fhId = fhId
      user.fhNev = fhNev
      users.append(user)

    self.conn.commit()
    cursor.close()
    return users

  def create_user(self, userDetails: any) -> User:
    cursor = self.conn.cursor()

    cursor.execute("INSERT INTO belepteto.felhasznalok VALUES (NULL, %s)", [userDetails["nev"]])
    self.conn.commit()

    cursor.execute("SELECT fhId, fhNev FROM belepteto.felhasznalok ORDER BY fhid DESC LIMIT 1")
    user = self.__create_user_from_results(cursor.fetchall())

    self.conn.commit()
    cursor.close()

    return user

  def update_user(self, userDetails: any) -> User:
    cursor = self.conn.cursor()

    try:
      existingUser = self.get_user_by_id(userDetails["id"])
      if existingUser is None:
        raise ValueError(f'User with id: {userDetails["id"]} does not exist!')

      cursor.execute("UPDATE belepteto.felhasznalok SET fhNev=%s WHERE fhId=%s",
                     [userDetails["nev"], userDetails["id"]])
      self.conn.commit()

      user = self.get_user_by_id(userDetails["id"])
      return user

    finally:
      self.conn.commit()
      cursor.close()

  def delete_user(self, fhId: str):
    cursor = self.conn.cursor()
    try:
      existingUser = self.get_user_by_id(fhId)
      if existingUser is None:
        raise ValueError(f'User with id: {fhId} does not exist!')
      cursor.execute("DELETE FROM belepteto.felhasznalok WHERE fhId=%s", [fhId])

    finally:
      self.conn.commit()
      cursor.close()

  def __create_user_from_results(self, results) -> User:
    user = None
    for row in results:
      user = User()
      fhId = row[0]
      fhNev = row[1]
      user = User()
      user.fhId = fhId
      user.fhNev = fhNev

    return user
