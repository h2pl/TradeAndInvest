import pandas as pd
import tushare as ts

# 设置你的token
ts.set_token('bfde54174d8de099c6429d7fdd4e7e89663a8262ead47a441a84301f')


def get_hk_stocks_data():
    # 获取所有港股基本信息
    hk_stock_basic = ts.pro_api().daily(**{
        # "ts_code": "",
        # "trade_date": "",
        "start_date": "20190904",
        "end_date": "20240304",
        "limit": "10",
        "offset": "1"})

    # 过滤市值超过指定阈值的股票
    # large_cap_stocks = hk_stock_basic[hk_stock_basic['market_cap'] > market_cap_threshold]

    # 按照每个股票获取过去3年的日线数据
    stocks_data = {}
    for stock_code in hk_stock_basic['ts_code']:
        try:
            # 获取指定时间段内（例如最近3年）的日线数据
            df = ts.pro_bar(ts_code=stock_code, freq='D', start_date='20190101', end_date='20221231')

            # 确保返回的数据不为空，并且对数据进行预处理，比如转换时间索引为日期格式等
            if not df.empty:
                df['trade_date'] = pd.to_datetime(df['trade_date'])
                df.set_index('trade_date', inplace=True)
                stocks_data[stock_code] = df
        except Exception as e:
            print(f"获取{stock_code}数据时发生错误: {str(e)}")

    return stocks_data

#
# if __name__ == '__main__':
#     # 获取所有市值超过100亿港元的港股数据
#     stocks_data = get_hk_stocks_data()
#     print(stocks_data)
#     # 继续执行回测逻辑...
