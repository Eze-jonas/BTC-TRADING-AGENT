def should_dca(price, last_dca_price, dca_drop_pct):

    trigger_price = last_dca_price * (
        1 - dca_drop_pct / 100
    )

    return price <= trigger_price