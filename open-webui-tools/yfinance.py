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

            if dividends.empty:
                return f"No dividend records found for ticker {ticker}."

            # Get the last 5 dividend payments
            last_five = dividends.tail(5).sort_index(ascending=False)

            # Fetch yield information
            info = stock.info
            yield_pct = info.get("dividendYield", 0)
            if yield_pct:
                yield_pct = yield_pct * 100  # Convert to percentage

            # Format the Markdown response
            response = f"### Dividend Information for {ticker.upper()}\n"
            response += f"- **Dividend Yield:** {yield_pct:.2f}%\n\n"
            response += "| Ex-Dividend Date | Amount ($/€) |\n"
            response += "| :--- | :--- |\n"

            for date, amount in last_five.items():
                date_str = date.strftime("%Y-%m-%d")
                response += f"| {date_str} | {amount:.4f} |\n"

            return response

        except Exception as e:
            return f"Error retrieving data for {ticker}: {str(e)}"

    def get_upcoming_dividend(self, ticker: str) -> str:
        """
        Retrieves the upcoming dividend date if it has been announced.
        :param ticker: The stock symbol.
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            ex_date_timestamp = info.get("exDividendDate")

            if ex_date_timestamp:
                ex_date = datetime.fromtimestamp(ex_date_timestamp).strftime("%Y-%m-%d")
                amount = info.get("dividendRate", "N/A")
                return f"The next dividend for {ticker.upper()} is scheduled (Ex-Date) for **{ex_date}** with an estimated amount of **{amount}**."
            else:
                return f"No confirmed upcoming dividend date found for {ticker.upper()} at this time."

        except Exception as e:
            return f"Error checking upcoming dividend for {ticker}: {str(e)}"
