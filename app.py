from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

EVENTS = [
    {
        "uid": "target-001",
        "type": "friendly",
        "lat": 24.1477,
        "lon": 120.6736,
        "status": "active",
        "label": "Friendly Unit A"
    },
    {
        "uid": "target-002",
        "type": "hostile",
        "lat": 24.1577,
        "lon": 120.6836,
        "status": "active",
        "label": "Hostile Unit B"
    }
]

@app.route("/events", methods=["GET"])
def get_events():
    return jsonify(EVENTS)

@app.route("/events", methods=["POST"])
def add_event():
    data = request.get_json()

    required_fields = ["uid", "type", "lat", "lon", "status", "label"]
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({
            "error": "Missing required fields",
            "missing_fields": missing_fields
        }), 400

    EVENTS.append(data)
    return jsonify({"message": "Event added successfully", "event": data}), 201

if __name__ == "__main__":
    app.run(debug=True, port=5000)