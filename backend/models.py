from flask_sqlalchemy import SQLAlchemy

# CockroachDB URI
COCKROACHDB_URI = "cockroachdb://deepak270705_outlook:Je96vnLUNqCnZAGmS4TiLA@hungry-tamarin-9056.8nk.gcp-asia-southeast1.cockroachlabs.cloud:26257/codecrafters?sslmode=verify-full"

# Initialize SQLAlchemy instance
db = SQLAlchemy()

# Configure Flask app to use CockroachDB URI
def configure_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = COCKROACHDB_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'
