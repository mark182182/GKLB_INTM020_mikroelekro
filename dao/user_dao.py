# Data access object for the 'felhasznalok' table
class User:
  __fhId: int
  __fhNev: str

  def __init__(self, fhId: int, fhNev: str):
    self.__fhId = fhId
    self.__fhNev = fhNev

  def getFhId(self) -> int:
    return self.__fhId

  def getFhNev(self) -> str:
    return self.__fhNev
