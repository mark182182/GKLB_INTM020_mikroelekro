# Data access object for the 'belepes' table
import datetime


class Entry:
  __fhAzonId: int
  __belepIdo: str

  def __init__(self, fhAzonId: int, belepIdo: str):
    self.__fhAzonId = fhAzonId
    self.__belepIdo = belepIdo

  def getFhAzonId(self) -> int:
    return self.__fhAzonId

  def getBelepIdo(self) -> str:
    return self.__belepIdo
