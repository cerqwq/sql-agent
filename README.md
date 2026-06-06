# 🗄️ SQL Agent

AI SQL助手，支持自然语言转SQL、查询优化、数据洞察。

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python" />
  <img src="https://img.shields.io/badge/OpenAI-API-green?logo=openai" />
  <img src="https://img.shields.io/badge/License-MIT-yellow" />
</p>

## ✨ 特性

- 🗣️ 自然语言转SQL
- ⚡ SQL查询优化
- 📖 SQL解释
- 📊 报表查询生成
- 🔍 索引建议
- 📈 数据洞察

## 🚀 快速开始

```bash
pip install openai

python agent.py
```

## 📖 使用

```python
from sql_agent import create_agent

agent = create_agent()

# 设置Schema
agent.set_schema("""
CREATE TABLE users (id INT, name VARCHAR(100));
CREATE TABLE orders (id INT, user_id INT, amount DECIMAL);
""")

# 自然语言转SQL
sql = agent.natural_language_to_sql("查询用户的订单总额")

# 优化SQL
result = agent.optimize_sql("SELECT * FROM users WHERE id = 1")

# 解释SQL
explanation = agent.explain_sql("SELECT COUNT(*) FROM orders GROUP BY user_id")

# 生成报表查询
query = agent.generate_report_query("月度销售报表")

# 索引建议
indexes = agent.suggest_indexes(["SELECT * FROM orders WHERE user_id = 1"])

# 数据洞察
insights = agent.data_insights(data, "分析用户行为趋势")
```

## 📁 项目结构

```
sql-agent/
├── agent.py       # SQL Agent核心
└── README.md
```

## 📄 许可证

MIT License
