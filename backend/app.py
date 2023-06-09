from flask import Flask
from flask_cors import CORS
import redis
from config.FirebaseManager import FirebaseManager

firebase_manager = FirebaseManager()

app = Flask(__name__)
CORS(app)
app.config['REDIS_URL'] = 'redis://localhost:6379/0'
redis_client = redis.from_url(app.config['REDIS_URL'])