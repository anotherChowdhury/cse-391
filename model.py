from flask import Flask

app = Flask(__name__)


class Item:

    def __init__(self, vendor, price, tax, shipping_cost, total, conversion_rate, aar, week, total_bdt):
        self.vendor = vendor
        self.price = price
        self.tax = tax
        self.shipping_cost = shipping_cost
        self.total = total
        self.conversion_rate = conversion_rate
        self.advanced_amount_required = aar
        self.week = week
        self.total_in_bdt = total_bdt
