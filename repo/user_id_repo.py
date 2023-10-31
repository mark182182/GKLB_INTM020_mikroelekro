from dao.user_id_dao import UserId
from db.db import Database


# Database queries related to the 'felhasznaloAzonosito' table
class UserIdRepository:
  __db: Database

  def __init__(self, db: Database):
    self.__db = db

  def get_userId_by_user(self, fhId: str) -> list[UserId]:
    cursor = self.__db.conn.cursor()

    cursor.execute("SELECT fhAzonId, fhId, rId, letiltva FROM belepteto.felhasznaloAzonosito WHERE fhId = %s", [fhId])

    results = cursor.fetchall()

    userIds: list[UserId] = []
    for row in results:
      fhAzonId = row[0]
      fhId = row[1]
      rId = row[2]
      letiltva = bool(row[3])
      userIds.append(UserId(fhAzonId, fhId, rId, letiltva))

    self.__db.conn.commit()
    cursor.close()
    return userIds

  def add_rfid_to_user(self, userIdDetails) -> UserId:
    cursor = self.__db.conn.cursor()

    cursor.execute("INSERT INTO belepteto.felhasznaloAzonosito VALUES (NULL, %s, %s, 0)",
                   [userIdDetails["fhId"], userIdDetails["rId"]])
    self.__db.conn.commit()

    cursor.execute("SELECT fhAzonId, fhId, rId, letiltva FROM belepteto.felhasznaloAzonosito ORDER BY rId DESC LIMIT 1")
    userId = self.__create_userId_from_results(cursor.fetchall())

    self.__db.conn.commit()
    cursor.close()

    return userId

  def update_lock_for_userId(self, userIdDetails) -> UserId:
    cursor = self.__db.conn.cursor()

    cursor.execute("UPDATE belepteto.felhasznaloAzonosito SET letiltva=%s WHERE fhId=%s AND rId=%s",
                   [userIdDetails["letiltva"], userIdDetails["fhId"], userIdDetails["rId"]])
    self.__db.conn.commit()

    cursor.execute("SELECT fhAzonId, fhId, rId, letiltva FROM belepteto.felhasznaloAzonosito WHERE fhId=%s AND rId=%s",
                   [userIdDetails["fhId"], userIdDetails["rId"]])
    userId = self.__create_userId_from_results(cursor.fetchall())

    self.__db.conn.commit()
    cursor.close()

    return userId

  def __create_userId_from_results(self, results):
    userId = None
    for row in results:
      fhAzonId = row[0]
      fhId = row[1]
      rId = row[2]
      letiltva = bool(row[3])
      userId = UserId(fhAzonId, fhId, rId, letiltva)
    return userId
