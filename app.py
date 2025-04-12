from flask import Flask, request, jsonify
from extensions import db
import uuid
import os
from models import Product

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
db.init_app(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tracking_id = db.Column(db.String(80), unique=True, nullable=False, default=str(uuid.uuid4()))

    def json(self):
        return {'user_id_for_accessing_tid': self.id, 'tracking_id_for_user': self.tracking_id}

@app.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "Hello, World!"}), 200

@app.route('/user', methods=['POST'])
def create_user():
    try:
        new_user = User()
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.json()), 201
    except Exception as e:
        return jsonify({"An error occurred while trying a POST request on the API": str(e)}), 500

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404
        return jsonify(user.json()), 200
    except Exception as e:
        return jsonify({"An error occurred while trying a GET request on the API": str(e)}), 500

@app.route('/postdata', methods=["POST"])
def add_products():
    try:
        data = request.get_json()
        new_product = Product(
            tracking_no=data['tracking_number'],
            shipment_type=data['shipment_type'],
            parcel_weight=data['parcel_weight'],
            invoice_no=data['invoice_number'],
            transport_mode=data['transport_mode'],
            tax=data['tax'],
            payment_status=data['payment_status'],
            delivery_status=data['delivery_status'],
            current_location=data['current_location'],
            delivery_date=data['delivery_date'],
            additional_notes=data['additional_notes']
        )
        print("It works")
        db.session.add(new_product)
        db.session.commit()
        return jsonify({"Product successfully created":new_product.json()}), 201
    except Exception as e:
        return jsonify({"Error Occurred": str(e)}), 500

@app.route('/getdata', methods=["GET"])
def get_products():
    try:
        products = Product.query.all()
        return jsonify([p.json() for p in products])
    except Exception as e:
        return jsonify({"Error Occurred": str(e)}), 500

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
