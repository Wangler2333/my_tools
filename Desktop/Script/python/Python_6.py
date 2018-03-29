#!/usr/bin/python

stock = {
    "name"   : "GOOG",
    "shares" : 100,
    "price"  : 490.10,
}

prices = {
    "GOOG"   : 490.10,
    "AAPL"   : 123.50,
    "IBM"    : 91.50,
    "MSFT"   : 52.13,
}

print stock["name"]
print stock["shares"] * stock["price"]

stock["Date"] = "June 7, 2007"

print stock
print prices

if "SCOX" in prices:
    p = prices["SCOX"]
else:
    p = 0.0

#p = prices.get("SCOX",0.0)
