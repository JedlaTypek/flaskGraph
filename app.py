from flask import Flask, render_template
import requests
from datetime import datetime

app = Flask(__name__)


def get_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/ethereum/market_chart?vs_currency=usd&days=30"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None


@app.route("/")
def index():
    data = get_crypto_data()
    if data is None:
        return "Nepodařilo se získat data", 500

    dates = [datetime.fromtimestamp(point[0] // 1000).strftime('%Y-%m-%d %H:%M') for point in data["prices"]]
    prices = [point[1] for point in data["prices"]]

    # Předáme data přímo do šablony
    return render_template("index.html", dates=dates, prices=prices)


if __name__ == "__main__":
    app.run(debug=True)