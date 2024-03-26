# Import necessary modules
import os

# CockroachDB URI
COCKROACHDB_URI = "cockroachdb://deepak270705_outlook:Je96vnLUNqCnZAGmS4TiLA@hungry-tamarin-9056.8nk.gcp-asia-southeast1.cockroachlabs.cloud:26257/codecrafters?sslmode=verify-full"

# Update SQLAlchemy Database URI
SQLALCHEMY_DATABASE_URI = COCKROACHDB_URI

# Disable SQLAlchemy track modifications
SQLALCHEMY_TRACK_MODIFICATIONS = False
