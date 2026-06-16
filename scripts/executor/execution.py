# BUY LOGIC
def buy(portfolio, price, amount):

    if amount > portfolio["cash"]:
        amount = portfolio["cash"]

    qty = amount / price

    portfolio["cash"] -= amount
    portfolio["btc_holdings"] += qty
    portfolio["current_price"] = price

    portfolio["trades"].append({
        "type": "BUY",
        "price": price,
        "amount": amount,
        "qty": qty
    })
    
    # SELL LOGIC
def sell(portfolio, price):

    qty = portfolio["btc_holdings"]

    if qty <= 0:
        return

    proceeds = qty * price

    portfolio["cash"] += proceeds
    portfolio["btc_holdings"] = 0
    portfolio["current_price"] = price

    portfolio["trades"].append({
        "type": "SELL",
        "price": price,
        "qty": qty,
        "proceeds": proceeds
    })
    
    