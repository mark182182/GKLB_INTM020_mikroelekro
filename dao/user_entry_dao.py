# Data access object for retrieving data from the 'felhasznaloAzonosito' and 'belepes' tables
from dao.entry_dao import Entry
from dao.user_dao import User

class UserEntry:
  __user: User
  __rfId: int
  __belepIdo: str

  def __init__(self, userId: UserId, entry: Entry):
    self.__userId = userId
    self.__entry = entry

    self.__user
    self.__rfId
    self.__belepIdo

  def getUserId(self) -> UserId:
    return self.__userId

  def getEntry(self) -> Entry:
    return self.__entry
