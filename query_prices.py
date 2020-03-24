import requests
import yaml
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

API_KEY_FILE = "auth.yaml"
cmc_url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
cmc_url_fiat = "https://pro-api.coinmarketcap.com/v1/tools/price-conversion"

with open(API_KEY_FILE, 'r') as api_key_file:
    api_key = yaml.safe_load(api_key_file)
cmc_key = api_key[0]["coinmarketcap"]


def get_quotes(*symbols):
    symbols = list(symbols)
    symbols_string = ",".join(symbols).upper()
    params = {
        "CMC_PRO_API_KEY": cmc_key,
        "symbol": symbols_string
    }
    try:
        r = requests.get(cmc_url, params)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        raise e
    if r.status_code == 200:
        quotes = {}
        data = r.json()["data"]
        for symbol in symbols:
            usd_price = data[symbol]["quote"]["USD"]["price"]
            quotes[symbol] = usd_price
        return quotes
    else:
        status = r.status_code
        message = r.json()["status"]["error_message"]
        raise ValueError(f"Request failed with status {status} : {message}")


def get_fiat_conversion(source_symbol, target_symbol):
    params = {"CMC_PRO_API_KEY": cmc_key,
              "amount": 1.0,
              "symbol": source_symbol,
              "convert": [target_symbol]}

    r = requests.get(cmc_url_fiat, params)
    rate = r.json()["data"]["quote"][target_symbol]["price"]
    return rate
