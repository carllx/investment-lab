# Qlib — Quant Research Guidance for investment-lab

> **Status:** Repo-native advisory methodology / research guidance
>
> **Canonical primary source:** https://github.com/microsoft/qlib
>
> **Current project research:**<br>
> `#4 Evaluate Qlib for stock & factor experiments`
>
> **Evidence package:**<br>
> `../qlib-source-harvest.md`
>
> **Reviewed Qlib snapshot:**<br>
> `79633dd9506ea689e5400dea0197717b5b3d74b7`
>
> **Current investment-lab hypothesis:**<br>
> `PARTIAL` — pending real experiment validation.

This document is not Qlib documentation.

It records selected ideas from Qlib that may improve Browser
judgment when designing quantitative investment experiments.

Qlib and this document do not override investment-lab project rules,
verified experiment evidence, or later decisions.

---

## 1. When Browser should consult Qlib

Consult this guidance when the current problem materially involves:

- 股票因子或特征研究；
- 机器学习选股；
- train / validation / test；
- IC / Rank IC；
- 信号质量；
- 股票组合构建；
- 回测；
- 交易成本；
- 数据泄漏；
- 如何组织一个可重复的量化实验。

不要因为问题属于“投资”就机械读取 Qlib。

如果判断依赖当前：

- API；
- 安装方式；
- Python 支持；
- 数据格式；
- 模型；
- release；
- 数据下载能力；
- 交易模拟能力；

必须重新检查当前 Qlib GitHub / 官方文档。

本 Guidance 主要保存较稳定的研究方法，
不是当前产品事实的永久快照。

---

## 2. The most useful idea: separate the experiment into layers

Qlib 最值得 investment-lab 借鉴的，不是模型数量。

而是不要把：

“我有一个股票想法”

直接跳成：

“这个策略最后赚了多少钱”。

一个量化实验可以拆成：

Data<br>
↓<br>
Feature / Factor<br>
↓<br>
Dataset<br>
↓<br>
Model / Rule<br>
↓<br>
Prediction / Signal<br>
↓<br>
Signal Analysis<br>
↓<br>
Portfolio / Strategy<br>
↓<br>
Backtest<br>
↓<br>
Portfolio Analysis

简单理解：

- **Data**：历史市场数据。
- **Factor / Feature**：给股票描述或打分的特征。
- **Model / Rule**：利用这些特征生成预测。
- **Signal**：最终产生的股票分数。
- **Backtest**：假装回到过去，只使用当时能够知道的信息进行模拟。

这种分层最重要的价值是：

> 实验失败时，我们更容易知道到底哪一层出了问题。

Browser 在设计实验时应尽量保持这些问题可分开检查。

---

## 3. Check signal quality separately from trading profit

Qlib 把 Signal Analysis 和 Portfolio Backtest 分开。

这个思想值得长期保留。

例如我们提出：

> “过去 20 天表现强的股票，
> 下一段时间是否通常也表现更强？”

不要第一步只看：

> “最后赚了多少？”

可以先检查：

> 分数更高的股票，
> 后来的表现是否总体也更好？

Qlib 中常见的工具包括：

### IC

简单理解：

> 股票预测分数与之后实际收益之间有没有统计关系。

### Rank IC

简单理解：

> 即使具体收益数字预测不准，
> 股票由好到坏的排序是否具有一定一致性。

IC / Rank IC 是：

> 信号质量检查工具。

它们不是：

> 盈利证明。

信号统计不错，不保证最终策略赚钱。

回测最终赚钱，也不能单靠最终收益证明模型可靠。

两层结果不一致时，可以继续检查：

- 组合构建；
- 市场环境；
- 换手率；
- 手续费；
- 成交限制；
- 数据质量；
- 研究设计。

这些结果提供排查线索，
但不能单独证明具体原因。

---

## 4. Time must really move forward

量化研究最大的风险之一是：

> 模拟过去时，不小心使用了当时其实还不知道的未来信息。

这叫 **look-ahead bias（前视偏差）**。

可以理解成：

> 考试前偷偷看到了答案。

Browser 设计时间序列实验时应检查：

过去
→ train

之后
→ validation

再之后、没有用于开发
→ test

股票时间序列通常不应该像普通独立样本那样随意随机打乱。

还应该特别检查：

- 预处理统计量是不是只根据训练期拟合；
- 财报在那个历史时间点是否真的已经公布；
- 标签引用的是哪一天的价格；
- 信号在什么时间实际能够生成；
- 回测成交发生在信号生成之后还是之前。

Qlib 提供了一些帮助控制这些问题的机制，
例如时间切分、fit interval 和 PIT 数据支持。

但：

> Framework 提供防护机制<br>
> ≠ 任意实验配置自动没有数据泄漏。

研究设计仍然需要 Browser / IDE 主动验证。

---

## 5. Keep the data layer replaceable

Qlib 将：

DataLoader<br>
↓<br>
DataHandler<br>
↓<br>
Dataset<br>
↓<br>
Model

分开。

值得 investment-lab 借鉴的不是这些类名本身，而是：

> 模型最好消费整理好的实验数据，
> 而不要直接绑定某个数据供应商。

