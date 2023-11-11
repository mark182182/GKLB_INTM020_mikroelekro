from flask import Flask

from db.db import Database
from raspi.lcd_i2c import LcdI2c
from raspi.rfid_spi import RfidSpi
from repo.entry_repo import EntryRepository
from repo.user_id_repo import UserIdRepository
from repo.user_repo import UserRepository
from repo.rfid_repo import RfidRepository

app = Flask(__name__)

db = Database()
db.setup()

lcdI2c = LcdI2c()

userRepo = UserRepository(db)
rfidRepo = RfidRepository(db)
userIdRepo = UserIdRepository(db, rfidRepo)
entryRepo = EntryRepository(db, userIdRepo, lcdI2c)

from route import user_route, rfid_route, user_id_route, entry_route

rfidSpi = RfidSpi(entryRepo)
lcdI2c.wait_for_input()
