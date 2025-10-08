from flask import Flask, request, redirect, jsonify
from flask_cors import CORS  # 🔥 NEW: Enable CORS
from models import db, Inquiry
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)  # 🔥 NEW: Allow requests from different origins (like S3)

db.init_app(app)

@app.route('/')
def home():
    return "Root Solutions Backend Running!"

@app.route('/contact', methods=['POST'])
def handle_contact():
    data = request.form
    inquiry = Inquiry(
        name=data.get('name'),
        email=data.get('email'),
        phone=data.get('phone'),
        message=data.get('message')
    )
    db.session.add(inquiry)
    db.session.commit()

    # ✅ Future: Trigger AI smart reply here
    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if not exist
    app.run(debug=True, host="0.0.0.0", port=5000)
