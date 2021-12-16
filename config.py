import os

# application settings
MONGO_URL = r"mongodb://127.0.0.1:27017"

# Generate a random secret key
SECRET_KEY = os.urandom(24)
CSRF_ENABLED = True
