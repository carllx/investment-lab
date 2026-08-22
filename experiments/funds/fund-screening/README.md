# 公募基金筛选与评价实验 (Fund Screening Experiment)

## 1. 实验概述
本实验属于 `investment-lab` 下的基金研究子模块，旨在通过多维量化指标与基金经理特征，对全市场公募基金进行层层初筛与打分，并为后续投资组合构建（Portfolio Selection）提供候选资产池。

## 2. 数据来源
数据主要来源于东方财富网 / 天天基金网公开及未公开数据端点：
- **全市场基金列表**：代码、名称、近 1周/1月/3月/6月/1年/2年/3年 收益率、手续费等。
- **基金概况 (`JJXQ`)**：基金规模 (`ENDNAV`)、夏普比率 (`SHARP1/2/3`)、基金类型等。
- **基金经理信息 (`JJJL`)**：历任经理天数、当前经理任期天数 (`DAYS`)、从业总天数 (`TOTALDAYS`)。
- **特色风险数据 (`TSSJ`)**：近 1/3/5 年最大回撤 (`MAXRETRA1/3/5`)。
- **同类排名走势 (`tlpm`)**：近 1年 (`1n`)、近 6月 (`6y`)、近 3月 (`3y`) 的同类相对排位百分比。
- **净值走势序列 (`FundNetDiagram2`)**：历史累计净值数据。

## 3. 核心筛选逻辑
实验采用漏斗式过滤流水线：
1. **中长期业绩硬性门槛**：近 1年收益 ≥ 15%、近 2年收益 ≥ 30%、近 3年收益 ≥ 45%（可配置）。
2. **基金规模过滤**：剔除规模小于 2 亿元的迷你基金，规避清盘与流动性风险。
3. **基金经理维度评估**：
   - **牛熊周期经验**：从业天数必须经历过完整牛熊周期（基准为 2014-2015 轮行情）。
   - **在任年限**：当前基金任期需满足一定年限（建议 ≥ 3 年）。
   - **回撤控制 (MDD)**：1/3/5 年最大回撤严格控制在 35% 以内。
4. **同类排名稳定性打分**：
   - 计算管理期内各周期（1年/6月/3月）每日相对同类排名的均值（`rank / total_count`）。
   - 要求各周期排名前 1/3（均值 < 0.333），并将综合排名加总排序。
5. **组合收益与波动率可视化**：
   - 在 Jupyter Notebook 中对齐筛选基金的净值时间序列，评估相关性与绘制收益走势。

## 4. 文件结构
```text
experiments/funds/fund-screening/
├── README.md               # 实验说明文档
├── config.py               # 路径与排期参数配置
├── query_data.py           # 同步 HTTP 数据抓取模块 (requests)
├── query_data_aio.py       # 异步 HTTP 数据抓取模块 (aiohttp)
├── analytics.py            # 基金经理指标过滤与胜率分析函数
├── main.py                 # 同步执行流水线入口
├── main_aio.py             # 异步执行流水线入口
├── notebooks/
│   └── portfolio_selection.ipynb  # 投资组合净值对齐与可视化 Notebook
└── fixtures/
    └── ref-overview.json   # 样例基金详情接口响应结构 (用于参考 Schema)
```

## 5. 运行方式

### 运行环境准备
```bash
# 激活 Python 环境并安装依赖
pip install pandas requests aiohttp matplotlib seaborn scipy
```

### 执行筛选流程
```bash
cd experiments/funds/fund-screening

# 执行同步筛选流程（主入口）
python main.py

# 执行异步高并发拉取原型（需 aiohttp；适用于全量测试，需注意外部 API 频控）
python main_aio.py
```

### 查看或运行 Notebook
```bash
jupyter notebook notebooks/portfolio_selection.ipynb
```

## 6. 输出与生成数据
运行后会在当前实验目录下生成 `report/` 文件夹（已配置 Git 忽略，不纳入版本控制；运行时会自动确保目录创建）：
- `report/list_of_all_funds.csv`：全市场基金列表。
- `report/overview/`：各基金详情 JSON 缓存。
- `report/overview_filtered_manager.csv`：通过规模与经理筛选后的基金列表。
- `report/rank/`：多周期同类排名数据缓存。
- `report/rank.csv`：最终通过排名稳定性筛选并打分的精选基金列表。

## 7. 维护状态与定位
- **定位**：进行中 / 活跃基金研究实验线（当前实现源自历史基线）。用于持续开展公募基金选品、经理画像刻画与配置策略实验。
- **后续规划**：后续阶段中，底层数据抓取将逐步平滑接入规范的数据源适配（如 AkShare）及结构化缓存存储（DuckDB/Parquet）。
