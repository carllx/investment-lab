# Qlib Source Harvest

## Capture metadata

- **Repository**: `https://github.com/microsoft/qlib`
- **Main ref used**: `79633dd9506ea689e5400dea0197717b5b3d74b7`
- **Latest stable release tag**: `v0.9.7` (`da920b7f954f48ab1bb64117c976710de198373e`, 2025-08-15)
- **Captured date**: 2026-08-23
- **Target issue**: [#4 Evaluate Qlib for stock & factor experiments](https://github.com/carllx/investment-lab/issues/4)
- **Status**: Read-only source harvest for Browser Guidance preparation (Phase 1A - Review Fix)

---

## Research-flow architecture

### 1. 官方量化研究闭环流程

[Source Fact]  
依据官方文档 `docs/introduction/introduction.rst` 与架构图 `docs/_static/img/framework.svg`，Qlib 将量化研究与交易划分为四层结构：
1. **Infrastructure Layer**: `DataServer` 提供底层高性能数据存储与检索；`Trainer` 控制模型训练进程。
2. **Learning Framework Layer**: 涵盖监督学习（Supervised Learning）与强化学习（RL），用于训练 `Forecast Model` 与 `Trading Agent`。
3. **Workflow Layer**: 覆盖端到端量化投资流程，具体管道为：
   $$\text{Data} \xrightarrow{\text{Data Loader}} \text{DataHandler (Feature/Label)} \xrightarrow{\text{Processor}} \text{Dataset (Segment Split)} \xrightarrow{\text{Model Train}} \text{Forecast Model}$$
   $$\xrightarrow{\text{Inference}} \text{Prediction / Signal} \xrightarrow{\text{Signal Analysis}} \text{Strategy (Decision Generator)} \xrightarrow{\text{Order}} \text{Execution Env (Exchange/Account)} \xrightarrow{\text{Portfolio Analysis}}$$
4. **Interface Layer**: `Analyser` / `Recorder` 统一输出信号分析报告、持仓组合分析与执行归因报告。

[Interpretation]  
- **通用方法论借鉴**: 将“数据预处理”、“特征工程”、“时序数据集切分”、“模型训练预测”、“信号截面分析”、“策略组合生成”、“撮合回测与账户归因”严格解耦，各环节以标准化的数据结构（DataFrame / Series / 契约对象）传递，是成熟量化系统的通用标准。
- **Qlib 特有实现**: 强绑定于基于 YAML 的工作流配置驱动机制（`qrun workflow_config.yaml`）、内置的基于文件系统的表达式缓存体系，以及将信号预测（`SignalRecord`）与投资组合回测（`PortAnaRecord`）作为两个独立但级联的 Recorder 步骤。

[Open Question for investment-lab]  
- `investment-lab` 是否需要全盘引入 YAML 工作流驱动，还是仅借鉴其各模块的 Python API 契约与流程解耦思想？

---

## Data layer

### 1. Market Data 组织与底层存储

[Source Fact]  
- 官方提供专门针对金融时序计算的 `.bin` 二进制存储格式（参考 `docs/component/data.rst` 及 Qlib 论文）。
- 日线数据默认存储各标的复权行情数据（`$open`, `$high`, `$low`, `$close`, `$volume`, `$factor`），其中 `$factor` 用于在需要时换算回原始成交价格（如 `$close / $factor`）以及进行整手股数换算。
- 提供 `scripts/dump_bin.py`，支持将任何标准 CSV 或 Parquet 格式的外部日线/高频数据转换为 Qlib `.bin` 格式。
- 自 `v0.9.7` 起进一步增强了原生 Parquet 数据支持（PR #1966）。

### 2. DataHandler 与 Dataset 的职责划分

[Source Fact]  
依据 `qlib/data/dataset/handler.py` 与 `qlib/data/dataset/__init__.py`：
- **`DataLoader` (如 `QlibDataLoader`)**: 负责从底层存储中读取原始行情字段或通过表达式引擎计算基础特征与标签。
- **`DataHandler` (如 `DataHandlerLP`)**: 负责协调 `DataLoader`，并管理两组可插拔的预处理器 `infer_processors` 与 `learn_processors`。Qlib 提供了 `fit_start_time` / `fit_end_time` 接口参数，供支持参数拟合的 Processors 获取拟合区间。
- **`Dataset` (如 `DatasetH`, `TSDatasetH`)**: 负责消费 `DataHandler` 处理后的数据，根据 `segments`（如 `train`, `valid`, `test`）切分时间窗口，并组装为模型所需的输入格式（例如 `DatasetH` 产出 2D 表格，`TSDatasetH` 产出 3D 滑动时序窗口 `(N, Time_step, Features)`）。

### 3. 数据层与模型的解耦

[Source Fact]  
- 模型（`Model`）仅与 `Dataset` 交互，调用 `dataset.prepare(segment, col_set=...)` 获取特征与标签矩阵。
- 模型内部完全不感知底层数据来自 `.bin`、Parquet、CSV 还是内存数据库，也不感知具体的因子计算公式。

[Interpretation]  
- 该设计保证了当未来替换底层数据源或扩展新因子时，无需改动任何模型推理与训练逻辑。

[Open Question for investment-lab]  
- `investment-lab` 本地现有数据体系（如 `experiments/funds/fund-screening` 中的 Json/CSV 行情）如何以最小成本对接？是编写专属 `DataLoader` 直接读取，还是通过转换脚本接入 Qlib 数据目录？

---

## Factors / Alpha158

### 1. Expression Engine 基本思想

[Source Fact]  
依据 `docs/component/data.rst` 与 `qlib/data/ops.py`：
- 采用声明式表达式字符串（Formulaic Expressions）定义因子，例如 `"Ref($close, 60) / $close"` 或 `"Mean($close, 20) / $close"`。
- 支持算子组合：
  - 时序平移：`Ref(X, d)`
  - 滚动统计：`Mean(X, d)`, `Std(X, d)`, `Max(X, d)`, `Min(X, d)`, `Quantile(X, d, q)`
  - 趋势与回归：`Slope(X, d)` (斜率), `Rsquare(X, d)` (拟合优度), `Resi(X, d)` (残差)
  - 滚动百分位排名：`Rank(X, N)`（**注意**：源码 `class Rank(Rolling)` 实现为单标的时序滚动百分位 `series.rolling(N).rank(pct=True)`，属于 Rolling Rank，而非截面排名）。
- 表达式在底层进行语法解析并由高性能引擎执行，计算结果具备 Disk/Memory 缓存机制。

### 2. Alpha158 的作用与特征分类

依据 `qlib/contrib/data/handler.py` 与 `qlib/contrib/data/loader.py`：

#### A. Alpha158 默认 158 个特征组成 (Default Feature Composition)
[Source Fact]  
在 `qlib/contrib/data/handler.py` 中，`Alpha158.get_feature_config()` 显式传入固定配置：
```python
conf = {
    "kbar": {},
    "price": {
        "windows": [0],
        "feature": ["OPEN", "HIGH", "LOW", "VWAP"],
    },
    "rolling": {},
}
```
其实际生成的 158 个特征构成为：
1. **Kbar 特征 (9 个)**: 刻画单日 K 线的实体幅度、上下影线比例（`KMID`, `KLEN`, `KMID2`, `KUP`, `KUP2`, `KLOW`, `KLOW2`, `KSFT`, `KSFT2`）。
2. **Price 特征 (4 个)**: 当日价格与收盘价比例（`OPEN0`, `HIGH0`, `LOW0`, `VWAP0`，即 `$open/$close`, `$high/$close`, `$low/$close`, `$vwap/$close`）。
3. **Rolling 时序统计特征 (29 类算子 × 5 个窗口 `[5, 10, 20, 30, 60]` = 145 个)**:
   - 动量与均线：`ROC` (变动率), `MA` (移动均线比例)
   - 波动与回归：`STD` (滚动波动率), `BETA` (线性回归斜率), `RSQR` (拟合优度), `RESI` (回归残差)
   - 极值与分位：`MAX` / `LOW` (区间最高/最低价), `QTLU` / `QTLD` (80%/20% 分位数), `RANK` (过去 N 天滚动百分位排名), `RSV` (未成熟随机值)
   - 周期与极值时点 (Aroon 指标类)：`IMAX` (最高价距今距离), `IMIN` (最低价距今距离), `IMXD` (最高与最低时点差)
   - 量价相关性：`CORR` (价格与对数成交量相关性), `CORD` (收益率与成交量变化率相关性)
   - 涨跌统计：`CNTP` (上涨天数比例), `CNTN` (下跌天数比例), `CNTD` (涨跌天数差)
   - 资金强度 (类似 RSI 结构)：`SUMP` (上涨金额比), `SUMN` (下跌金额比), `SUMD` (涨跌金额差比)
   - 成交量与量价波动：`VMA` (成交量均线), `VSTD` (成交量波动率), `WVMA` (成交量加权价格波动率), `VSUMP` (成交量增加比), `VSUMN` (成交量减少比), `VSUMD` (成交量增减差比)
- **合计**: $9 + 4 + 145 = 158$ 个特征。

#### B. Alpha158DL 支持的可配置扩展选项 (Configurable Options / Docstring)
[Source Fact]  
`qlib/contrib/data/loader.py` 中的 `Alpha158DL.get_feature_config(config)` 提供了更通用的可配置接口，支持在调用时传入自定义参数扩展特征，例如：
- 扩展 `price` 的历史滞后窗口（如 `windows: [0, 1, 2, 3, 4]`）；
- 开启 `volume` 的历史滞后窗口（如 `windows: [0, 1, 2, 3, 4]`，计算 `VOLUME0`~`VOLUME4`）；
- 通过 `include` / `exclude` 列表按需增删 rolling 算子。
这些属于 `Alpha158DL` 的**可配置选项**，非 `Alpha158` 的**默认特征构成**。

### 3. 自定义 Factor / Feature 的入口

[Source Fact]  
1. **YAML / 配置直接注入**: 在 `DataHandler` 的 `config.feature` 列表中直接写入表达式字符串。
2. **继承 DataLoader / DataHandler**: 类似 `Alpha158`，继承 `QlibDataLoader` 并重写 `get_feature_config` 返回特征字典。
3. **扩展底层算子**: 在 `qlib/data/ops.py` 中继承 `ElemOperator` 或 `PairOperator` 注册新的时序/数学算子。

---

## Dataset & temporal split

### 1. train / validation / test 时序切分机制

[Source Fact]  
依据 `examples/benchmarks/LightGBM/workflow_config_lightgbm_Alpha158.yaml`：
- **Train 阶段** (如 `2008-01-01` ~ `2014-12-31`): 用于模型参数优化及预处理器统计量拟合 (`fit_start_time` ~ `fit_end_time`)。
- **Validation 阶段** (如 `2015-01-01` ~ `2016-12-31`): 用于超参数调优、早停（Early Stopping）判断。
- **Test 阶段** (如 `2017-01-01` ~ `2020-08-01`): 严格样本外（Out-of-Sample）盲测，用于输出模型最终预测信号并执行回测。

### 2. 避免未来信息泄漏（Lookahead Bias）的设计与边界

[Source Fact]  
1. **标签对齐设计**:
   - `Alpha158` 官方默认标签定义为：
     `Ref($close, -2) / Ref($close, -1) - 1`
   - `Ref(..., -1)` 为下一交易日（$T+1$），`Ref(..., -2)` 为再下一交易日（$T+2$）。这代表使用 $T$ 日收盘后生成的信号，在 $T+1$ 日以收盘价买入，并在 $T+2$ 日以收盘价卖出所获得的实际收益率。这天然避免了使用 $T$ 日盘中未知数据的未来偏差。
2. **预处理区间传递机制**:
   - Qlib 提供了 `fit_start_time` 与 `fit_end_time` 参数机制，Alpha handlers 会把这些参数传递给支持参数拟合的 Processors（如计算均值、方差、分位数截断等）。
   - 官方 LightGBM + Alpha158 baseline 在配置中显式将该 fit 区间与 train 区间对齐。
3. **Point-in-Time (PIT) 数据库支持**:
   - 依据 `docs/advanced/PIT.rst`，对于财务报表等多期修正、延迟披露的数据，Qlib 设计了记录披露日期（`date`）与报告期（`period`）的 PIT 索引，确保在历史任意回测截面获取的都是当时物理时间点已发布的最新数据版本。

[Interpretation]  
- Qlib 提供了支持防前视偏差的接口工具（如标签位移、`fit_start_time`/`fit_end_time` 与 PIT 数据库），正确使用这些配置可以有效避免常见的数据泄漏。但框架本身无法自动保证任意用户自定义配置或自定义 Processor 都不发生泄漏，防泄漏责任仍取决于研究者的实验配置严谨性。

---

## Signal analysis

### 1. SignalRecord 与 SigAnaRecord 架构

[Source Fact]  
依据 `qlib/workflow/record_temp.py` 与 `qlib/contrib/eva/alpha.py`：
- **`SignalRecord`**: 驱动模型在测试集上完成推断，将多标的的预测打分序列保存为 `pred.pkl`，真实标签保存为 `label.pkl`。
- **`SigAnaRecord`**: 读取 `pred.pkl` 和 `label.pkl`，执行截面信号质量分析，输出核心统计指标并记录到 Recorder。

### 2. 核心信号指标与计算方法

[Source Fact]  
在 `qlib/contrib/eva/alpha.py` 中 `calc_ic` 实现如下：
- **IC (Information Coefficient)**:
  每日截面上，模型预测得分 $\hat{y}_t$ 与真实收益率 $y_t$ 的 Pearson 线性相关系数：
  $$\text{IC}_t = \text{corr}(\hat{y}_t, y_t)$$
- **Rank IC**:
  每日截面上，模型预测得分的排序与真实收益率排序的 Spearman 秩相关系数：
  $$\text{Rank IC}_t = \text{corr}(\text{rank}(\hat{y}_t), \text{rank}(y_t))$$
- **ICIR / Rank ICIR**:
  IC 时序序列的信噪比（均值除以标准差）：
  $$\text{ICIR} = \frac{\mathbb{E}[\text{IC}_t]}{\sigma(\text{IC}_t)}, \quad \text{Rank ICIR} = \frac{\mathbb{E}[\text{Rank IC}_t]}{\sigma(\text{Rank IC}_t)}$$
- **多空组合分析 (`ana_long_short=True`)**:
  将每日截面按预测得分由高到低分档，计算做多顶部分组（Long-Top）与做空底部分组（Short-Bottom）的多空年化收益率与多空夏普比率。

### 3. 直观解释：Signal Analysis 与最终回测收益的关系

[Interpretation]  
- **IC / Rank IC 的核心作用**: 主要帮助观察预测分数与未来实际相对收益/排序之间是否存在稳定的统计关联，衡量的是模型纯粹的选股与排序能力。
- **最终回测收益的复合性**: 最终回测收益不仅取决于预测信号质量，还复合了投资组合构建（如 Top-k 选股数量、权重分配）、市场宏观环境、换手率损耗、交易成本以及各类成交约束。
- **分离分析的价值**: 两层分析适合分开看。当 IC 表现与最终回测收益出现不一致时（例如 IC 良好但回测收益不佳，或回测收益较高但 IC 接近 0），它为进一步排查是“模型预测能力问题”还是“交易执行/组合构建损耗”提供了关键线索。

---

## Backtest

### 1. 预测信号进入策略与 TopkDropout 机制

[Source Fact]  
依据 `qlib/contrib/strategy/signal_strategy.py`：
- **信号输入**: `TopkDropoutStrategy` 继承 `BaseSignalStrategy`，在每个交易步（`trade_step`）通过 `signal.get_signal(shift=1)` 读取前一交易日生成的预测得分 `pred_score`。
- **调仓逻辑**:
  1. 设定持仓数量 `topk`（如 50 只）与每日最大替换数量 `n_drop`（如 5 只）。
  2. 对现有持仓按最新预测得分排序，得分最低的标的若跌出前列，将优先被选入卖出候选列表（最多卖出 `n_drop` 只）。
  3. 从未持仓且当前得分最高的标的中选出最多 `n_drop + (topk - 当前持仓数)` 只标的买入。
- **持仓天数约束 (`hold_thresh`)**:
  - `TopkDropoutStrategy` 提供了 `hold_thresh` 参数（默认值为 1），在卖出股票前检查当前持仓天数是否满足最小阈值（`current.get_stock_count(order.stock_id) >= self.hold_thresh`）。

[Interpretation]  
- `hold_thresh` 可以用于在策略层面表达最短持仓天数约束。

[Open Question for investment-lab]  
- `hold_thresh=1` 仅属于策略层的持仓天数过滤，并不等同于 Qlib 在所有 strategy / account / execution 路径下都严格实施了中国 A 股的 T+1 交易规则（即“当日买入股数当日冻结不可卖，仅前一交易日及之前持仓可用”）。该规则在非 TopkDropout 策略或复杂执行环境下的行为必须由 investment-lab 通过 Spike 实测验证。

### 2. 交易假设与执行环境支持度 (`Exchange` 模块)

[Source Fact]  
依据 `qlib/backtest/exchange.py`：
- **成交价设定 (`deal_price`)**: 支持 `close`、`open`、`vwap` 或自定义字段。
- **涨跌停限制 (`limit_threshold`)**: 静态阈值（如 `0.095` 代表 9.5% 涨跌停保护）。命中涨停禁止买入（`limit_buy`），命中跌停禁止卖出（`limit_sell`）。在策略层支持 `forbid_all_trade_at_limit`。
- **停牌处理 (`check_stock_suspended`)**: 若当日行情缺失或 `$close` 为 NaN，判定为停牌，禁止任何买卖。
- **交易成本**:
  - `open_cost`: 买入佣金/经手费比例（默认 `0.0015`，官方 baseline 配 `0.0005`）。
  - `close_cost`: 卖出佣金+印花税比例（默认 `0.0025`，官方 baseline 配 `0.0015`）。
  - `min_cost`: 单笔最低手续费（默认 `5.0` 元人民币）。
  - `impact_cost`: 滑点与市场冲击模型，按订单金额占当日总成交金额的比例加权：$\text{adj\_cost} = \text{impact\_cost} \times (\frac{\text{trade\_val}}{\text{total\_trade\_val}})^2$。
- **交易单位 (`trade_unit`)**: 默认 A 股为 100 股（整手交易）。`round_amount_by_trade_unit` 结合 `$factor` 将复权交易股数向下取整为整手（卖出清仓时不受整手限制）。

### 3. A 股实盘回测特别注意事项（能力边界与核实项）

| 功能项 | Qlib 一手代码支持状态 (Verified) | 需要 investment-lab 自行实验验证的部分 |
| :--- | :--- | :--- |
| **整手交易 (100股)** | `[Verified]` 支持（通过 `trade_unit=100` 与 `$factor` 取整） | 复权价格折算在极端拆股送股时是否产生碎股尾差 |
| **涨跌停限制** | `[Verified]` 支持静态涨跌停禁止买卖 | 注册制（20% 涨跌停）、科创板/北交所、ST (5%) 差异化动态涨跌停 |
| **停牌不可交易** | `[Verified]` 支持（NaN `$close` 判定为停牌） | 长期停牌标的复牌补跌时持仓净值突变对风控的影响 |
| **T+1 交易规则** | `[Reported]` 仅在 `TopkDropoutStrategy` 策略层提供 `hold_thresh=1` 持仓天数检查 | 账户层（Account/Position）是否严格区分当日可用余额与冻结持仓；非 Topk 策略下的 T+1 行为 |
| **分红送转与派息** | `[Verified]` 依赖离线除权因子 `$factor` 调整价格 | 回测中分红现金是否动态注入 `cash` 账户，还是仅以纯资本利得计价 |
| **历史印花税变动** | `[Verified]` 仅支持全局固定单一 `close_cost` 费率 | 需验证是否能根据历史时间分段应用不同印花税率（如 2023 年 8 月减半） |

---

## Official Alpha158 + LightGBM baseline

[Source Fact]  
- **Source Path**: `examples/benchmarks/LightGBM/workflow_config_lightgbm_Alpha158.yaml`
- **Ref / Commit**: `79633dd9506ea689e5400dea0197717b5b3d74b7`

```yaml
qlib_init:
    provider_uri: "~/.qlib/qlib_data/cn_data"
    region: cn
market: &market csi300
benchmark: &benchmark SH000300
data_handler_config: &data_handler_config
    start_time: 2008-01-01
    end_time: 2020-08-01
    fit_start_time: 2008-01-01
    fit_end_time: 2014-12-31
    instruments: *market
port_analysis_config: &port_analysis_config
    strategy:
        class: TopkDropoutStrategy
        module_path: qlib.contrib.strategy
        kwargs:
            signal: <PRED>
            topk: 50
            n_drop: 5
    backtest:
        start_time: 2017-01-01
        end_time: 2020-08-01
        account: 100000000
        benchmark: *benchmark
        exchange_kwargs:
            limit_threshold: 0.095
            deal_price: close
            open_cost: 0.0005
            close_cost: 0.0015
            min_cost: 5
task:
    model:
        class: LGBModel
        module_path: qlib.contrib.model.gbdt
        kwargs:
            loss: mse
            colsample_bytree: 0.8879
            learning_rate: 0.2
            subsample: 0.8789
            lambda_l1: 205.6999
            lambda_l2: 580.9768
            max_depth: 8
            num_leaves: 210
            num_threads: 20
    dataset:
        class: DatasetH
        module_path: qlib.data.dataset
        kwargs:
            handler:
                class: Alpha158
                module_path: qlib.contrib.data.handler
                kwargs: *data_handler_config
            segments:
                train: [2008-01-01, 2014-12-31]
                valid: [2015-01-01, 2016-12-31]
                test: [2017-01-01, 2020-08-01]
    record: 
        - class: SignalRecord
          module_path: qlib.workflow.record_temp
          kwargs: 
            model: <MODEL>
            dataset: <DATASET>
        - class: SigAnaRecord
          module_path: qlib.workflow.record_temp
          kwargs: 
            ana_long_short: False
            ann_scaler: 252
        - class: PortAnaRecord
          module_path: qlib.workflow.record_temp
          kwargs: 
            config: *port_analysis_config
```

---

## Version / stability notes

### 1. 版本现状与关系

[Source Fact]  
- **当前最新 Stable Release**: `v0.9.7`（发布于 2025-08-15，tag SHA: `da920b7f954f48ab1bb64117c976710de198373e`）。
- **当前 Remote Main Branch**: commit `79633dd9506ea689e5400dea0197717b5b3d74b7`。
- `v0.9.7` 主要改动包括：
  - 引入 `BaseDataHandler` 并重构统一的 fetch 接口；
  - 增加 Parquet 原生数据格式支持；
  - 更新 `risk_analysis` 支持几何累计收益模式；
  - 依赖库升级（适配最新 LightGBM、pydantic-settings）。

### 2. 后续 Spike 版本锁定建议

[Interpretation]  
- **建议锁定 Stable Tag `v0.9.7` 或特定 Commit**:
  1. Qlib 的 main 分支处于持续迭代状态，涉及实验性 RL 框架及数据层重构，直接拉取 main 分支可能引入未发布的依赖变动或非向后兼容的接口调整。
  2. 固定在 `v0.9.7` 有利于保障 `investment-lab` 在后续进行 Spike 验证时的环境可复现性与依赖确定性。

---

## Durable ideas worth Browser reviewing (长期有效的方法论启示)

1. **时序与截面双重解耦**:
   - 因子计算在时序维度（Rolling / Elem Operator）完成；
   - 截面数据预处理与信号检验在截面维度（Cross-sectional Normalization / IC 统计）完成；
   - 避免在底层特征生成阶段过早混入截面统计量，确保数据加载的并行性与缓存复用。
2. **两阶段评估哲学 (Signal-Level vs. Portfolio-Level)**:
   - 先通过 `SigAnaRecord` (IC, Rank IC, ICIR) 观察预测信号的纯粹排序能力与信噪比；
   - 信号具备统计基础后，再进入 `PortAnaRecord` (TopkDropout / 优化器回测) 评估组合构建、换手率与交易摩擦。
3. **严格的防未来信息泄漏设计**:
   - 标签定义必须明确时序位移（如 $T$ 日信号对应 $T+1$ 到 $T+2$ 的收益）；
   - 预处理器的拟合区间（`fit_start_time` ~ `fit_end_time`）应与训练集对齐，避免全样本统计量泄漏。

---

## Version-specific facts that require live re-check (需实测核对的特定版本细节)

1. **Python 3.10+ / 3.13 兼容性与 C 扩展编译**:
   - Qlib 包含 Cython 编译加速模块与 C++ 表达式算子，在 macOS ARM (Apple Silicon) 及高版本 Python 下的编译与安装行为需要实测。
2. **数据源采集器 (Data Collector) 的有效性**:
   - `scripts/data_collector/yahoo` 及国内数据抓取脚本依赖第三方接口，历史上易受外部反爬或格式调整影响，需实测现有数据下载通道是否畅通。

---

## Open questions for investment-lab (留待本实验室回答的开放问题)

1. **多资产扩展能力**: Qlib 架构天然偏向股票截面选股（如 CSI300 / CSI500），`investment-lab` 的基金研究（ETF / 场外公募基金筛选）如何适配其 `DataHandler`？
2. **轻量化独立集成 vs. 全重量引入**: 我们是提取其因子表达式体系与 IC 评估算法作为独立模块，还是将 Qlib 作为重型后端服务运行？
3. **A 股特色约束增强**: 针对 ST 股票动态过滤、可转债、打新收益及动态印花税，是否需要在 Qlib `Exchange` 基础上构建定制化的交易模拟器？

---

## Primary-source index (一手证据来源索引)

| 事实 / 结论主题 | 源码 / 文档路径 | 固定 Ref / Tag | 支持的事实说明 |
| :--- | :--- | :--- | :--- |
| **量化流程与四层架构** | `docs/introduction/introduction.rst` | `79633dd` | 官方四层架构定义与量化闭环流程描述 |
| **数据层与文件存储** | `docs/component/data.rst` | `79633dd` | `.bin` 格式、`dump_bin.py`、DataLoader/DataHandler 结构 |
| **Alpha158 特征库** | `qlib/contrib/data/handler.py` & `qlib/contrib/data/loader.py` | `79633dd` | `Alpha158` 默认配置 (Kbar 9 + Price 4 + Rolling 145 = 158) 及标签定义 |
| **表达式引擎算子** | `qlib/data/ops.py` | `79633dd` | 时序滚动算子、`Rank(X, N)`（Rolling Rank）等算子定义 |
| **Processor 防未来泄露** | `qlib/data/dataset/handler.py` | `79633dd` | `DataHandlerLP` 的 `fit_start_time` / `fit_end_time` 机制接口 |
| **PIT 财报时点数据库** | `docs/advanced/PIT.rst` | `79633dd` | 针对财报修正的时点数据防泄漏存储规范 |
| **IC / Rank IC 算法** | `qlib/contrib/eva/alpha.py` | `79633dd` | `calc_ic` 中 Pearson IC、Spearman Rank IC 与 ICIR 实现 |
| **信号记录与分析器** | `qlib/workflow/record_temp.py` | `79633dd` | `SignalRecord` 与 `SigAnaRecord` 的依赖关系与输出指标 |
| **Topk 轮换选股策略** | `qlib/contrib/strategy/signal_strategy.py` | `79633dd` | `TopkDropoutStrategy` 结合得分调仓与 `hold_thresh` 逻辑 |
| **撮合回测与交易约束** | `qlib/backtest/exchange.py` | `79633dd` | 涨跌停、停牌、100股整手、成本费率与滑点模型实现 |
| **官方经典基线配置** | `examples/benchmarks/LightGBM/workflow_config_lightgbm_Alpha158.yaml` | `79633dd` | Alpha158 + LightGBM + CSI300 完整基线参数 |
| **最新发布与变更记录** | `CHANGES.rst` & GitHub Release `v0.9.7` | `v0.9.7` | 版本演进历史、接口重构与 `v0.9.7` 特性清单 |
