from dao.user_dao import User
from dao.user_entry_dao import UserEntry
from dao.user_id_dao import UserId
from db.db import Database
#from raspi.lcd_i2c import LcdI2c
from repo.user_id_repo import UserIdRepository
from smtp.smtp_client import smtp


# Database queries related to the 'belepes' table
class EntryRepository:
  __db: Database
  __userIdRepo: UserIdRepository
  #__lcdI2c: LcdI2c

  def __init__(self, db: Database, userIdRepo: UserIdRepository#, lcdI2c: LcdI2c
   ):
    self.__db = db
    self.__userIdRepo = userIdRepo
    #self.__lcdI2c = lcdI2c

  def get_entry_by_user(self, fhId: int, isTop1: bool = False) -> list[UserEntry]:
    cursor = self.__db.conn.cursor()

    query = """
    SELECT fa.fhId, fh.fhNev, fa.rId, b.belepIdo FROM belepteto.felhasznaloAzonosito as fa 
    INNER JOIN belepteto.belepes as b
    ON fa.fhAzonId = b.fhAzonId
    INNER JOIN belepteto.felhasznalok as fh
    ON fa.fhId = fh.fhId 
    WHERE fh.fhId = %s"""

    cursor.execute(f'{query} ORDER BY b.belepIdo DESC LIMIT 1' if isTop1 else query, [fhId])

    userEntries: list[UserEntry] = self.__create_entry_from_results(cursor.fetchall())

    self.__db.conn.commit()
    cursor.close()
    return userEntries

  def get_entries_for_all_users(self) -> list[UserEntry]:
    cursor = self.__db.conn.cursor()

    cursor.execute("""
    SELECT fa.fhId, fh.fhNev, fa.rId, b.belepIdo FROM belepteto.felhasznaloAzonosito as fa
    INNER JOIN belepteto.belepes as b
    ON fa.fhAzonId = b.fhAzonId
    INNER JOIN belepteto.felhasznalok as fh
    ON fa.fhId = fh.fhId""")

    userEntries: list[UserEntry] = self.__create_entry_from_results(cursor.fetchall())

    self.__db.conn.commit()
    cursor.close()
    return userEntries

  def check_entry_for_rfid(self, rErtek: str) -> UserEntry:
    cursor = self.__db.conn.cursor()
    try:
      try:
        existingUserId: UserId = self.__userIdRepo.get_userId_by_rErtek(rErtek)
      except ValueError as e:
        self.__lcdI2c.denied_unknown()
        raise e

      cursor.execute("""
      INSERT INTO belepteto.belepes VALUES (%s, CURRENT_TIMESTAMP)
      """, [existingUserId.get_fh_azon_id()])
      self.__db.conn.commit()

      if existingUserId.get_letiltva():
        self.__lcdI2c.denied_locked()
        self.__send_mail_on_too_many_attempts(existingUserId)
        raise ValueError(f'{rErtek} is locked, cannot enter!')

      cursor.execute("""SELECT fhAzonId, belepIdo FROM belepteto.belepes
       WHERE fhAzonId = %s
       ORDER BY belepIdo DESC LIMIT 1""", [existingUserId.get_fh_azon_id()])

      results = cursor.fetchall()

      if len(results) != 1:
        #self.__lcdI2c.denied_generic()
        raise ValueError(f'Unable to enter using rfid value {rErtek}!')

      userEntry = self.get_entry_by_user(existingUserId.get_fh_id(), True)

      if len(userEntry) != 1:
        #self.__lcdI2c.denied_generic()
        raise ValueError(f'Unable to enter using rfid value {rErtek}!')

      self.__db.conn.commit()
      #self.__lcdI2c.allowed()
      return userEntry[0]
    except ValueError as e:
      raise e
    finally:
      cursor.close()

  def __create_entry_from_results(self, results) -> list[UserEntry]:
    userEntries: list[UserEntry] = []

    for row in results:
      fhId = row[0]
      fhNev = row[1]
      rId = row[2]
      belepIdo = row[3]

      userEntries.append(UserEntry(User(fhId, fhNev), rId, str(belepIdo)))
    return userEntries

  def __send_mail_on_too_many_attempts(self, userId: UserId):
    entries: list[UserEntry] = self.get_entry_by_user(userId.get_fh_id())
    belepIdok: list[str] = []
    for entry in entries:
      belepIdok.append(entry.get_belep_ido())

    if len(entries) == 3:
      print("Too many attempts with locked card, sending e-mail")
      smtp.send_email_on_unauthorized(userId.get_rfertek(), userId.get_fh_id(), belepIdok)
