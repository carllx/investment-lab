# Qlib Research Guidance

> **Status**: APPROVED (Distilled from Source Harvest)  
> **Target Issue**: [#4 Evaluate Qlib for stock & factor experiments](https://github.com/carllx/investment-lab/issues/4)  
> **Harvest Anchor Commit**: `147f506349c97f0f88143ad0cdd80673f77b3e6a`  
> **Evidence Package**: [qlib-source-harvest.md](../qlib-source-harvest.md)  
> **Audience**: Browser Agent / Research Lead (用于设计股票、因子、机器学习与回测实验时的方法论参考)

---

## 1. 核心定位与决策预设 (Core Judgment)

### 预设判断: `PARTIAL` (局部采用 / 独立实验容器)
- **定位**: Qlib 作为 `investment-lab` 进行**股票截面选股、多因子量价建模、机器学习时序实验与标准化信号检验 (IC/Rank IC)** 的专业工具箱。
- **边界约束**:
  - 仅在专属股票/因子实验子项目中完整使用；
  - **不让整个 `investment-lab` 强依赖 Qlib 的数据格式或工作流体系**；
  - 保持主仓库数据层与研究框架的独立性。

---

## 2. 适用与非适用场景 (When to Use vs. When NOT to Use)

### 适用场景 (Recommended)
1. **股票量价多因子特征工程**: 需要基于公式化表达式（Expression Engine）快速生成高维特征（如 Alpha158 及其衍生变量）并复用时序缓存。
2. **监督学习/时序预测模型训练**: 构建 GBDT（LightGBM/XGBoost）或时序神经网络进行截面收益预测。
3. **标准化信号质量检验**: 快速评估预测打分的横截面相关性（Pearson IC、Spearman Rank IC、ICIR、多空分档收益分析）。
4. **标准截面轮动策略基准回测**: 使用经典的 Top-k 选股或 TopkDropout 换仓逻辑进行基准测试。

### 不适用场景 (Avoid / Use Alternative)
1. **全实验室核心数据基础设施**: 避免将全部公募基金、ETF、宏观指标强行转入 Qlib `.bin` 格式。
2. **高保真 A 股微观规则回测**:
   - 依赖严格账户层 T+1 当日买入冻结/可用持仓隔离；
   - 需要精确模拟全面注册制 20% 涨跌停与 ST 5% 动态分层涨跌停；
   - 需要根据历史时间点动态调整印花税率（如 2023 年 8 月减半）；
   - 需要精准处理分红派息现金动态入账。
3. **宏观资产配置与场外基金筛选**: Qlib 架构天然面向高频/日线截面股票池，非股票截面选股场景应保持轻量独立架构。

---

## 3. 核心方法论与设计原则 (Key Architectural Principles)

### A. 数据与模型的严格解耦
- **`DataHandler`**: 负责底层数据加载（`DataLoader`）、时序特征提取与预处理（`Processor`）。
- **`Dataset`**: 负责时序时间段切分（`train`, `valid`, `test`），输出标准矩阵。
- **原则**: 预测模型仅消费 `Dataset`，不感知底层数据存储格式与因子计算细节。

### B. 时序计算与截面处理的分离
- **因子公式**: 严格在单标的的**时序滚动维度**计算（如移动均线 `Mean`、滚动波动率 `Std`、滚动斜率 `Slope`）。
- **`Rank(X, N)` 注意事项**: 属于 **Rolling Rank (Percentile)**（即单只股票在过去 $N$ 天的滚动百分位排名），**不是截面排名**。
- **截面处理**: 截面标准化（Cross-sectional Z-score）、中位数去极值等操作必须且仅能在 `Processor` 或信号评估环节执行。

### C. 防前视偏差 (Lookahead Bias 防护准则)
1. **标签对齐 (Label Alignment)**:
   - 预测目标收益率必须显式位移，例如默认标签 `Ref($close, -2) / Ref($close, -1) - 1`，代表 $T$ 日盘后出信号、$T+1$ 日收盘买入、$T+2$ 日收盘卖出的净收益，严防使用 $T$ 日盘中未知数据。
2. **预处理区间对齐 (Fit-Transform Alignment)**:
   - 必须通过 `fit_start_time` / `fit_end_time` 将预处理器的拟合统计量限制在 `train` 训练集内，禁止全样本预处理。
3. **时点数据库 (Point-in-Time, PIT)**:
   - 基本面与财报数据需利用发布日期（`date`）与报告期（`period`）双索引，防范财报修正与滞后发布带来的未来数据泄漏。

### D. 两阶段评估哲学 (Two-Stage Evaluation)
- **阶段一: 信号纯粹质量评估 (`SigAnaRecord`)**:
  - 先看截面相关性指标（IC、Rank IC、ICIR、Rank ICIR）。
  - **小白认知**: IC 衡量的是“模型打分高低与未来涨幅相对排名的稳定一致性”，用于排查模型预测本身的信噪比。
- **阶段二: 组合与执行回测 (`PortAnaRecord`)**:
  - 信号统计有效后再进入实际回测，评估持仓权重、换手率摩擦、佣金冲击成本与滑点。
- **线索价值**:
  - IC 良好但回测不赚钱 $\rightarrow$ 排查交易成本、换手率或调仓频率瓶颈；
  - 回测赚钱但 IC 接近 0 $\rightarrow$ 排查是否偶然押中个别极端大牛股或出现数据泄漏。

---

## 4. A 股回测边界核查清单 (A-Share Reality Check)

| 机制项 | Qlib 原生支持现状 | Browser Agent 实验应对建议 |
| :--- | :--- | :--- |
| **整手交易** | 支持 100 股向下取整 (`trade_unit=100`) | 直接使用官方配置 |
| **静态涨跌停与停牌** | 支持静态 `limit_threshold` 涨停禁买/跌停禁卖及 NaN 停牌识别 | 默认开启，适用于主板 10% 标的 |
| **T+1 规则** | 仅在 `TopkDropoutStrategy` 提供策略层 `hold_thresh=1` 过滤 | 明确标注限制；若自研策略需在 Spike 中单独验证持仓可用状态 |
| **动态涨跌停与动态印花税** | 仅支持单一静态费率与单一静态涨跌停阈值 | 在需要严谨复现历史阶段收益时，需通过自定义 Exchange 或外挂微调处理 |
| **分红派息** | 基于 `$factor` 调整复权价，无动态现金入账 | 了解其以资本收益折算为准的特性，不作为精确现金流记账凭证 |

---

## 5. 后续 Spike 实施指引 (Spike Action Guide)

1. **版本锁定**: 后续实验环境统一固定于最新 Stable Tag **`v0.9.7`**，避免跟踪 `main` 分支未发布特性的破坏性变更。
2. **基准选择**: 以官方 `Alpha158 + LightGBM + CSI300` (`examples/benchmarks/LightGBM/workflow_config_lightgbm_Alpha158.yaml`) 作为股票实验的标准参考实现。
3. **隔离开发**: 在 `experiments/` 下建立专门的实验目录（如 `experiments/stocks/qlib-experiments/`），确保不污染公共模块。
