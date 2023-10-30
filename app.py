from flask import Flask

from db.db import Database
from repo.user_identifier import UserIdRepository
from repo.user_repo import UserRepository
from repo.rfid_repo import RfidRepository

app = Flask(__name__)
db = Database()
db.setup()

userRepo = UserRepository(db)
rfidRepo = RfidRepository(db)
userIdRepo = UserIdRepository(db)

from route import user_route, rfid_route, user_id_route