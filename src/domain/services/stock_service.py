class StockService:
    def get_price_alert(self, stock):
        if stock.close > 500:
            return f"Alerta: El precio de {stock.ticker} ha superado los $500."
        return None
