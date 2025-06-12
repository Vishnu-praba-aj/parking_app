from models import db

class ParkingLot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prime_location_name = db.Column(db.String(100), nullable=False)
    price_per_hour = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    pin_code = db.Column(db.String(10), nullable=False)
    max_number_of_spots = db.Column(db.Integer, nullable=False)

    spots = db.relationship('ParkingSpot', backref='lot', lazy=True, cascade="all, delete-orphan")

    def available_spots_count(self):
        return ParkingSpot.query.filter_by(lot_id=self.id, status='A').count()
    
    def to_dict(self):
        return {
            "id": self.id,
            "prime_location_name": self.prime_location_name,
            "price_per_hour": self.price_per_hour,
            "address": self.address,
            "pin_code": self.pin_code,
            "max_number_of_spots": self.max_number_of_spots
        } 