import backtrader as bt

import yfinance as yf

# 用股票的代码来指定想要下载数据的股票，
# 例如 "AAPL" 是苹果公司的股票代码，"0700.HK" 是腾讯控股在港股的代码
stock_code = "AAPL"

# 用yfinance下载股票数据
df = yf.download(stock_code, start="2020-01-01", end="2024-01-01")

# 查看数据
# data.head()
print(df.head())


# 策略定义
class MyStrategy(bt.Strategy):
    params = (
        ('ema_period', 20),
    )

    def __init__(self):
        self.ema = bt.indicators.ExponentialMovingAverage(self.data.close, period=self.params.ema_period)

    def next(self):
        sell_threshold = 0.05

        # 检查是否产生买入信号
        if not self.position:  # 如果当前没有持仓
            if self.data.close > self.ema:  # 当当前收盘价大于EMA时
                self.buy()  # 执行买入

        # 检查是否产生卖出信号（当股价远高于20日EMA时）
        elif self.position and (self.data.close / self.ema - 1) > sell_threshold:  # 假设sell_threshold为设定的偏离比例阈值
            sell_threshold = 0.10  # 可以根据实际情况调整这个数值，例如这里设置为10%
            self.sell()  # 当收盘价比EMA高出10%时，执行卖出


data = bt.feeds.PandasData(dataname=df)

# 创建Cerebro引擎
cerebro = bt.Cerebro()

# 假设data是Backtrader可读取的数据格式，例如CSV文件中的数据
# data = bt.feeds.GenericCSVData(dataname='hk_stock_data.csv')

# 向Cerebro引擎中添加数据
cerebro.adddata(data)

# 添加策略到Cerebro
cerebro.addstrategy(MyStrategy)

# 设置起始资金
cerebro.broker.setcash(100000.0)

# 设置每次交易的买入数量
cerebro.addsizer(bt.sizers.PercentSizer, percents=100)

# 设置交易手续费，这里以0.1%为例
cerebro.broker.setcommission(commission=0.001)

# 运行回测
results = cerebro.run()

# 绘制结果
cerebro.plot()
