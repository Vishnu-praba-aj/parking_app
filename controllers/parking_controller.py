from flask import Blueprint, request, jsonify
from models import db
from models.parking_lot import ParkingLot
from models.parking_spot import ParkingSpot
from models.reservation import Reservation
from datetime import datetime



parking_bp = Blueprint('parking', __name__, url_prefix='/parkinglots')


@parking_bp.route('/all_users', methods=['GET'])
def get_all_users():
    from models.user import User  # or wherever it's defined
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'username': user.username,
        'email': user.email
    } for user in users])


# GET all parking lots
@parking_bp.route('/get_lots', methods=['GET'])
def get_parking_lots():
    lots = ParkingLot.query.all()
    return jsonify([{
        "id": lot.id,
            "prime_location_name": lot.prime_location_name,
            "price_per_hour": lot.price_per_hour,
            "address": lot.address,
            "pin_code": lot.pin_code,
            "max_number_of_spots": lot.max_number_of_spots
    } for lot in lots])

@parking_bp.route('/<int:lot_id>', methods=['GET'])
def get_one_parking_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    return jsonify({
        'id': lot.id,
        'name': lot.name,
        'location': lot.location,
        'price_per_hour': lot.price_per_hour,
        'address': lot.address,
        'pin_code': lot.pin_code,
        'max_number_of_spots': lot.max_number_of_spots
    })


@parking_bp.route('/spot/<int:spot_id>', methods=['GET'])
def get_one_parking_spot(spot_id):
    spot = ParkingSpot.query.get_or_404(spot_id)
    return jsonify({
        'id': spot.id,
        'spot_number': spot.spot_number,
        'status': spot.status,
        'lot_id': spot.lot_id
    })

@parking_bp.route('/user_summary/<int:user_id>', methods=['GET'])
def user_summary(user_id):
    reservations = Reservation.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'reservation_id': r.id,
        'spot_id': r.spot_id,
        'lot_id': r.spot.lot_id,
        'spot_number': r.spot.spot_number,
        'parking_timestamp': r.parking_timestamp,
        'leaving_timestamp': r.leaving_timestamp,
        'parking_cost': r.parking_cost
    } for r in reservations])

@parking_bp.route('/book_spot/<int:lot_id>', methods=['POST'])
def book_parking_spot(lot_id):
    data = request.json
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({'message': 'User ID is required'}), 400

    # Find first available spot in the lot (status = 'A' means available)
    spot = ParkingSpot.query.filter_by(lot_id=lot_id, status='A').first()
    if not spot:
        return jsonify({'message': 'No available spots in this lot'}), 404

    # Mark spot as occupied
    spot.status = 'O'

    # Create reservation with current time as parking_timestamp
    reservation = Reservation(
        spot_id=spot.id,
        user_id=user_id,
        parking_timestamp=datetime.utcnow()
    )

    db.session.add(reservation)
    db.session.commit()

    return jsonify({
        'reservation_id': reservation.id,
        'spot_id': spot.id,
        'spot_number': spot.spot_number,
        'lot_id': lot_id,
        'user_id': user_id,
        'parking_timestamp': reservation.parking_timestamp.isoformat()
    }), 201


# POST (Create)
@parking_bp.route('/create_lot', methods=['POST'])
def create_parking_lot():
    # data = dict with keys: prime_location_name, price_per_hour, address, pin_code, max_number_of_spots
    data=request.get_json()
    lot = ParkingLot(
        prime_location_name=data['prime_location_name'],
        price_per_hour=data['price_per_hour'],
        address=data['address'],
        pin_code=data['pin_code'],
        max_number_of_spots=data['max_number_of_spots']
    )
    db.session.add(lot)
    db.session.commit()  # Need id to create spots linked to lot

    # Create spots
    for i in range(1, lot.max_number_of_spots + 1):
        spot = ParkingSpot(
            lot_id=lot.id,
            spot_number=f'S{i}',
            status='A'  # Available by default
        )
        db.session.add(spot)

    db.session.commit()
    return lot.to_dict(), 201

# PUT (Update)
@parking_bp.route('/release_spot/<int:reservation_id>', methods=['PUT'])
def release_parking_spot(reservation_id):
    reservation = Reservation.query.get(reservation_id)
    if not reservation or reservation.leaving_timestamp:
        return False  # Already released or invalid

    reservation.leaving_timestamp = datetime.utcnow()
    
    # Calculate parking cost (simple example)
    duration_hours = (reservation.leaving_timestamp - reservation.parking_timestamp).total_seconds() / 3600
    price_per_hour = reservation.spot.lot.price_per_hour
    reservation.parking_cost = round(duration_hours * price_per_hour, 2)

    # Set spot status available again
    spot = reservation.spot
    spot.status = 'A'

    db.session.commit()
    return True

@parking_bp.route('/lot/<int:lot_id>/status', methods=['GET'])
def lot_status(lot_id):
    spots = ParkingSpot.query.filter_by(lot_id=lot_id).all()
    status_info = []
    for spot in spots:
        info = {
            'spot_id': spot.id,
            'spot_number': spot.spot_number,
            'status': spot.status
        }
        if spot.status == 'O':
            reservation = Reservation.query.filter_by(spot_id=spot.id).order_by(Reservation.parking_timestamp.desc()).first()
            info['user_id'] = reservation.user_id
            info['parked_at'] = reservation.parking_timestamp.isoformat()
        status_info.append(info)

    return jsonify(status_info)

# DELETE
@parking_bp.route('/delete_lot/<int:lot_id>', methods=['DELETE'])
def delete_parking_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    occupied_spots = ParkingSpot.query.filter_by(lot_id=lot_id, status='O').count()
    if occupied_spots > 0:
        return jsonify({'message': 'Cannot delete lot. Some spots are still occupied.'}), 400

    # Safe to delete
    ParkingSpot.query.filter_by(lot_id=lot_id).delete()
    db.session.delete(lot)
    db.session.commit()
    return jsonify({'message': 'Parking lot deleted successfully'})



@parking_bp.route('/update_lot/<int:lot_id>', methods=['PUT'])
def update_parking_lot(lot_id):
    data = request.json
    lot = ParkingLot.query.get_or_404(lot_id)

    updated_spots = data.get('max_number_of_spots')
    if updated_spots is not None and updated_spots != lot.max_number_of_spots:
        current_spots = ParkingSpot.query.filter_by(lot_id=lot.id).order_by(ParkingSpot.spot_number).all()
        current_count = len(current_spots)

        if updated_spots > current_count:
            # Add new spots
            for i in range(current_count + 1, updated_spots + 1):
                new_spot = ParkingSpot(
                    lot_id=lot.id,
                    spot_number=f'S{i}',
                    status='A'
                )
                db.session.add(new_spot)

        elif updated_spots < current_count:
            # Check if the spots to be removed are unoccupied
            to_remove = current_spots[updated_spots:]
            for spot in to_remove:
                if spot.status == 'O':
                    return jsonify({'error': 'Cannot reduce spots. Some spots are still occupied.'}), 400
                db.session.delete(spot)

        lot.max_number_of_spots = updated_spots

    # Update other fields
    for field in ['prime_location_name', 'price_per_hour', 'address', 'pin_code']:
        if field in data:
            setattr(lot, field, data[field])

    db.session.commit()
    return jsonify({'message': f'Parking lot {lot_id} updated successfully'}), 200
