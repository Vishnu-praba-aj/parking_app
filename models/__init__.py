from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)

    # Import models here to register them before create_all
    from .user import User
    from .admin import Admin
    from .parking_lot import ParkingLot
    from .parking_spot import ParkingSpot
    from .reservation import Reservation

    with app.app_context():
        db.create_all()
        print("✅ Database initialized and all tables created.")
