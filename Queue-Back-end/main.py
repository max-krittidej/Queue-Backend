from logging import INFO
from flask import Flask,request
import json
from google.cloud import firestore
import datetime
import pytz

app = Flask(__name__)
db = firestore.Client(project='beyond-kids-project')
queue = db.collection('new_queue')
Tz = pytz.timezone("Asia/Bangkok")
#https://firebase.google.com/docs/firestore/manage-data/delete-data
def delete_collection(coll_ref):

  docs = coll_ref.list_documents()
  deleted = 0

  for doc in docs:
      print(f"Deleting doc {doc.id} => {doc.get().to_dict()}")
      doc.delete()
      deleted = deleted + 1


@app.route('/enqueue', methods=[ "POST"])
def index():
    place = request.json["place_id"]
    info = queue.document(place).get().to_dict()
    info["new_queue_no"]+=1
    queue.document(place).set(info)
    json_text = json.dumps(info)
    return json_text 
  
@app.route('/call', methods=["POST"])
def index2():
    place = request.json["place_id"]
    info = queue.document(place).get().to_dict()
    if info["current_calling_queue_no"] != info["new_queue_no"]:
      info["current_calling_queue_no"]+=1
      print(info)
      data ={
        "counter_id": request.json["counter_id"],
        "datetime": datetime.datetime.now(Tz),
        'calling_queue': info["current_calling_queue"]
      }
      queue.document(place).collection("calls").document(info["current_calling_queue"]).set(data)
      queue.document(place).set(info)
      value= info
    
    value = 0
    
    json_text = json.dumps(value)
    return json_text

@app.route('/reset', methods=["POST"])
def index3():
    place = request.json["place_id"]
    info = queue.document(place).get().to_dict()
    info = {'new_queue_no': 0, 'current_calling_queue_no': 0, 'place_id': place}
    queue.document(place).set(info)
    json_text = json.dumps(info)
    delete_collection(queue.document(place).collection("calls"))
    return json_text



if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80)



# new_queue_no: 0 , current 0

#enqueue
#new_queue_no:2, 
