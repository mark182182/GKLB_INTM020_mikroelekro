import threading
from time import sleep

from pirc522 import RFID

from repo.entry_repo import EntryRepository


class RfidSpi:
  __entryRepo: EntryRepository
  __rdr = RFID(pin_irq=None)
  __is_reading: bool = False

  def __init__(self, entryRepo: EntryRepository):
    self.__entryRepo = entryRepo
    self.__wait_for_input()

  def __wait_for_input(self):
    if not self.__is_reading:
      self.__is_reading = True
      uid = self.__rdr.read_id(as_number=True)
      if uid is not None:
        print(f'reading card: {uid}')
        self.__entryRepo.check_entry_for_rfid(uid)
      self.__is_reading = False
      schedule = threading.Timer(1, self.__wait_for_input)
      schedule.start()
