
import openai
from config import OPENAI_API_KEY, GPT_MODEL, GPT_ENABLED
import numpy as np

openai.api_key = OPENAI_API_KEY

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs)).iloc[-1]

def generate_tech_signal(data):
    close = data['Close']
    sma_short = close.rolling(window=5).mean().iloc[-1]
    sma_long = close.rolling(window=20).mean().iloc[-1]
    rsi = compute_rsi(close)
    signal = "HOLD"
    if sma_short > sma_long and rsi < 70:
        signal = "BUY"
    elif sma_short < sma_long and rsi > 30:
        signal = "SELL"
    return signal, rsi

def gpt_decision(ticker, price, rsi, sentiment):
    if not GPT_ENABLED:
        return "HOLD", 0.5
    prompt = (f"The stock {ticker} is trading at {price}. RSI is {rsi}. "
              f"Sentiment score: {sentiment}. Should I Buy, Hold, or Sell? Confidence (0-1).")
    response = openai.ChatCompletion.create(
        model=GPT_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    text = response.choices[0].message.content
    decision = "HOLD"
    confidence = 0.5
    if "buy" in text.lower(): decision = "BUY"
    elif "sell" in text.lower(): decision = "SELL"
    import re
    match = re.search(r"(\d\.\d+)", text)
    if match: confidence = float(match.group(1))
    return decision, confidence
