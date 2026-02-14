from __future__ import annotations


class Broker:
    def __init__(self, cash: float = 1_000_000):
        if cash < 0:
            raise ValueError("cash must be nonnegative")
        self.cash = float(cash)
        self.position = 0

    def market_order(self, side: str, qty: int, price: float) -> None:
        if side not in ("buy", "sell"):
            raise ValueError("side must be 'buy' or 'sell'")
        if not isinstance(qty, int) or qty <= 0:
            raise ValueError("qty must be a positive int")
        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError("price must be positive")

        cost = float(qty) * float(price)

        if side == "buy":
            if self.cash < cost:
                raise ValueError("insufficient cash")
            self.cash -= cost
            self.position += qty
        else:
            if self.position < qty:
                raise ValueError("insufficient shares")
            self.position -= qty
            self.cash += cost

    def equity(self, last_price: float) -> float:
        if not isinstance(last_price, (int, float)) or last_price <= 0:
            raise ValueError("last_price must be positive")
        return float(self.cash) + float(self.position) * float(last_price)
