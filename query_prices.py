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
        "limit": 1000,
        "sort": "cmc_rank",
    }
    try:
        r = requests.get(cmc_url + endpoint_symbols, params)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        raise e
    if r.status_code == 200:
        data = r.json()["data"]
    symbol_list = []
    for currency in data:
        symbol_list.append(currency["symbol"])
    return symbol_list


def get_quotes(symbols):
    symbols_string = ','.join(symbols)
    params = {
        "CMC_PRO_API_KEY": cmc_key,
        "symbol": symbols_string
    }
    try:
        r = requests.get(cmc_url + endpoint_crypto, params)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        raise e
    quotes = dict()
    if r.status_code == 200:
        for symbol in symbols:
            price = r.json()["data"][symbol]["quote"]["USD"]["price"]
            quotes[symbol] = price
        return quotes
    elif r.status_code == 400:
        message = r.json()["status"]["error_message"]
        for symbol in symbols:
            if symbol in message:
                print(f"Request for symbol {symbol} failed ")
                symbols.remove(symbol)
        return get_quotes(symbols)


def get_fiat_conversion(source_symbol, target_symbol):
    params = {"CMC_PRO_API_KEY": cmc_key,
              "amount": 1.0,
              "symbol": source_symbol,
              "convert": [target_symbol]}

    r = requests.get(cmc_url + endpoint_fiat, params)
    rate = r.json()["data"]["quote"][target_symbol]["price"]
    return rate
