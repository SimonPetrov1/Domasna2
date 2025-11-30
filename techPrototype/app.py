import os

import pandas as pd
from flask import Flask, render_template, abort
app = Flask(__name__)
#----------LOAD DATA----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "all_coins.csv")

# Load CSV once at startup
df = pd.read_csv(DATA_PATH)

# Ensure we have these columns: time, symbol, open, high, low, close, volume
# Convert UNIX time to date for easier display

df["date"] = pd.to_datetime(df["time"], unit = "s").dt.date

#----------ROUTES-------------

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/coins")
def coins():
    symbols = sorted(df["symbol"].unique())
    return render_template("coins.html", symbols=symbols)


@app.route("/coin/<symbol>")
def coin_detail(symbol):
    coin_df = df[df["symbol"] == symbol].sort_values("date")
    if coin_df.empty:
        abort(404)

    rows = coin_df.to_dict(orient="records")
    return render_template("coin_detail.html", symbol=symbol, rows=rows)


if __name__ == "__main__":
    app.run(debug=True)
