import os

from flask import Flask, g
from flask_basicauth import BasicAuth
from flask_expects_json import expects_json
from flask_rest_error_handling import setup_error_handling

from .models import Insurance
from .payload_validation_schemas import quote_schema


def create_app():
    app = Flask(__name__)
    app.config['BASIC_AUTH_USERNAME'] = os.environ['BASIC_AUTH_USERNAME']
    app.config['BASIC_AUTH_PASSWORD'] = os.environ['BASIC_AUTH_PASSWORD']
    basic_auth = BasicAuth(app)
    setup_error_handling(app, error_codes=[400, 401, 403, 404, 405, 500])

    @app.route('/quote', methods=['POST'])
    @basic_auth.required
    @expects_json(quote_schema)
    def quote():
        bitcoin_amount = g.data['bitcoin']
        insurance = Insurance(bitcoin_amount=bitcoin_amount)

        return {
            'monthly_premium': insurance.premium_rounded
        }

    return app
