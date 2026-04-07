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


def find_event_by_uid(uid):
    for event in EVENTS:
        if event["uid"] == uid:
            return event
    return None


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

    existing = find_event_by_uid(data["uid"])
    if existing:
        return jsonify({
            "error": "UID already exists",
            "uid": data["uid"]
        }), 409

    EVENTS.append(data)
    return jsonify({"message": "Event added successfully", "event": data}), 201


@app.route("/events/<uid>", methods=["PUT"])
def update_event(uid):
    data = request.get_json()

    event = find_event_by_uid(uid)
    if not event:
        return jsonify({
            "error": "Event not found",
            "uid": uid
        }), 404

    required_fields = ["uid", "type", "lat", "lon", "status", "label"]
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({
            "error": "Missing required fields",
            "missing_fields": missing_fields
        }), 400

    if data["uid"] != uid:
        return jsonify({
            "error": "UID in path and body do not match",
            "path_uid": uid,
            "body_uid": data["uid"]
        }), 400

    event["type"] = data["type"]
    event["lat"] = data["lat"]
    event["lon"] = data["lon"]
    event["status"] = data["status"]
    event["label"] = data["label"]

    return jsonify({
        "message": "Event updated successfully",
        "event": event
    }), 200


@app.route("/events/<uid>", methods=["DELETE"])
def delete_event(uid):
    event = find_event_by_uid(uid)
    if not event:
        return jsonify({
            "error": "Event not found",
            "uid": uid
        }), 404

    EVENTS.remove(event)
    return jsonify({
        "message": "Event deleted successfully",
        "uid": uid
    }), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)