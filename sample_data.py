import os
from flask_pymongo import PyMongo
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask

load_dotenv()
app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGODB_URI")
mongo = PyMongo(app)
db = mongo.db

sample_incidents = [
    {
        "title": "AI model generated biased output",
        "description": "A language model produced a racially biased response during testing.",
        "severity": "High",
        "reported_at": datetime.utcnow()
    },
    {
        "title": "Unexpected system shutdown",
        "description": "AI-powered system shut down unexpectedly, causing service disruption.",
        "severity": "Medium",
        "reported_at": datetime.utcnow()
    },
    {
        "title": "Minor data privacy leak",
        "description": "A user’s data was briefly accessible to another user due to a bug.",
        "severity": "Low",
        "reported_at": datetime.utcnow()
    }
]

if __name__ == "__main__":
    db.incidents.insert_many(sample_incidents)
    print("Sample incidents inserted.")
