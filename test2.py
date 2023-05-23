from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['MONGODB_SETTINGS'] = {
    'host': config.DBURL,
    'alias': 'default'
}

