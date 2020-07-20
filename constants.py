portfolio_filename = "test_portfolio.csv"
column_names = [
    "Ticker",
    "Amount",
    "Price (USD)",
    "Price (EUR)",
    "Total (USD)",
    "Total (EUR)",
    "Percentage (%)",
]

column_ids = [
    "ticker",
    "amount",
    "usd_price",
    "eur_price",
    "usd_total",
    "eur_total",
    "percent",
]

data_types = {
    "ticker": str,
    "amount": float,
    "usd_price": float,
    "eur_price": float,
    "usd_total": float,
    "eur_total": float,
    "percent": float,
}

editable = {
    "ticker": True,
    "amount": True,
    "usd_price": False,
    "eur_price": False,
    "usd_total": False,
    "eur_total": False,
    "percent": False,
}
