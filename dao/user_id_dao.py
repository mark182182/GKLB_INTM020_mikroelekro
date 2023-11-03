# Data access object for the 'felhasznaloAzonosito' table
class UserId:
  __fhAzonId: int
  __fhId: int
  __rId: int
  __rfErtek: str
  __letiltva: bool

  def __init__(self, fhAzonId: int, fhId: int, rId: int, rfErtek: str, letiltva: bool):
    self.__fhAzonId = fhAzonId
    self.__fhId = fhId
    self.__rId = rId
    self.__rfErtek = rfErtek
    self.__letiltva = letiltva

  def getFhId(self) -> int:
    return self.__fhId

  def getFhAzonId(self) -> int:
    return self.__fhAzonId

  def getRid(self) -> int:
    return self.__rId

  def getRfertek(self) -> str:
    return self.__rfErtek

  def getLetiltva(self) -> bool:
    return self.__letiltva
