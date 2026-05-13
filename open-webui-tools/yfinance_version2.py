import json
from datetime import datetime
from typing import Any, Dict

import yfinance as yf


class Tools:
    def __init__(self):
        pass

    def get_dividend_report(self, ticker: str) -> str:
        """
        Recupera en una sola llamada el historial reciente y el próximo dividendo anunciado.
        :param ticker: El símbolo de la acción (ej. 'TEF.MC').
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            dividends = stock.dividends

            report = {
                "ticker": ticker.upper(),
                "currency": info.get("currency", "USD"),
                "history": [],
                "upcoming": None,
            }

            # 1. Procesar Historial (Últimos 5)
            if not dividends.empty:
                last_five = dividends.tail(5).sort_index(ascending=False)
                for date, amount in last_five.items():
                    report["history"].append(
                        {
                            "date": date.strftime("%Y-%m-%d"),
                            "amount": round(float(amount), 4),
                            "status": "HISTÓRICO",
                        }
                    )

            # 2. Procesar Próximo
            ex_date_timestamp = info.get("exDividendDate")
            if ex_date_timestamp:
                report["upcoming"] = {
                    "date": datetime.fromtimestamp(ex_date_timestamp).strftime(
                        "%Y-%m-%d"
                    ),
                    "amount": info.get("dividendRate"),
                    "status": "ANUNCIADO",
                }

            return json.dumps(report)
        except Exception as e:
            return json.dumps({"error": str(e)})
