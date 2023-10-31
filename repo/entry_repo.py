from dao.entry_dao import Entry
from dao.user_entry_dao import UserEntry
from dao.user_id_dao import UserId
from db.db import Database


# Database queries related to the 'belepes' table
class EntryRepository:
  __db: Database

  def __init__(self, db: Database):
    self.__db = db

  def get_entry_by_user(self, fhId: str) -> list[UserEntry]:
    cursor = self.__db.conn.cursor()

    cursor.execute("""
    SELECT fa.fhAzonId, fa.fhId, fa.rId, fa.letiltva, b.belepIdo FROM belepteto.felhasznaloAzonosito as fa
    INNER JOIN belepteto.belepes as b
    ON b.fhAzonId = fa.fhAzonId
    WHERE fhId = %s""", [fhId])

    userEntries: list[UserEntry] = self.__create_entry_from_results(cursor.fetchall())

    self.__db.conn.commit()
    cursor.close()
    return userEntries

  def get_entries_for_all_users(self) -> list[UserEntry]:
    cursor = self.__db.conn.cursor()

    cursor.execute("""
    SELECT fa.fhAzonId, fa.fhId, fa.rId, fa.letiltva, b.belepIdo FROM belepteto.felhasznaloAzonosito as fa
    INNER JOIN belepteto.belepes as b
    ON b.fhAzonId = fa.fhAzonId
    """)
    self.__db.conn.commit()

    userEntries: list[UserEntry] = self.__create_entry_from_results(cursor.fetchall())
    cursor.close()

    return userEntries

  def __create_entry_from_results(self, results) -> list[UserEntry]:
    userEntries: list[UserEntry] = []

    for row in results:
      fhAzonId = row[0]
      fhId = row[1]
      rId = row[2]
      letiltva = bool(row[3])
      belepIdo = row[4]
      userEntries.append(UserEntry(UserId(fhAzonId, fhId, rId, letiltva),
                                   Entry(fhAzonId, str(belepIdo))))
    return userEntries
