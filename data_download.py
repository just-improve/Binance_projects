from binance.cm_futures import CMFutures
import pandas as pd
from datetime import datetime

class DataCsv:
    total_day_minutes = 1440

    def __init__(self, binance_client_data):
        self.binance_client_data = binance_client_data

    @staticmethod
    def covert_interval_to_days(interval, num_days):
        num_of_klines = 0
        minutes_total = num_days * DataCsv.total_day_minutes
        if interval == '1m':
            num_of_klines = minutes_total / 1

        elif interval == '5m':
            num_of_klines = minutes_total / 5

        elif interval == '15m':
            num_of_klines = minutes_total / 15


        return num_of_klines

    @staticmethod
    def generate_num_of_klines(self_obj, market_name, interval, num_days):
        number_of_klines = int(DataCsv.covert_interval_to_days(interval, num_days))
        my_kline = self_obj.binance_client_data.klines(market_name, interval, limit=number_of_klines)
        return my_kline

    @staticmethod
    def change_list(list_to_change):
        for x in list_to_change:
            time_date_from_ts = datetime.fromtimestamp(x[0] / 1000)
            date_from_ts = time_date_from_ts.strftime("%d/%m/%Y")
            time_from_ts = time_date_from_ts.strftime("%H:%M:%S")
            del x[11]   #Ignore
            del x[10]   #TakerBuyBaseAssetVolume
            del x[7]    #BaseAssetVolume
            del x[6]    #CloseTime
            del x[0]    #EndTime

            x.insert(0, time_from_ts)
            x.insert(0, date_from_ts)

    def klin_to_csv(self, market_name='BTCUSD_PERP', interval='15m', days=2):

        my_kline = DataCsv.generate_num_of_klines(self, market_name, interval, days)
        print(my_kline)
        DataCsv.change_list(my_kline)
        print(my_kline)


        #               0       1       2      3     4         5        6                 7            8                   9                10                   11
        columns = 'OpenTime', 'Open','High','Low','Close','Volume','CloseTime','BaseAssetVolume','NumberOfTrades','TakerBuyVolume','TakerBuyBaseAssetVolume','Ignore'

        columns2 = 'OpenTime', 'Open','High','Low','Close','Volume','NumberOfTrades','TakerBuyVolume'
        #6           #7 oi            #8 fullname   #9 aux1     #10 aux2
        columns3 = 'Date', 'Time','Open','High','Low','Close','Volume','NumberOfTrades','TakerBuyVolume'


        df = pd.DataFrame(columns=columns3)
        count = 0
        for x in my_kline:
            df.loc[count]=x
            count+=1
        print(df)
        return df
myList = [1,2,3,4,5]

# DataCsv.change_list(myList)
# print(myList)

print(datetime.strptime('24052010', '%d%m%Y').date())