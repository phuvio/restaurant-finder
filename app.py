from os import getenv
from flask import Flask
from flask_googlemaps import GoogleMaps


app = Flask(__name__)

app.config['GOOGLEMAPS_KEY'] = getenv('GOOGLEMAPS_KEY')
app.config['SECRET_KEY'] = getenv('SECRET_KEY')

GoogleMaps(app)

import routes
