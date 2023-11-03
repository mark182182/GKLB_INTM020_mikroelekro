import jsonpickle
from app import app, entryRepo


@app.route('/entry/user/<fhId>', methods=['GET'])
def get_entry_by_user(fhId: str):
  try:
    userEntry = entryRepo.get_entry_by_user(fhId)

    return jsonpickle.encode(userEntry)
  except Exception as e:
    return jsonpickle.encode({'error': 'Unable to retrieve entry for user', 'details': str(e)}), 500


@app.route('/entry', methods=['GET'])
def get_entries_for_all_users():
  try:
    userEntries = entryRepo.get_entries_for_all_users()

    return jsonpickle.encode(userEntries)
  except Exception as e:
    return jsonpickle.encode({'error': 'Unable to retrieve entries for all users', 'details': str(e)}), 500


@app.route('/entry/rfid/<rErtek>', methods=['GET'])
def check_entry_for_rfid(rErtek: str):
  try:
    userEntry = entryRepo.check_entry_for_rfid(rErtek)

    return jsonpickle.encode(userEntry), 200
  except Exception as e:
    return jsonpickle.encode({'error': 'Unable to enter using rfid', 'details': str(e)}), 500
