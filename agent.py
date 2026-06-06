"""
SQL Agent - AI SQL助手
支持自然语言转SQL、查询优化、数据洞察
"""

import json
import os
from typing import Dict, List, Any
from datetime import datetime

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class SQLAgent:
    """
    AI SQL助手
    支持：自然语言转SQL、查询优化、数据分析
    """

    def __init__(self, model: str = "mimo-v2.5-pro", api_key: str = None, base_url: str = None):
        self.model = model
        self.schema_cache: Dict[str, str] = {}

        if OPENAI_AVAILABLE:
            self.client = OpenAI(
                api_key=api_key or os.environ.get('OPENAI_API_KEY', ''),
                base_url=base_url or os.environ.get('OPENAI_BASE_URL', 'https://api.xiaomimimo.com/v1')
            )
        else:
            self.client = None

    def set_schema(self, schema: str):
        """设置数据库Schema"""
        self.schema_cache["default"] = schema

    def natural_language_to_sql(self, question: str, schema: str = None) -> str:
        """自然语言转SQL"""
        if not self.client:
            return "LLM客户端未配置"

        schema = schema or self.schema_cache.get("default", "")

        prompt = f"""请将以下自然语言问题转换为SQL查询：

数据库Schema：
{schema}

问题：{question}

要求：
1. 只返回SQL语句
2. 使用标准SQL语法
3. 考虑性能优化
4. 添加必要注释"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )

        return response.choices[0].message.content

    def optimize_sql(self, sql: str, schema: str = None) -> Dict:
        """优化SQL查询"""
        if not self.client:
            return {"error": "LLM客户端未配置"}

        schema = schema or self.schema_cache.get("default", "")

        prompt = f"""请优化以下SQL查询：

Schema：
{schema}

SQL：
{sql}

请返回JSON格式：
{{
    "optimized_sql": "优化后的SQL",
    "issues": ["问题1", "问题2"],
    "suggestions": ["建议1", "建议2"],
    "estimated_improvement": "预期提升"
}}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )

        try:
            content = response.choices[0].message.content
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except Exception as e:
            return {"error": str(e)}

        return {"optimization": content}

    def explain_sql(self, sql: str) -> str:
        """解释SQL查询"""
        if not self.client:
            return "LLM客户端未配置"

        prompt = f"""请详细解释以下SQL查询：

{sql}

要求：
1. 整体功能说明
2. 每个子句的作用
3. 关键逻辑解析
4. 性能考虑"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )

        return response.choices[0].message.content

    def generate_report_query(self, report_type: str, schema: str = None) -> str:
        """生成报表查询"""
        if not self.client:
            return "LLM客户端未配置"

        schema = schema or self.schema_cache.get("default", "")

        prompt = f"""请根据以下需求生成SQL报表查询：

Schema：
{schema}

报表类型：{report_type}

要求：
1. 返回完整的SQL查询
2. 包含聚合函数
3. 考虑数据可视化需求
4. 添加必要注释"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )

        return response.choices[0].message.content

    def suggest_indexes(self, queries: List[str], schema: str = None) -> List[Dict]:
        """建议索引"""
        if not self.client:
            return [{"error": "LLM客户端未配置"}]

        schema = schema or self.schema_cache.get("default", "")
        queries_text = "\n".join(f"Q{i+1}: {q}" for i, q in enumerate(queries))

        prompt = f"""请根据以下查询建议数据库索引：

Schema：
{schema}

查询：
{queries_text}

请返回JSON格式：
[
    {{"table": "表名", "columns": ["列1", "列2"], "type": "btree/hash/gin", "reason": "原因"}}
]"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )

        try:
            content = response.choices[0].message.content
            import re
            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except Exception as e:
            return [{"error": str(e)}]

        return [{"suggestion": content}]

    def data_insights(self, data: Any, question: str = "") -> str:
        """数据洞察"""
        if not self.client:
            return "LLM客户端未配置"

        prompt = f"""请分析以下数据并提供洞察：

数据：{json.dumps(data[:20] if isinstance(data, list) else data, ensure_ascii=False)}

问题：{question or '请分析数据特征和趋势'}

要求：
1. 数据概览
2. 关键发现
3. 趋势分析
4. 建议"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1500
        )

        return response.choices[0].message.content


def create_agent(**kwargs) -> SQLAgent:
    """创建SQL Agent"""
    return SQLAgent(**kwargs)


if __name__ == "__main__":
    agent = create_agent()

    # 设置Schema
    agent.set_schema("""
    CREATE TABLE users (
        id INT PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100),
        created_at TIMESTAMP
    );
    CREATE TABLE orders (
        id INT PRIMARY KEY,
        user_id INT,
        amount DECIMAL(10,2),
        status VARCHAR(20),
        created_at TIMESTAMP
    );
    """)

    print("SQL Agent")
    print()

    # 测试
    sql = agent.natural_language_to_sql("查询最近7天的订单总额")
    print(f"Generated SQL: {sql}")
    print()

    explanation = agent.explain_sql("SELECT SUM(amount) FROM orders WHERE created_at > DATE_SUB(NOW(), INTERVAL 7 DAY)")
    print(f"Explanation: {explanation[:200]}...")
