from flask import Flask, render_template, request
from replit import db, database
import datetime
import json

app = Flask('app')

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/get')
def get_db():
  return notedb.to_json()

@app.route('/submit')
def submit():
  note = request.args['note']
  tags = request.args.getlist('tags')
  notedb.save_note(note, tags=tags)
  return render_template('index.html')

class NoteDB:
  def __init__(self, db_url=None):
    self.db = database.Database(db_url) if db_url else db

  def to_json(self):
    return json.dumps(dict(self.db.items()))

  def get_latest(self):
    return self.db["notes"][-1]

  def save_note(self, note, tags=[]):
    timestamp = int(datetime.datetime.now().timestamp())
    notes = self.db.get("notes", [])
    notes.append({
      "timestamp": timestamp,
      "note": note,
      "tags": tags
    })
    self.db["notes"] = notes

  def delete_all(self):
    for k in self.db.keys():
      del self.db[k]

notedb = NoteDB()

if __name__=="__main__":  
  app.run(host='0.0.0.0', port=8080)