import os
import pandas as pd
from flask import Flask, jsonify, render_template
from sqlalchemy import create_engine
import json

basedir = os.path.abspath(os.path.dirname(__file__))


engine = create_engine(
    "postgresql://odmyqxza:QBXiWB5oehN0PzjCAYU2-Ucj1WW36i7f@salt.db.elephantsql.com:5432/odmyqxza")

app = Flask(__name__)
@app.route("/")
def home():
    """List all available api routes."""
    # return "/api/v1.0/"
    bs_results = pd.read_sql("select * from balance_sheet", engine)
    bs_results.assets = bs_results.current_assets + bs_results.noncurrent_assets
    bs_data = bs_results.to_dict(orient="records")
    return render_template(os.path.join('home.html'), bs_data=bs_data)



@app.route('/<ticker>')
def company_page(ticker):
    bs_results = pd.read_sql("select * from balance_sheet", engine)
    bs_data = jsonify(bs_results.to_dict(orient="records"))
    is_results = pd.read_sql("select * from income_statement", engine)
    is_data = jsonify(is_results.to_dict(orient="records"))
    return render_template(os.path.join(ticker+'.html'), bs_data=bs_data, is_data=is_data, ticker=ticker)

@app.route('/team')
def team_page():
    return render_template(os.path.join('team.html'))


# first der.
@app.route("/balance")
def balance():
    print("Session created")
    """display balance sheet"""
    bs_results = pd.read_sql("select * from balance_sheet", engine)
    bs_data = jsonify(bs_results.to_dict(orient="split"))
    return bs_data
  
@app.route("/income")
def income():
    print("Session created")
    """display income statement"""
    is_results = pd.read_sql("select * from income_statement", engine)
    # is_tickers = list(is_results.ticker)
    is_data = jsonify(is_results.to_dict(orient="records"))
    return is_data
if __name__ == '__main__':
    app.run(debug=True)