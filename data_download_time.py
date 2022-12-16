from binance.cm_futures import CMFutures
import pandas as pd
from datetime import datetime

four_day_as_ts = 345600000
two_day_as_ts = 172800000
one_day_as_ts = 86400000
half_day_as_ts = 43200000

class DataCsvTime:

    RESOLUTION = {"1m": 60, "5m": 300, "1h": 3600, "1d": 86400}

    def __init__(self, binance_client_data):
        self.binance_client_data = binance_client_data

    def generate_klines_from_time(self,market_name, interval, iterations):
        iterations = iterations*2
        last_ts_server = self.binance_client_data.time()['serverTime']
        earlier_ts_server = last_ts_server - half_day_as_ts
        columns = 'Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'NumberOfTrades', 'TakerBuyVolume'
        df = pd.DataFrame(columns=columns)
        count = 0
        cm_future_obj = isinstance(self.binance_client_data,CMFutures)

        for x in range(iterations):
            my_kline = self.binance_client_data.klines(market_name, interval, startTime=earlier_ts_server, endTime=last_ts_server, limit = 1000)
            if cm_future_obj:
                DataCsvTime.change_list_cm(my_kline)
            elif cm_future_obj is False:
                DataCsvTime.change_list_um(my_kline)
            my_kline.reverse()
            print(my_kline)
            print('ksw')
            last_ts_server = last_ts_server - half_day_as_ts
            earlier_ts_server = last_ts_server - half_day_as_ts

            for x in my_kline:
                df.loc[count] = x
                count += 1
        iterations = iterations/2
        df.to_csv(market_name+" "+interval+ " "+ str(iterations)+'.csv', index=False)
        return df

    #https: // binance - docs.github.io / apidocs / delivery / en /  # kline-candlestick-data
    @staticmethod
    def change_list_cm(list_to_change):
        for x in list_to_change:
            time_date_from_ts = datetime.fromtimestamp(x[0] / 1000)
            date_from_ts = time_date_from_ts.strftime("%d/%m/%Y")
            time_from_ts = time_date_from_ts.strftime("%H:%M:%S")
            del x[11]  # Ignore
            del x[10]  # TakerBuyBaseAssetVolume
            del x[7]  # BaseAssetVolume
            del x[6]  # CloseTime
            del x[0]  # EndTime

            x.insert(0, time_from_ts)
            x.insert(0, date_from_ts)

    #https: // binance - docs.github.io / apidocs / futures / en /  # kline-candlestick-data
    @staticmethod
    def change_list_um(list_to_change):
        for x in list_to_change:
            time_date_from_ts = datetime.fromtimestamp(x[0] / 1000)
            date_from_ts = time_date_from_ts.strftime("%d/%m/%Y")
            time_from_ts = time_date_from_ts.strftime("%H:%M:%S")
            del x[11]  # Ignore
            del x[10]  # TakerBuyBaseAssetVolume
            del x[7]  # BaseAssetVolume
            del x[6]  # CloseTime
            del x[0]  # EndTime

            x.insert(0, time_from_ts)
            x.insert(0, date_from_ts)

# btcbusd dane od 12.1.2021 to jest około 700 dni

# 1m
# 3m
# 5m
# 15m
# 30m
# 1h
# 2h
# 4h
# 6h
# 8h
# 12h
# 1d
# 3d
# 1w
# 1M

# d['startDate'] = dt.strftime("%Y/%m/%d")
# d['startTime'] = dt.strftime("%H:%M:%S")

#     UM futures klines
# [
#   [
#     1499040000000,      // Open time               -0 usuwamy ponieważ mamy już dane
#     "0.01634790",       // Open
#     "0.80000000",       // High
#     "0.01575800",       // Low
#     "0.01577100",       // Close
#     "148976.11427815",  // Volume
#     1499644799999,      // Close time              -6
#     "2434.19055334",    // Quote asset volume      -7
#     308,                // Number of trades
#     "1756.87402397",    // Taker buy base asset volume
#     "28.46694368",      // Taker buy quote asset volume    -10
#     "17928899.62484339" // Ignore.                          -11
#   ]
# ]


# [  CM futures klines
#   [
#     1591258320000,          // Open time
#     "9640.7",               // Open
#     "9642.4",               // High
#     "9640.6",               // Low
#     "9642.0",               // Close (or latest price)
#     "206",                  // Volume
#     1591258379999,          // Close time                       -6
#     "2.13660389",           // Base asset volume               -7
#     48,                     // Number of trades
#     "119",                  // Taker buy volume
#     "1.23424865",           // Taker buy base asset volume    -10
#     "0"                     // Ignore.                        -11
#   ]
# ]