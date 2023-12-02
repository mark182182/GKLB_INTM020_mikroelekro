from dto.user_dao import User
from db.db import Database


# Database queries related to the 'felhasznalok' table
class UserRepository:
  __db: Database

  def __init__(self, db: Database):
    self.__db = db

  def get_user_by_id(self, fhId: str) -> User:
    cursor = self.__db.conn.cursor()

    cursor.execute("SELECT fhId, fhNev FROM belepteto.felhasznalok WHERE fhId = %s", [fhId])
    existingUser = self.__create_user_from_results(cursor.fetchall())
    if existingUser is None:
      raise ValueError(f'User with id: {fhId} does not exist!')

    self.__db.conn.commit()
    cursor.close()
    return existingUser

  def get_users(self) -> list[User]:
    cursor = self.__db.conn.cursor()

    cursor.execute("SELECT fhId, fhNev FROM belepteto.felhasznalok")
    results = cursor.fetchall()

    users = []
    for row in results:
      fhId = row[0]
      fhNev = row[1]
      users.append(User(fhId, fhNev))

    self.__db.conn.commit()
    cursor.close()
    return users

  def create_user(self, userDetails: any) -> User:
    cursor = self.__db.conn.cursor()

    cursor.execute("INSERT INTO belepteto.felhasznalok VALUES (NULL, %s)", [userDetails["nev"]])
    self.__db.conn.commit()

    cursor.execute("SELECT fhId, fhNev FROM belepteto.felhasznalok ORDER BY fhid DESC LIMIT 1")
    user = self.__create_user_from_results(cursor.fetchall())

    self.__db.conn.commit()
    cursor.close()

    return user

  def update_user(self, userDetails: any) -> User:
    cursor = self.__db.conn.cursor()

    try:
      existingUser = self.get_user_by_id(userDetails["id"])
      if existingUser is None:
        raise ValueError(f'User with id: {userDetails["id"]} does not exist!')

      cursor.execute("UPDATE belepteto.felhasznalok SET fhNev=%s WHERE fhId=%s",
                     [userDetails["nev"], userDetails["id"]])
      self.__db.conn.commit()

      user = self.get_user_by_id(userDetails["id"])
      return user

    finally:
      self.__db.conn.commit()
      cursor.close()

  def delete_user(self, fhId: str):
    cursor = self.__db.conn.cursor()
    try:
      existingUser = self.get_user_by_id(fhId)
      if existingUser is None:
        raise ValueError(f'User with id: {fhId} does not exist!')
      cursor.execute("DELETE FROM belepteto.felhasznalok WHERE fhId=%s", [fhId])

    finally:
      self.__db.conn.commit()
      cursor.close()

  def __create_user_from_results(self, results) -> User:
    user = None
    for row in results:
      fhId = row[0]
      fhNev = row[1]
      user = User(fhId, fhNev)

    return user
