from extensions import db
import uuid

class Product(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    tracking_no = db.Column(db.String(36), nullable=False,default=lambda: str(uuid.uuid4()))
    shipment_type = db.Column(db.String, nullable=False)
    parcel_weight = db.Column(db.String,nullable=False)
    invoice_no = db.Column(db.Integer,nullable=False)
    transport_mode = db.Column(db.String,nullable=False)
    tax = db.Column(db.String,nullable=False)
    payment_status = db.Column(db.Boolean,default=False,nullable=False)
    delivery_status = db.Column(db.Boolean,default=False,nullable=False)
    current_location = db.Column(db.String,nullable=False)
    delivery_date = db.Column(db.String,nullable=True)
    additional_notes = db.Column(db.String, nullable=True)
    address = db.Column(db.String,nullable=False)
    name = db.Column(db.String,nullable=False)
    phone_number = db.Column(db.String,nullable=False)

    def json(self):
        output = {
            "id": self.id,
            "tracking_number": self.tracking_no,
            "shipment_type": self.shipment_type,
            "parcel_weight": self.parcel_weight,
            "invoice_number": self.invoice_no,
            "transport_mode": self.transport_mode,
            "tax": self.tax,
            "payment_status": self.payment_status,
            "delivery_status": self.delivery_status,
            "current_location": self.current_location,
            "delivery_date": self.delivery_date, # Ensure date is serialized correctly
            "additional_notes": self.additional_notes,
            "phone_number":self.phone_number,
            "name":self.name,
            "address":self.address
        }
        print(output)
        return output
