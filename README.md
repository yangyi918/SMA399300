# SMA399300
> Kimi指导的量化投资自学笔记：从0到1跑通双均线策略  

## 1 成果速览
- 标的：沪深300指数（399300）  
- 周期：2014-01-01 ～ 2024-01-01  
- 策略：20/60日均线金叉买入、死叉卖出  
- 收益：初始资金100万 → 期末**157.2万**（净值1.57，年化约9.4%）  
- 最大回撤：约15%（2015年股灾段）  
- 交易次数：10次（含买卖）

## 2 一键复现
```bash
git clone https://github.com/你的用户名/QuantAfter50.git
cd QuantAfterSystem
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python first_strategy.py
