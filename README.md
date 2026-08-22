# Investment Lab 🧪

> A personal laboratory for investment research, strategy experimentation, backtesting, fund and stock selection, and trading workflows.

`investment-lab` 是一个以实验为先（Experiment-first）的个人投资研究工作空间，用于组织针对基金、股票、策略回测与投资组合选择的独立研究实验。

---

## 📁 仓库结构

```text
investment-lab/
├── experiments/                    # 投资与策略实验集合
│   └── funds/
│       └── fund-screening/         # 公募基金多维筛选与配置研究实验
│           ├── README.md           # 实验详细说明与运行指引
│           ├── main.py             # 实验运行入口 (同步)
│           ├── main_aio.py         # 实验运行入口 (异步高并发原型)
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
| **Funds (基金)** | [fund-screening](experiments/funds/fund-screening/) | 基于业绩门槛、基金经理牛熊任期、回撤控制与排名稳定性的公募基金多维筛选与配置实验（源自初始 baseline） | 进行中 / 活跃实验线 |

---

## 🛠️ 设计原则与边界

1. **实验自治（Experiment-first）**：每个实验均具备自包含的运行逻辑、配置与分析说明，不预设过度复杂的全局量化框架。
2. **源码与数据隔离**：大规模抓取缓存、高频生成文件与运行时报表（如 `report/`、`report2/`、`data/` 等）均由 `.gitignore` 严格忽略，保持 Git 仓库精简干净。
3. **知识边界与晋升**：本仓库拥有实验代码、参数与运行时成果的完整权威；跨实验沉淀的持久性结论未来按需向外部知识库（如 Obsidian Wiki）单向晋升，不做机械式双向同步。
4. **渐进式演进**：避免未经真实实验需求验证的抽象，保持轻量、务实与可复现性。
