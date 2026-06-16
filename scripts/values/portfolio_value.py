def portfolio_value(portfolio):

    return (
        portfolio["cash"]
        + portfolio["btc_holdings"]
        * portfolio["current_price"]
    )