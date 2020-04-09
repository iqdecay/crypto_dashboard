import os
import dash
from dash.dependencies import Input, Output, State
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
from numpy import nan
from constants import column_names, column_ids, editable, data_types
from query_prices import get_quotes, get_fiat_conversion, get_available_symbols

# pd.options.display.float_format = '{:.2f}'.format
if os.path.exists("portfolio.csv"):
    print("Loading portfolio")
    try:
        df = pd.read_csv("portfolio.csv", dtype=data_types)
    except:
        raise FileNotFoundError("Unable to load portfolio but file exists")
else:
    df = pd.DataFrame(columns=column_ids)


def significant(x, n=4):
    # Round down x to n significant numbers
    float_string = "%s" % float(f"%.{n}g" % x)
    return float(float_string)


USD_TO_EUR = significant(get_fiat_conversion("USD", "EUR"), 4)

quotes = dict()
quotes = get_quotes(df["ticker"])

available_symbols = get_available_symbols()

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__,
                show_undo_redo=True,
                external_stylesheets=external_stylesheets)

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    dash_table.DataTable(
                        id='data-table',
                        columns=[{
                            'name': column_names[i],
                            'id': column_ids[i],
                            'deletable': False,
                            'editable': editable[column_ids[i]],
                            'renamable': False,
                            'format': {
                                "locale":
                                    {'symbol': ["$", '#']},
                                'nully': ""
                            }
                        } for i in range(0, 6)],
                        data=df.to_dict('records'),
                        editable=True,
                        data_timestamp=0,
                        style_cell={'fontSize': 12},
                    ), width=6),
                dbc.Col(
                    dcc.Graph(id='pie-chart'), width=6),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(dbc.Button('Add Row', id='add-row-button', n_clicks=0,
                                   n_clicks_timestamp=0), width=4),
                dbc.Col(dbc.Button('Save the table !', id='save-data-button', n_clicks=0), width=4),
                dbc.Col(
                    [
                        html.Div("Total amount", id='display_total'),
                        html.Div(id='hidden-save-button-div', style={'display': 'none'}),
                        html.Div(id='hidden-row-button-div', style={'display': 'none'}),
                    ]
                    , width=4
                ),
            ]),
        dbc.Row(
            dbc.Col(
            )),
    ],
    style={
        "width": '90%',
    }
)


@app.callback(
    [Output('data-table', 'data'),
     Output('display_total', 'children')],
    [Input('data-table', 'data_timestamp'),
     Input('add-row-button', 'n_clicks_timestamp')],
    [State('data-table', 'data'),
     State('display_total', 'children')])
def update_data_with_user_input(data_timestamp, click_timestamp, data, total):
    # Use timestamp comparison to understand where the input comes from
    if data_timestamp >= click_timestamp:
        # Update the table with the new values
        total_amount = 0
        for row in data:
            symbol = row["ticker"]
            if symbol not in available_symbols:
                row["ticker"] = ""
                return data
            if symbol not in quotes:
                quotes[symbol] = get_quotes([symbol])[symbol]
            row['usd_price'] = significant(quotes[row["ticker"]])
            row['eur_price'] = significant(row['usd_price'] * USD_TO_EUR)
            try:
                row['amount'] = significant(float(row['amount']))
                row['eur_total'] = significant(row['eur_price'] * row['amount'])
                total_amount += row['eur_total']
            except (TypeError, ValueError):
                row['amount'] = ''

        for row in data:
            if row['amount'] != '':
                amount = row['eur_total'] / total_amount
                row['percent'] = significant(amount * 100,2)
    elif data_timestamp < click_timestamp:
        data.append({column_ids[i]: '' for i in range(len(column_ids))})
        total_amount = total
    return data, significant(total_amount)


@app.callback(
    Output('pie-chart', 'figure'),
    [Input('data-table', 'data')],
)
def update_pie_chart(data):
    n_rows = len(data)
    return {
        'data': [{
            'title': "Portfolio allocation",
            'showlegend': False,
            'type': 'pie',
            'values': [data[i]["percent"] for i in range(n_rows)],
            'labels': [data[i]["ticker"] for i in range(n_rows)],
            'hole': 0.6,
            'textinfo': 'label+percent',
            'uniformtext_mode':"hide",
        }]
    }


@app.callback(
    Output('hidden-save-button-div', 'children'),
    [Input('save-data-button', 'n_clicks')],
    [State('data-table', 'data')])
def save_data_table(n_clicks, data):
    if n_clicks != 0:
        new_df = pd.DataFrame.from_records(data)
        new_df.replace("", nan, inplace=True)
        new_df = new_df.dropna("index", thresh=2)
        new_df.to_csv("portfolio.csv", index=False)


if __name__ == '__main__':
    app.run_server(debug=True)