未来数据可能来自：

- 自己的 CSV / Parquet；
- 数据库；
- OpenBB；
- AkShare；
- Tushare；
- 其他 provider。

如果换一个数据源就必须重写整个模型，
说明系统耦合过深。

因此 Qlib Spike 的一个重要 Gate 是：

> 我们自己的股票数据，
> 能否通过很薄的一层接入 Qlib？

而不是：

> 为了使用 Qlib，
> 先把整个 investment-lab 改造成 Qlib 数据体系。

---

## 6. Factors should be reproducible

Qlib Expression Engine 可以用明确公式描述股票特征。

值得借鉴的核心原则是：

> 一个因子应该能够被明确描述，
> 并在同样的数据条件下重新计算得到相同结果。

例如不要只写：

> “最近走势很好”。

应该尽量转化为可以计算的定义，例如：

> “当前价格相对过去 20 日平均价格的位置”。

这样才能：

- 重复实验；
- 回测；
- 比较；
- 修改；
- 验证；
- 排除模糊解释。

Alpha158 可以作为成熟特征库的参考案例。

但：

> Qlib 提供 158 个特征<br>
> ≠ investment-lab 应该默认使用全部 158 个。

---

## 7. Backtest is a simulator, not the market

Qlib Backtest / Exchange 可以表示多种交易条件，例如：

- 成交价格；
- 涨跌停；
- 停牌；
- 手续费；
- 最低手续费；
- 整手交易；
- 市场冲击。

这提醒我们：

> 回测不能只计算股票价格涨跌。

现实交易有摩擦和约束。

但同样：

> Qlib 能表达某一种交易限制<br>
> ≠ 它完整还原了中国 A 股真实制度。

当前尤其应在真实 Spike 中核实：

- T+1；
- 不同板块 / ST 的涨跌停；
- 历史规则变化；
- 历史交易费用变化；
- 分红现金处理；
- 停牌、退市等特殊情况。

这些目前属于验证问题，
不要提前写成 Qlib 已完整支持或完全不支持的永久事实。

---

## 8. Official baseline is an environment check, not an investment conclusion

Qlib 提供：

Alpha158<br>
+<br>
LightGBM<br>
+<br>
CSI300<br>
+<br>
TopkDropout<br>
+<br>
Backtest

这样的完整官方 baseline。

它首先适合帮助我们回答：

> “Qlib 的完整研究链条在我们的环境里能不能工作？”

第一次运行 baseline 的成功标准应该主要是：

- 可以复现；
- 流程能够理解；
- 中间结果可以检查；
- 输出能够解释。

而不是：

> “历史收益够不够高？”

历史 benchmark 不能直接证明今天仍然有投资价值。

---

## 9. Current investment-lab judgment

Current hypothesis:

**PARTIAL**

含义是：

某些股票 / 因子实验可以完整使用 Qlib。

但暂时不要：

- 让基金实验强制依赖 Qlib；
- 让公司基本面研究依赖 Qlib；
- 让整个 investment-lab 数据层依赖 Qlib；
- 因为 Qlib 功能很多就建立全局 Qlib infrastructure。

是否扩大使用范围，
必须由 #4 的真实 Spike 证据决定。

---

## 10. Evidence Browser should require from the Qlib Spike

未来 Browser 给 IDE 下发 Qlib 实验时，应重点取得：

1. 官方 Alpha158 + LightGBM baseline 能稳定运行。

2. 我们自己的小型股票数据能够接入 Qlib，
   而不需要重构整个 investment-lab。

3. 可以简单加入一个我们自己定义的因子。

4. 可以得到并理解 IC / Rank IC 等信号层结果。

5. 同一预测信号可以分别进入：
   - Qlib backtest
   - 一个透明的小型 baseline

   并解释两者结果差异。

6. A 股关键交易限制没有被静默忽略。

这些证据比“Qlib 有很多功能”更重要。

---

## 11. Do not inherit these automatically

不要因为 Qlib 提供以下能力，就自动把它们变成
investment-lab 的默认架构：

- 整套 YAML workflow；
- Qlib 数据目录作为唯一数据格式；
- 全部 model zoo；
- RL infrastructure；
- online serving；
- order execution framework；
- Alpha158 的全部 features；
- TopkDropout 作为默认投资策略。

只有真实实验产生需求后，再讨论是否采用。

---

## 12. Live-check boundary

以下问题不得只凭本 Guidance 回答：

- 当前最新 Qlib release 是什么？
- 当前 Python 支持范围是什么？
- macOS ARM 当前安装情况如何？
- 当前官方数据下载还能否使用？
- 当前 API 怎么写？
- 某项 A 股交易机制现在是否已经增加支持？
- 当前 benchmark 或模型有什么变化？

遇到这些问题：

> 回到当前 Qlib primary source。

Canonical repository:

https://github.com/microsoft/qlib

Evidence snapshot used during this distillation:

Qlib:
79633dd9506ea689e5400dea0197717b5b3d74b7

investment-lab reviewed harvest:
147f506349c97f0f88143ad0cdd80673f77b3e6a
