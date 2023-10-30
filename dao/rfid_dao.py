# Data access object for the 'rfid' table
class Rfid:
  __rId: int
  __rErtek: str

  def __init__(self, rId: int, rErtek: str):
    self.__rId = rId
    self.__rErtek = rErtek

  def getRid(self) -> int:
    return self.__rId

  def getRertek(self) -> str:
    return self.__rErtek
