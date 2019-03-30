import math

import bs4
import requests
from flask import render_template, request

from model import app, Item


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/handle_data', methods=['POST'])
def handle_data():
    print(request.form)
    url = request.form.get("link")
    res = requests.get(url.strip(), headers={
        'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/37.0.2062.120 Safari/537.36'})
    textFile = res.text

    week = 5
    rate = 76
    shipping = 0
    tax = 15
    name = ""
    cdn = 0.0
    price = 0.0
    taka = 0.0
    advnc_req = 0.0
    if url.startswith('https://www.amazon.ca'):
        amazon = bs4.BeautifulSoup(textFile, 'html.parser')

        price = amazon.find_all('span', attrs={'id': ['priceblock_ourprice', 'priceblock_dealprice']})[
            0].getText().strip()

        price = price.replace('CDN$', '').strip()
        cdn = math.ceil((float(price) + ((float(price) * 15) / 100)))
        tax = (float(price) * 15) / 100
        taka = cdn * rate
        advnc_req = "{:,}".format(math.ceil((taka / 2.5) / 100) * 100)

        taka = "{:,}".format(taka)
        cdn = "{:,}".format(cdn)

        name = 'Amazon Prime'

    elif url.startswith('https://www.aldoshoes.com'):

        aldo = bs4.BeautifulSoup(textFile, 'html.parser')
        original_price = float(aldo.find('span', attrs={'class': 'c-product-price__formatted-price'})
                               .text.replace('$', '').strip())
        discounted__price = aldo.find('span', attrs={
            'class': 'c-product-price__formatted-price c-product-price__formatted-price--is-reduced'})

        if discounted__price is not None:
            discounted__price = discounted__price.text.replace('$', '')
            cdn = float(discounted__price)

        else:
            cdn = original_price

        if cdn < 70:
            tax = float(cdn + 6) * 15 / 100
            shipping = 6
        else:
            tax = float(cdn) * 15 / 100

        taka = cdn * rate
        advnc_req = "{:,}".format(math.ceil((taka / 2.5) / 100) * 100)

        taka = "{:,}".format(taka)
        cdn = "{:,}".format(cdn)

        name = "Aldo"


    elif url.startswith('https://www.fossil.com/ca/'):
        fossil = bs4.BeautifulSoup(textFile, 'html.parser')
        name = 'Fossil'

        price = fossil.find('div', attrs={
            'class': ["col-md-12 product-price-display text-display-4 pdp-margin-bottom hidden-xs "]}).getText().strip()

        discount = fossil.find_all('span', attrs={'class': 'text-danger'})
        price = price[4:10]

        if discount != []:
            discount = fossil.find_all('span', attrs={'class': 'text-danger'})[0].getText().strip()
            discount = discount[4:]
            price = float(discount) + 0.25
            tax = float(price) * 15 / 100
            cdn = math.ceil(((float(price) + 0.25) + ((float(price) + 0.25) * 15) / 100))
        else:
            price = float(price) + 0.25
            tax = float(price) * 15 / 100
            cdn = math.ceil(((float(price) + 0.25) + ((float(price) + 0.25) * 15) / 100))

        taka = cdn * rate
        advnc_req = "{:,}".format(math.ceil((taka / 2.5) / 100) * 100)
        taka = "{:,}".format(taka)
        cdn = "{:,}".format(cdn)

    item = Item(
        vendor=name,
        price=price,
        tax=tax,
        shipping_cost=shipping,
        total=cdn,
        conversion_rate=rate,
        aar=advnc_req,
        week=week,
        total_bdt=taka
    )
    return render_template("item-details.html", item=item)


def format_placeholders(name, price, tax, shipping, cdn, taka, advnc_req, week, rate):
    body = f"\n Hello! Thanks for your Inquiry!" \
        f"\nHere is the detail for the product(s):" \
        f"\nPrice - ${str(price)}" \
        f"\nTax (in Canada) - {tax} " \
        f"\n+\nShipping ({name}) - {shipping}" \
        f"\n------------------------------" \
        f"\nTotal - ${cdn}" \
        f"\nIn BDT ({rate}TK/CAD$) - TK {taka}" \
        f"\n+" \
        f"\nWeight Charge (To be Added After Product Arrival to BD)" \
        f"\nFor products <100g = 150TK Flat" \
        f"\nFor products >100g up to 2kg = 160TK/100g" \
        f"\nFor products >2kg = 1700TK/Kg" \
        f"\n----------------------------------" \
        f"\nAdvance Required - TK {advnc_req}" \
        f"\nExpected Shipment Arrival:" \
        f"\n{week} Weeks Minimum" \
        f"\n------------------------------"
    return body
