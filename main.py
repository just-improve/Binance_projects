from binance.cm_futures import CMFutures
from binance.um_futures import UMFutures
from datetime import datetime
import pandas as pd
import time
from data_download import DataCsv
from data_download_time import DataCsvTime


if __name__ == '__main__':
    #binance_client = CMFutures(base_url="https://fapi.binance.com")
    timestamptime = time.time()

    binance_client_cm = CMFutures()
    binance_client_um = UMFutures()

    data_to_csv_cm = DataCsvTime(binance_client_cm)
    data_to_csv_um = DataCsvTime(binance_client_um)


    df_obj = data_to_csv_um.generate_klines_from_time('BTCBUSD','15m',900)
    # print(df_obj)






# 1667548800024   1667577600017
# to jest 8 godzin
# df_obj = data_to_csv_cm.generate_klines_from_time('BTCUSD_PERP', '5m', 10)
