from db.db import Database
from dao.rfid_dao import Rfid


class RfidRepository:
  __db: Database

  def __init__(self, db: Database):
    self.__db = db

  def get_rfid_by_id(self, rId: str) -> Rfid:
    cursor = self.__db.conn.cursor()

    cursor.execute("SELECT rId, rErtek FROM belepteto.rfid WHERE rId = %s", [rId])
    existingRfid = self.__create_rfid_from_results(cursor.fetchall())
    if existingRfid is None:
      raise ValueError(f'Rfid with id: {rId} does not exist!')

    self.__db.conn.commit()
    cursor.close()
    return existingRfid

  def get_rfids(self) -> list[Rfid]:
    cursor = self.__db.conn.cursor()

    cursor.execute("SELECT rId, rErtek FROM belepteto.rfid")
    results = cursor.fetchall()

    rfids = []
    for row in results:
      rId = row[0]
      rErtek = row[1]
      rfids.append(Rfid(rId, rErtek))

    self.__db.conn.commit()
    cursor.close()
    return rfids

  def create_rfid(self, rfidDetails: any) -> Rfid:
    cursor = self.__db.conn.cursor()

    cursor.execute("INSERT INTO belepteto.rfid VALUES (NULL, %s)", [rfidDetails["ertek"]])
    self.__db.conn.commit()

    cursor.execute("SELECT rId, rErtek FROM belepteto.rfid ORDER BY rId DESC LIMIT 1")
    rfid = self.__create_rfid_from_results(cursor.fetchall())

    self.__db.conn.commit()
    cursor.close()

    return rfid

  def update_rfid(self, rfidDetails: any) -> Rfid:
    cursor = self.__db.conn.cursor()

    try:
      existingRfid = self.get_rfid_by_id(rfidDetails["id"])
      if existingRfid is None:
        raise ValueError(f'Rfid with id: {rfidDetails["id"]} does not exist!')

      cursor.execute("UPDATE belepteto.rfid SET rErtek=%s WHERE rId=%s",
                     [rfidDetails["ertek"], rfidDetails["id"]])
      self.__db.conn.commit()

      rfid = self.get_rfid_by_id(rfidDetails["id"])
      return rfid

    finally:
      self.__db.conn.commit()
      cursor.close()

  def delete_rfid(self, rId: str):
    cursor = self.__db.conn.cursor()
    try:
      existingRfid = self.get_rfid_by_id(rId)
      if existingRfid is None:
        raise ValueError(f'Rfid with id: {rId} does not exist!')
      cursor.execute("DELETE FROM belepteto.rfid WHERE rId=%s", [rId])

    finally:
      self.__db.conn.commit()
      cursor.close()

  def __create_rfid_from_results(self, results) -> Rfid:
    rfid = None
    for row in results:
      rId = row[0]
      rErtek = row[1]
      rfid = Rfid(rId, rErtek)
    return rfid
