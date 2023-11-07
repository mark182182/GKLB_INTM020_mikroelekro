from dao.rfid_dao import Rfid
from dao.user_id_dao import UserId
from db.db import Database
from repo.rfid_repo import RfidRepository


# Database queries related to the 'felhasznaloAzonosito' table
class UserIdRepository:
  __db: Database

  def __init__(self, db: Database, rfId: RfidRepository):
    self.__db = db
    self.__rfidRepo = rfId

  def get_userId_by_user(self, fhId: str) -> list[UserId]:
    cursor = self.__db.conn.cursor()

    cursor.execute("""SELECT fhAzonId, fhId, rf.rId, rf.rErtek, letiltva FROM belepteto.felhasznaloAzonosito as fa
    INNER JOIN belepteto.rfid as rf
    ON fa.rId = rf.rId
    WHERE fhId = %s""", [fhId])

    results = cursor.fetchall()

    userIds: list[UserId] = []
    for row in results:
      fhAzonId = row[0]
      fhId = row[1]
      rId = row[2]
      rErtek = row[3]
      letiltva = bool(row[4])
      userIds.append(UserId(fhAzonId, fhId, rId, rErtek, letiltva))

    self.__db.conn.commit()
    cursor.close()
    return userIds

  def get_userId_by_rErtek(self, rErtek: str) -> UserId:
    cursor = self.__db.conn.cursor()

    cursor.execute("""SELECT fhAzonId, fhId, rf.rId, rf.rErtek, letiltva FROM belepteto.felhasznaloAzonosito as fa
    INNER JOIN belepteto.rfid as rf
    ON fa.rId = rf.rId
    WHERE rErtek = %s
    """, [rErtek])

    userId = self.__create_userId_from_results(cursor.fetchall())

    if userId is None:
      raise ValueError(f'{rErtek} is not assigned to any user!')

    self.__db.conn.commit()
    cursor.close()
    return userId

  def add_rfid_to_user(self, userIdDetails) -> UserId:
    cursor = self.__db.conn.cursor()

    existingRfid: Rfid = self.__rfidRepo.get_rfid_by_value(userIdDetails["rErtek"])

    cursor.execute("INSERT INTO belepteto.felhasznaloAzonosito VALUES (NULL, %s, %s, 0)",
                   [userIdDetails["fhId"], existingRfid.get_rid()])
    self.__db.conn.commit()

    cursor.execute(
      """SELECT fhAzonId, fhId, rf.rId, rf.rErtek, letiltva FROM belepteto.felhasznaloAzonosito as fa
      INNER JOIN belepteto.rfid as rf
      ON fa.rId = rf.rId
      ORDER BY rId DESC LIMIT 1""")
    userId = self.__create_userId_from_results(cursor.fetchall())

    self.__db.conn.commit()
    cursor.close()

    return userId

  def remove_rfid_from_user(self, rErtek: str):
    cursor = self.__db.conn.cursor()

    existingUserId: UserId = self.get_userId_by_rErtek(rErtek)

    cursor.execute("DELETE FROM belepteto.felhasznaloAzonosito WHERE rId = %s",
                   [existingUserId.get_rid()])
    self.__db.conn.commit()

    cursor.execute("""
    SELECT fhAzonId, fhId, rId, letiltva FROM belepteto.felhasznaloAzonosito as fa
    WHERE rId = %s""", [existingUserId.get_rid()])

    removedUserId = self.__create_userId_from_results(cursor.fetchall())

    if removedUserId is not None:
      raise ValueError(f'Unable to remove rfid {rErtek} from user!')

    self.__db.conn.commit()
    cursor.close()

  def update_lock_for_userId(self, userIdDetails) -> UserId:
    cursor = self.__db.conn.cursor()

    cursor.execute("UPDATE belepteto.felhasznaloAzonosito SET letiltva=%s WHERE fhId=%s AND rId=%s",
                   [userIdDetails["letiltva"], userIdDetails["fhId"], userIdDetails["rId"]])
    self.__db.conn.commit()

    cursor.execute("""SELECT fhAzonId, fhId, rf.rId, rf.rErtek, letiltva FROM belepteto.felhasznaloAzonosito as fa
    INNER JOIN belepteto.rfid as rf
    ON fa.rId = rf.rId
    WHERE fhId=%s AND rf.rId=%s""",
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
      rErtek = row[3]
      letiltva = bool(row[4])
      userId = UserId(fhAzonId, fhId, rId, rErtek, letiltva)
    return userId
