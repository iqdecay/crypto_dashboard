# Cryptocurrency dashboard :
You can create a portfolio simply by adding rows to the table, the total
value of the portfolio is updated in real time.
## Usage : 

`pip install -r requirements.txt`

Then, in `auth.yaml`, put your Coinmarketcap Pro API key

Running the server : 
`python3 app.py`

Then go to 127.0.0.1:8050 in your browser 

## TODO :
- [x] Add error checking for requests
- [x] Query eur to usd on cmc
- [x] Load and save portfolio from disk
- [x] Allow adding a row in the table
- [x] Get list of available symbols from CMC
- [x] Ticker format validation
- [x] Function for rounding numbers
- [x] Query new symbol when added (use dictionary initialized at app launch)
- [x] Group API calls to avoid rate limit exceeded
- [x] Add total amount
- [ ] Group small values together in pie chart
- [ ] Format currency
- [ ] Order by percentage
- [ ] Comments and documentation
- [ ] Button for toggling row deletion
- [ ] Add form for buying a crypto, with its usd and btc/eth price,
and add a tick in the data
- [ ] Register history of what has happened
- [ ] When app opens, add a price projection for the old portfolios
