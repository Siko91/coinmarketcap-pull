import requests
import json
import matplotlib # pip install matplotlib
import matplotlib.pyplot

#   https://coinmarketcap.com/api/#endpoint_listings
#   https://api.coinmarketcap.com/v2/listings/
#   https://api.coinmarketcap.com/v2/ticker/

#   Task 1: Get Top 10 currencies by market cap

arr = json.loads(
        requests.get("https://api.coinmarketcap.com/v2/ticker/").content
    )["data"].values()

top = sorted(
        arr, 
        key= lambda i: i["circulating_supply"] * i["quotes"]["USD"]["price"], 
        reverse=True
    )[:10]

#   https://graphs2.coinmarketcap.com/currencies/bitcoin/

#   Task 2: Get the trading history of the top 10 coins

historyOfTop = []
for i in top:
    history = json.loads(requests.get(
        "https://graphs2.coinmarketcap.com/currencies/" + i["website_slug"] + "/"
    ).content)
    historyOfTop.append(history)

#   Task 3: Make a cool chart of the history

traces = []
count = 0
for i in historyOfTop:
    x_axis = map(lambda tpls: tpls[0], i["price_usd"])
    y_axis = map(lambda tpls: tpls[1], i["price_usd"])
    matplotlib.pyplot.plot(x_axis, y_axis, label=top[count]["website_slug"])
    count = count + 1

matplotlib.pyplot.title("Prices USD")
matplotlib.pyplot.legend()
matplotlib.pyplot.show()