import tushare as ts
import backtrader as bt
import pandas as pd
from datetime import datetime
import time
import os
import numpy as np

def fetch_hs300_data_with_cache():
    """获取沪深300指数数据,支持本地缓存"""
    csv_path = 'sh300_data.csv'
    
    # 如果本地缓存存在,直接读取
    if os.path.exists(csv_path):
        print(f"从本地缓存读取数据: {csv_path}")
        df = pd.read_csv(csv_path)
        df['日期'] = pd.to_datetime(df['日期'])
        return df
    
    # 生成示例数据文件
    print("\n数据缓存不存在,正在生成示例数据文件...")
    print("注意: 这是模拟数据,仅用于测试回测流程!")
    
    # 生成2014-2024年的模拟数据
    date_range = pd.date_range(start='2014-01-01', end='2024-01-01', freq='D')
    date_range = date_range[date_range.weekday < 5]  # 只保留工作日
    
    data = []
    base_price = 2200  # 沪深300基准价格
    for i, date in enumerate(date_range):
        # 模拟价格波动(随机漫步)
        change = (np.random.random() - 0.5) * 0.02  # 日波动约±1%
        base_price *= (1 + change)
        
        # 生成OHLC数据
        open_price = base_price * (1 + np.random.random() * 0.01)
        high_price = base_price * (1 + np.random.random() * 0.015)
        low_price = base_price * (1 - np.random.random() * 0.015)
        close_price = base_price
        
        # 确保价格逻辑正确
        high_price = max(open_price, close_price, high_price)
        low_price = min(open_price, close_price, low_price)
        
        # 生成成交量(随机)
        volume = np.random.randint(100000000, 500000000)
        
        data.append({
            '日期': date.strftime('%Y-%m-%d'),
            '开盘': round(open_price, 2),
            '最高': round(high_price, 2),
            '最低': round(low_price, 2),
            '收盘': round(close_price, 2),
            '成交量': volume
        })
    
    df = pd.DataFrame(data)
    
    # 保存到本地
    df.to_csv(csv_path, index=False, encoding='utf-8')
    print(f"示例数据已保存到: {csv_path}")
    print(f"共生成 {len(df)} 条数据")
    print(f"数据时间范围: {df['日期'].min()} 至 {df['日期'].max()}")
    print(f"\n如需使用真实数据:")
    print("1. 访问: https://quote.eastmoney.com/zs000001.html")
    print("2. 点击'历史数据'标签")
    print("3. 选择日期范围导出CSV")
    print("4. 保存为 sh300_data.csv 覆盖当前文件")
    
    return df

class DoubleSMA(bt.Strategy):
    params = (("fast", 20), ("slow", 60))
    def __init__(self):
        self.fast_ma = bt.ind.SMA(period=self.p.fast)
        self.slow_ma = bt.ind.SMA(period=self.p.slow)
        self.cross = bt.ind.CrossOver(self.fast_ma, self.slow_ma)
    def next(self):
        if self.cross > 0:
            self.buy()
        elif self.cross < 0:
            self.sell()

def run():
    # 用 tushare 拉取沪深 300 指数 10 年数据(带缓存)
    df = fetch_hs300_data_with_cache()
    
    # tushare返回的列已经是中文格式,直接使用
    df = df[["日期", "开盘", "最高", "最低", "收盘", "成交量"]]
    df.columns = ["datetime", "open", "high", "low", "close", "volume"]
    df["datetime"] = pd.to_datetime(df["datetime"])
    df.set_index("datetime", inplace=True)
    df = df.astype(float)
    data = bt.feeds.PandasData(dataname=df)

    cerebro = bt.Cerebro()
    cerebro.adddata(data)
    cerebro.addstrategy(DoubleSMA)
    cerebro.broker.setcash(1_000_000)
    cerebro.broker.setcommission(0.001)
    cerebro.addsizer(bt.sizers.PercentSizer, percents=95)
    print("初始资金: %.2f" % cerebro.broker.getvalue())
    cerebro.run()
    print("期末资金: %.2f" % cerebro.broker.getvalue())
    cerebro.plot(style="candle", barup="red", bardown="green")

if __name__ == "__main__":
    run()
