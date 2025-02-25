from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb+srv://nabeeltest:aRYFYcGmXEEZFUmF@cluster0.sqxns.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0", serverSelectionTimeoutMS=5000)

db = client.mydb
motion = db.motion

@app.route('/motion/1/', methods=['POST'])
def set_motion1():
    data = request.json
    if not data or 'motion' not in data:
        return jsonify({"error": "Missing 'motion' field"}), 400

    motion.update_one(
        {"_id": "motion1"},
        {"$set": {"motion": data['motion'], "date": datetime.now()}},
        upsert=True
    )
    return jsonify({"message": "Motion 1 updated successfully"}), 200

@app.route('/motion/2/', methods=['POST'])
def set_motion2():
    data = request.json
    if not data or 'motion' not in data:
        return jsonify({"error": "Missing 'motion' field"}), 400

    motion.update_one(
        {"_id": "motion2"},
        {"$set": {"motion": data['motion'], "date": datetime.now()}},
        upsert=True
    )
    return jsonify({"message": "Motion 2 updated successfully"}), 200

@app.route('/summotion', methods=['POST'])
def set_summotion():
    data = request.json
    if not data or 'sum_motion' not in data:
        return jsonify({"error": "Missing 'sum_motion' field"}), 400

    motion.update_one(
        {"_id": "summotion"},
        {"$set": {"sum_motion": data['sum_motion'], "date": datetime.now()}},
        upsert=True
    )
    return jsonify({"message": "Sum Motion updated successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000, threaded=True)