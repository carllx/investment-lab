# Investment Lab 🧪

> A personal laboratory for investment research, strategy experimentation, backtesting, fund and stock selection, and trading workflows.

`investment-lab` 是一个面向多资产类别的个人投资研究与量化实验平台。本项目采用多实验（Multi-Experiment）组织架构，将数据获取、特征工程、策略回测与资产优选解耦为独立的投研实验模块。

---

## 📁 仓库结构

```text
investment-lab/
├── experiments/                    # 投资与策略实验集合
│   └── funds/
│       └── fund-screening/         # 公募基金多维筛选与组合实验
│           ├── README.md           # 实验详细说明
│           ├── main.py             # 实验运行入口 (同步)
│           ├── main_aio.py         # 实验运行入口 (异步)
│           ├── analytics.py        # 基金经理与指标分析
│           ├── query_data.py       # 数据获取接口 (同步)
│           ├── query_data_aio.py   # 数据获取接口 (异步)
│           ├── config.py           # 实验配置
│           ├── notebooks/          # 交互式研究与可视化
│           │   └── portfolio_selection.ipynb
│           └── fixtures/           # 示例响应数据与测试基准
│               └── ref-overview.json
├── docs/                           # 工程文档与规范
│   └── agents/                     # Agent 协作与工程化指引
├── .gitignore                      # 源码与生成数据/缓存边界隔离
└── AGENTS.md                       # 智能体协作指南
```

---

## 🔬 现有实验列表

| 实验分类 | 实验名称 | 描述 | 状态 |
| :--- | :--- | :--- | :--- |
| **Funds (基金)** | [fund-screening](experiments/funds/fund-screening/) | 基于业绩门槛、基金经理牛熊任期、回撤控制与排名稳定性的公募基金多维筛选实验 | 活跃 / 基线 |

---

## 🛠️ 设计原则与数据边界

1. **多实验隔离**：每个实验均具备自包含的运行逻辑、配置与分析说明，互不干扰。
2. **源码与数据隔离**：大规模抓取缓存、高频生成文件与运行时报表（如 `report/`、`data/`、`*.parquet`、`*.duckdb`）均由 `.gitignore` 严格忽略，保持 Git 仓库精简干净。
3. **渐进式演进**：避免未经真实需求验证的过度框架抽象，保持轻量、务实与可复现性。

---

## 📄 License
MIT License
