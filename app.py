import os
from flask import Flask, request, jsonify, abort
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGODB_URI")
mongo = PyMongo(app)
db = mongo.db

ALLOWED_SEVERITIES = {"Low", "Medium", "High"}

def incident_to_json(incident):
    return {
        "id": str(incident["_id"]),
        "title": incident["title"],
        "description": incident["description"],
        "severity": incident["severity"],
        "reported_at": incident["reported_at"].isoformat() + "Z"
    }
    
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the SparklyHood Incident API!"}), 200

@app.route("/incidents", methods=["GET"])
def get_incidents():
    incidents = db.incidents.find()
    return jsonify([incident_to_json(i) for i in incidents]), 200

@app.route("/incidents", methods=["POST"])
def create_incident():
    data = request.get_json(force=True)
    title = data.get("title")
    description = data.get("description")
    severity = data.get("severity")
    if not title or not description or not severity:
        return jsonify({"error": "Missing required fields"}), 400
    if severity not in ALLOWED_SEVERITIES:
        return jsonify({"error": "Invalid severity"}), 400
    incident = {
        "title": title,
        "description": description,
        "severity": severity,
        "reported_at": datetime.utcnow()
    }
    result = db.incidents.insert_one(incident)
    incident["_id"] = result.inserted_id
    return jsonify(incident_to_json(incident)), 201

@app.route("/incidents/<id>", methods=["GET"])
def get_incident(id):
    try:
        incident = db.incidents.find_one({"_id": ObjectId(id)})
    except Exception:
        return jsonify({"error": "Invalid incident id"}), 400
    if not incident:
        return jsonify({"error": "Incident not found"}), 404
    return jsonify(incident_to_json(incident)), 200

@app.route("/incidents/<id>", methods=["DELETE"])
def delete_incident(id):
    try:
        result = db.incidents.delete_one({"_id": ObjectId(id)})
    except Exception:
        return jsonify({"error": "Invalid incident id"}), 400
    if result.deleted_count == 0:
        return jsonify({"error": "Incident not found"}), 404
    return '', 204

if __name__ == "__main__":
    app.run(debug=True)
