from flask import Flask, request, jsonify
from extensions import db
from flask_cors import CORS
import uuid
import os
from models import Product

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
db.init_app(app)
CORS(app)

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
            shipment_type=data['shipment_type'],
            parcel_weight=data['parcel_weight'],
            invoice_no=data['invoice_number'],
            transport_mode=data['transport_mode'],
            tax=data['tax'],
            payment_status=data['payment_status'],
            delivery_status=data['delivery_status'],
            current_location=data['current_location'],
            delivery_date=data['delivery_date'],
            additional_notes=data['additional_notes'],
            name=data['name'],
            phone_number=data['phone_number'],
            address=data['address']
        )
        print("It works")
        db.session.add(new_product)
        db.session.commit()
        return jsonify({"Product successfully created":new_product.json()}), 201
    except Exception as e:
        return jsonify({"Error Occurred": str(e)}), 500

@app.route('/getdatas', methods=["GET"])
def get_products():
    try:
        products = Product.query.all()
        return jsonify([p.json() for p in products])
    except Exception as e:
        return jsonify({"Error Occurred": str(e)}), 500

@app.route('/updatedata', methods=["PUT"])
def update_product():
    try:
        data = request.get_json()
        tracking_no = request.args.get('tracking_no')
        if not tracking_no:
            return jsonify({"message": "Missing tracking_no in query params"}), 400
        product = Product.query.filter_by(tracking_no=tracking_no).first()
        if not product:
            return jsonify({"message": "Product not found"}), 404

        product.shipment_type = data['shipment_type', product.shipment_type]
        product.parcel_weight = data['parcel_weight', product.parcel_weight]
        product.invoice_no = data['invoice_number', product.invoice_number]
        product.transport_mode = data['transport_mode', product.transport_mode]
        product.tax = data['tax',product.tax]
        product.payment_status = data['payment_status', product.payment_status]
        product.delivery_status = data['delivery_status', product.delivery_status]
        product.current_location = data['current_location', product.current_location]
        product.delivery_date = data['delivery_date', product.delivery_date]
        product.additional_notes = data['additional_notes', product.additional_notes]
        product.name = data['name', product.name]
        product.address = data['address', product.address]
        product.phone_number = data['phone_number', product.phone_number]
        

        db.session.commit()
        return jsonify({"Product successfully updated":product.json()}), 200
    except Exception as e:
        return jsonify({"Error Occurred": str(e)}), 500

@app.route('/deletedata', methods=["DELETE"])
def delete_product():
    try:
        tracking_no = request.args.get('tracking_no')
        product = Product.query.filter_by(tracking_no=tracking_no).first()
        if not product:
            return jsonify({"message": "Product not found"}), 404

        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product successfully deleted"}), 200
    except Exception as e:
        return jsonify({"Error Occurred": str(e)}), 500
    
@app.route('/getdata/<tracking_no>', methods=['GET'])
def get_product_by_id(tracking_no):
    try:
        product = Product.query.filter_by(tracking_no=tracking_no).first()
        if not product:
            return jsonify({"message": "Product not found"}), 404
        return jsonify(product.json()), 200
    except Exception as e:
        return jsonify({"Error Occurred": str(e)}), 500
    
with app.app_context():
    db.create_all()
