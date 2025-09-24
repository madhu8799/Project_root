import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from prometheus_flask_exporter import PrometheusMetrics
from models import db, ContactMessage
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Database
    db.init_app(app)
    with app.app_context():
        # For production, prefer migrations; create_all is a simple bootstrap
        db.create_all()

    # CORS: restrict to your frontend origins
    allowed = os.getenv("CORS_ORIGINS", "https://www.rootsolutions.in,https://rootsolutions.in")
    CORS(app, resources={r"/*": {"origins": [o.strip() for o in allowed.split(",")]}})

    # Prometheus metrics at /metrics (optional but recommended per architecture)
    PrometheusMetrics(app)

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok"}), 200

    @app.route("/contact", methods=["POST"])
    def contact():
        # Accept both JSON and form posts to be compatible with any frontend state
        data = {}
        if request.is_json:
            data = request.get_json(silent=True) or {}
        else:
            data = {
                "name": request.form.get("name"),
                "email": request.form.get("email"),
                "phone": request.form.get("phone"),
                "message": request.form.get("message"),
            }

        # Minimal validation
        name = (data.get("name") or "").strip()
        email = (data.get("email") or "").strip()
        phone = (data.get("phone") or "").strip()
        message = (data.get("message") or "").strip()

        if not (name and email and phone and message):
            return jsonify({"error": "All fields are required"}), 400

        msg = ContactMessage(name=name, email=email, phone=phone, message=message)
        db.session.add(msg)
        db.session.commit()

        return jsonify({"status": "received"}), 201

    return app

app = create_app()

if __name__ == "__main__":
    # For local testing only; use Gunicorn in Docker/EC2
    app.run(host="0.0.0.0", port=5000)
