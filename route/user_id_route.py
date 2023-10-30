import jsonpickle
from flask import request

from app import app, userIdRepo


@app.route('/userId/<fhId>', methods=['GET'])
def get_userId_by_user(fhId: str):
  try:
    user = userIdRepo.get_userId_by_user(fhId)

    return jsonpickle.encode(user)
  except Exception as e:
    return jsonpickle.encode({'error': 'Unable to retrieve userId for user', 'details': str(e)}), 500


@app.route('/userId', methods=['POST'])
def add_rfid_to_user():
  try:
    userIdDetails = request.get_json()
    userId = userIdRepo.add_rfid_to_user(userIdDetails)

    return jsonpickle.encode(userId)
  except Exception as e:
    return jsonpickle.encode({'error': 'Unable to add rfid to user', 'details': str(e)}), 500


@app.route('/userId/lock/<isLocked>', methods=['PATCH'])
def update_lock_for_userId(isLocked):
  try:
    userIdDetails = request.get_json()
    userIdDetails["letiltva"] = int(isLocked)
    userId = userIdRepo.update_lock_for_userId(userIdDetails)

    return jsonpickle.encode(userId)
  except Exception as e:
    return jsonpickle.encode({'error': 'Unable to change lock state for userId', 'details': str(e)}), 500
