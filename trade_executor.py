
from config import TICKERS, ALLOCATION
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import yfinance as yf

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("google_credentials.json", scope)
client = gspread.authorize(creds)
log_sheet = client.open("AutoTrader").worksheet("Trade Log")
portfolio = {ticker: {"shares": 0, "avg_price": 0} for ticker in TICKERS}
cash = 1000

def execute_trade(ticker, action, price):
    global cash, portfolio
    shares = int((cash * ALLOCATION) // price)
    if action == "BUY" and shares > 0:
        portfolio[ticker]["shares"] += shares
        portfolio[ticker]["avg_price"] = price
        cash -= shares * price
        log_trade(ticker, "BUY", price, shares)
    elif action == "SELL" and portfolio[ticker]["shares"] > 0:
        cash += portfolio[ticker]["shares"] * price
        log_trade(ticker, "SELL", price, portfolio[ticker]["shares"])
        portfolio[ticker] = {"shares": 0, "avg_price": 0}

def log_trade(ticker, action, price, shares):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_sheet.append_row([now, ticker, action, price, shares, cash])
