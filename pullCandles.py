import requests
import json
import datetime
import time
import matplotlib # pip install matplotlib
import matplotlib.pyplot

#https://graphs2.coinmarketcap.com/currencies/bitcoin/1367174841000/1397952000000/

url = "https://graphs2.coinmarketcap.com/currencies/bitcoin/"

start = 1367174841000
diff = 8640000000
end = int(time.time()) * 1000

market_cap_history = []
price_usd_history = []
volume_usd_history = []

fr = start
to = start + diff
while fr < end:
    urlFrTo = url + str(fr) + "/" + str(to) + "/"
    print "GET:  " + urlFrTo
    history = json.loads(requests.get(urlFrTo).content)
    market_cap_history = market_cap_history + history["market_cap_by_available_supply"]
    price_usd_history = price_usd_history + history["price_usd"]
    volume_usd_history = volume_usd_history + history["volume_usd"]
    fr = to
    to = to + diff
    if(to > end): 
        to = end

print str(len(price_usd_history)) + " records saved"

def getCandleRecords(records):
    candleRecords = []
    currentTime = str(datetime.datetime.fromtimestamp(records[0][0] / 1000))[:10]
    currentData = []
    for record in records:
        data = record[1]
        time = str(datetime.datetime.fromtimestamp(record[0] / 1000))[:10]
        if(currentTime == time):
            currentData.append(data)
        if(currentTime != time or record == records[len(records)-1]):
            candleRecords.append(
                {
                    "time": time,
                    "open": currentData[0],
                    "close": currentData[len(currentData)-1],
                    "max": max(currentData),
                    "min": min(currentData)
                }
            )
            currentData = []
            currentTime = time
    return candleRecords
    
market_cap_candles = getCandleRecords(market_cap_history)
price_usd_candles = getCandleRecords(price_usd_history)
volume_usd_candles = getCandleRecords(volume_usd_history)

with open("market_cap_candles.json", "w") as jsonFile:
    jsonFile.write(json.dumps(market_cap_candles, indent=2))

with open("price_usd_candles.json", "w") as jsonFile:
    jsonFile.write(json.dumps(price_usd_candles, indent=2))

with open("volume_usd_candles.json", "w") as jsonFile:
    jsonFile.write(json.dumps(volume_usd_candles, indent=2))

print "Done!"