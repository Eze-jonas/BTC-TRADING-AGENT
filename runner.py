from scripts.states.portfolio import portfolio
from scripts.values.portfolio_value import portfolio_value

from scripts.executor.execution import buy
from scripts.executor.execution import sell


buy(portfolio, 50000, 1000)

print(portfolio)
print(portfolio_value(portfolio))

portfolio["current_price"] = 55000

print(portfolio_value(portfolio))

sell(portfolio, 55000)

print(portfolio)
print(portfolio_value(portfolio))