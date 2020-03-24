import requests
import yaml
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

API_KEY_FILE = "auth.yaml"
cmc_url = "https://pro-api.coinmarketcap.com/v1/"
endpoint_crypto = "cryptocurrency/quotes/latest"
endpoint_fiat = "tools/price-conversion"
endpoint_symbols = "cryptocurrency/map"

with open(API_KEY_FILE, 'r') as api_key_file:
    api_key = yaml.safe_load(api_key_file)
cmc_key = api_key[0]["coinmarketcap"]


def get_available_symbols():
    params = {
        "CMC_PRO_API_KEY": cmc_key,
    }
    r = requests.get(cmc_url + endpoint_symbols, params)


def get_quotes(symbol):
    params = {
        "CMC_PRO_API_KEY": cmc_key,
        "symbol": symbol
    }
    try:
        r = requests.get(cmc_url + endpoint_crypto, params)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        raise e
    if r.status_code == 200:
        price = r.json()["data"][symbol]["quote"]["USD"]["price"]
        return price
    else:
        status = r.status_code
        message = r.json()["status"]["error_message"]
        print(f"Request for symbol {symbol} failed with status {status} : "
              f"{message}")
        return None


def get_fiat_conversion(source_symbol, target_symbol):
    params = {"CMC_PRO_API_KEY": cmc_key,
              "amount": 1.0,
              "symbol": source_symbol,
              "convert": [target_symbol]}

    r = requests.get(cmc_url + endpoint_fiat, params)
    rate = r.json()["data"]["quote"][target_symbol]["price"]
    return rate
