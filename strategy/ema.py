import backtrader as bt


class EMA20Strategy(bt.Strategy):
    params = (
        ('period', 20),
        ('fast_exit_threshold', 0.1),  # 偏离EMA的百分比阈值
    )

    def __init__(self):
        self.dataclose = self.datas[0].close  # 获取收盘价
        self.ema = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.period)  # 计算20日EMA

    def next(self):
        # 判断是否处于上升趋势
        if self.dataclose[-1] > self.dataclose[-self.params.period]:
            # 股价回踩20EMA附近时买入
            if abs((self.dataclose[-1] - self.ema[-1]) / self.ema[-1]) <= self.params.fast_exit_threshold:
                size = min(int(self.broker.cash / self.data.close), self.getposition().size or 1)
                self.buy(size=size)

        # 上涨偏离20EMA均线过大时卖出
        if self.dataclose[-1] > self.ema[-1] and abs(
                (self.dataclose[-1] - self.ema[-1]) / self.ema[-1]) > self.params.fast_exit_threshold:
            self.sell()
