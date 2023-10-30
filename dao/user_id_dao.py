# Data access object for the 'felhasznaloAzonosito' table
class UserId:
  __fhAzonId: int
  __fhId: int
  __rfId: int
  __letiltva: bool

  def __init__(self, fhAzonId: int, fhId: int, rfId: int, letiltva: bool):
    self.__fhAzonId = fhAzonId
    self.__fhId = fhId
    self.__rfId = rfId
    self.__letiltva = letiltva

  def getFhId(self) -> int:
    return self.__fhId

  def getFhNev(self) -> str:
    return self.__fhNev

  def getFhAzonId(self) -> int:
    return self.__fhAzonId

  def getFhId(self) -> int:
    return self.__fhId

  def getRfId(self) -> int:
    return self.__rfId

  def getLetiltva(self) -> bool:
    return self.__letiltva
