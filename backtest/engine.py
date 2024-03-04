import backtrader as bt

from data.fetcher import get_hk_stocks_data
from strategy.ema import EMA20Strategy

assert bt.__version__ >= '1.9.75.130', "Please upgrade to a version of backtrader supporting PandasData"
if __name__ == '__main__':
    # 获取所有市值超过100亿港元的港股数据及日线数据
    stocks_data = get_hk_stocks_data()

    # 实现回测逻辑之前，请确保stocks_data是一个包含了所有满足条件股票日线数据的字典
    print(stocks_data)
    for stock_name, df in stocks_data.items():
        # 初始化回测环境
        cerebro = bt.Cerebro()
        print(f"开始对{stock_name}的回测")
        print(df)

        # 加载数据
        data = bt.feeds.PandasData(dataname=df)
        cerebro.adddata(data)  # 添加数据至回测引擎

        # 设置策略
        cerebro.addstrategy(EMA20Strategy)

        # 设置初始资金
        initial_cash = 1000000
        cerebro.broker.setcash(initial_cash)

        # 配置其他参数（例如手续费、佣金等，如果需要）
        # cerebro.broker.setcommission(commission=...)

        # 运行回测
        results = cerebro.run()

        # 输出回测结果或其他统计信息（这里仅输出完成回测的消息）
        print(f"完成对{stock_name}的回测")

        # 如果需要分析回测结果，可以访问cerebro.strats[0][0].analyzers.*
        # 示例：获取最终净值
        final_value = cerebro.strats[0][0].analyzers.portfolio.get_analysis()['total']['networth']
        print(f"{stock_name}最终净值: {final_value}")
