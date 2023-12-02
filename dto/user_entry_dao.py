# Data transfer object for retrieving data from the 'felhasznaloAzonosito' and 'belepes' tables
from dto.user_dao import User


class UserEntry:
  __user: User
  __rfId: int
  __belepIdo: str

  def __init__(self, user: User, rfId: int, belepIdo: str):
    self.__user = user
    self.__rfId = rfId
    self.__belepIdo = belepIdo

  def get_user(self) -> User:
    return self.__user

  def get_rf_id(self) -> int:
    return self.__rfId

  def get_belep_ido(self) -> str:
    return self.__belepIdo
