import json
from datetime import datetime
from typing import Any, Dict

import yfinance as yf


class Tools:
    def __init__(self):
        pass

    def get_stock_dividends(self, ticker: str) -> str:
        """
        Retrieves the recent dividend history and current yield for a given stock or ETF.
        :param ticker: The stock symbol (e.g., 'PG', 'MSFT', 'ITX.MC').
        """
        try:
            stock = yf.Ticker(ticker)

            # Fetch dividend history
            dividends = stock.dividends

            # Fetch yield information
            info = stock.info
            yield_pct = info.get("dividendYield", 0)
            if yield_pct:
                yield_pct = yield_pct * 100  # Convert to percentage

            data = {
                "ticker": ticker.upper(),
                "dividend_yield_percentage": round(yield_pct, 2) if yield_pct else 0,
                "recent_dividends": []
            }

            if not dividends.empty:
                # Get the last 5 dividend payments
                last_five = dividends.tail(5).sort_index(ascending=False)
                for date, amount in last_five.items():
                    data["recent_dividends"].append({
                        "date": date.strftime("%Y-%m-%d"),
                        "amount": round(float(amount), 4)
                    })

            return json.dumps(data)

        except Exception as e:
            return json.dumps({"error": f"Error retrieving data for {ticker}: {str(e)}"})

    def get_upcoming_dividend(self, ticker: str) -> str:
        """
        Retrieves the upcoming dividend date if it has been announced.
        :param ticker: The stock symbol.
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            ex_date_timestamp = info.get("exDividendDate")
            
            data = {
                "ticker": ticker.upper(),
                "ex_dividend_date": None,
                "dividend_rate": info.get("dividendRate")
            }

            if ex_date_timestamp:
                data["ex_dividend_date"] = datetime.fromtimestamp(ex_date_timestamp).strftime("%Y-%m-%d")

            return json.dumps(data)

        except Exception as e:
            return json.dumps({"error": f"Error checking upcoming dividend for {ticker}: {str(e)}"})
