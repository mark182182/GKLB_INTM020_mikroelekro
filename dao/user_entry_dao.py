# Data access object for retrieving data from the 'felhasznaloAzonosito' and 'belepes' tables
from dao.user_dao import User

class UserEntry:
  __user: User
  __rfId: int
  __belepIdo: str

  def __init__(self, user: User, rfId: int, belepIdo: str):
    self.__user = user
    self.__rfId = rfId
    self.__belepIdo = belepIdo

  def getUser(self) -> User:
    return self.__user

  def getRfId(self) -> int:
    return self.__rfId

  def getBelepIdo(self) -> str:
    return self.__belepIdo
