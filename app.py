from flask import Flask

from db.db import Database
from repo.user_repo import UserRepository
from repo.rfid_repo import RfidRepository

app = Flask(__name__)
db = Database()
db.setup()

userRepo = UserRepository(db)
rfidRepo = RfidRepository(db)

from route import user_route
from route import rfid_route
