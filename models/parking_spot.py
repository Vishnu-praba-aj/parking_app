from models import db

class ParkingSpot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'), nullable=False)
    spot_number = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(1), nullable=False, default='A')  # 'A' = Available, 'O' = Occupied

    reservation = db.relationship('Reservation', backref='spot', uselist=False, cascade="all, delete-orphan")
