import requests

from json_logic import jsonLogic


class Quote:
    """Represents a Quote object to calculate a client's premium given an amount of Bitcoin."""

    COINDESK_API_URL = 'https://api.coindesk.com/v1/bpi/currentprice.json'
    COMMISSION_ADD_ON = 100
    EXCHANGE_RATE = 17.32

    def __init__(self, bitcoin_amount):
        """Initalize Quote class."""
        self.btc_amount = bitcoin_amount
        self.eur_amount = self.get_bitcoin_price() * bitcoin_amount
        self.zar_amount = self.convert_eur_to_zar()
        self.annual_commission_proportion = self.get_annual_commission_proportion()
        self.montly_commission_proportion = self.annual_commission_proportion / 12
        self.premium = self.calculate_premium()
        self.premium_rounded = round(self.premium, 2)

    def get_bitcoin_price(self):
        """Get the current Bitcoin price (in Euros) from the Coindesk API."""
        response = requests.get(self.COINDESK_API_URL).json()

        return response['bpi']['EUR']['rate_float']

    def convert_eur_to_zar(self):
        """Convert Euros to South African Rands."""
        return self.eur_amount * self.EXCHANGE_RATE

    def get_annual_commission_proportion(self):
        """Determines the commission proportion (decimal percentage) based on the zar_amount."""
        rules = {'if': [
            {'<': [{'var': 'zar_amount'}, 50000]}, 0.015,
            {'<': [{'var': 'zar_amount'}, 500000]}, 0.010, 0.005
        ]}

        data = {'zar_amount': self.zar_amount}

        return jsonLogic(rules, data)

    def calculate_premium(self):
        """Calculates the monthly premium."""
        return (self.montly_commission_proportion * self.zar_amount) + self.COMMISSION_ADD_ON
