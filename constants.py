column_names = [
    "Ticker",
    "Amount",
    "Price (USD)",
    "Price (EUR)",
    "Total (EUR)",
    "Percentage (%)",
]

column_ids = [
    "ticker",
    "amount",
    "usd_price",
    "eur_price",
    "eur_total",
    "percent",
]

data_types = {
    "ticker": str,
    "amount": float,
    "usd_price": float,
    "eur_price": float,
    "eur_total": float,
    "percent": float,
}

editable = {
    "ticker": True,
    "amount": True,
    "usd_price": False,
    "eur_price": False,
    "eur_total": False,
    "percent": False,
}
