from flask import Flask
from models import db, init_db
from controllers.auth import auth_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "b'x\xd0q\x8a3\xb91\xa1\x82\xa7T\xa5q3\xea\x07\xf2\nR\xc4dO5='"  # Needed for session and flash

# Initialize DB and create tables
init_db(app)

# Register blueprints
app.register_blueprint(auth_bp)

from controllers.parking_controller import parking_bp

app.register_blueprint(parking_bp)


@app.route('/')
def home():
    return 'Welcome to the Parking App 🚗'

if __name__ == '__main__':
    app.run(debug=True)
