# TradingAgents — Multi-Agent Research Guidance for investment-lab

> **Status:** Repo-native advisory methodology / research guidance
>
> **Canonical primary source:** https://github.com/TauricResearch/TradingAgents
>
> **Current project research:**
> `#7 Evaluate TradingAgents as multi-agent research benchmark`
>
> **Evidence package:**
> `../tradingagents-source-harvest.md`
>
> **Reviewed upstream snapshot:**
> `a33fd4c0f134485a43553a2c23a63cb14adbd88f`
>
> **Reviewed investment-lab harvest:**
> `3c283f33923aaac03035ad2e5f06d7ef25824d96`
>
> **Current investment-lab hypothesis:**
> `REFERENCE` — useful as a multi-agent research benchmark and source of selected patterns,
> but investment-lab should not currently depend on the TradingAgents framework.

This document is not TradingAgents documentation.

It records selected ideas that may improve Browser judgment
when deciding whether an investment-research task benefits from
multiple Agents, independent evidence collection, adversarial review,
context isolation, or staged decision-making.

TradingAgents does not override investment-lab project rules,
verified evidence, experiment results, or later architectural decisions.

The existence of more Agents is not evidence of better research.

---

## 1. When Browser should consult this guidance

Consult this Guidance when the current problem materially involves:

- whether one Agent or multiple Agents should perform a research task;
- splitting investment research across different evidence domains;
- company research that combines fundamentals, market data, news, macro, and sentiment;
- independent evidence collection;
- adversarial or red-team review;
- qualitative versus deterministic risk control;
- long Agent workflows and context management;
- structured handoffs between research stages;
- repeated investment decisions with later reflection;
- evaluating the cost and value of multi-Agent orchestration.

Do not consult it merely because a task involves investment.

For:

- factor research;
- IC / Rank IC;
- quantitative backtesting;
- ML stock selection;

Qlib Guidance is normally more relevant.

For:

- company fundamentals;
- management;
- earnings;
- investment-thesis research;
- evidence discipline;

ai-berkshire Guidance is normally more relevant.

TradingAgents Guidance primarily answers:

> When does splitting research across Agents
> create real incremental value?

---

## 2. The central principle: more Agents need a reason

The most important lesson is not:

> Multi-Agent is better than Single-Agent.

It is:

> Add another Agent only when independence,
> specialization, or context separation creates
> information or reasoning value worth its cost.

A new Agent may add value through:

Evidence diversity

or

Reasoning diversity

or

Context isolation.

A new Agent that merely receives the same evidence,
uses the same tools,
and adopts a different personality
may add little beyond cost and verbosity.

Browser should therefore ask:

> What becomes meaningfully different
> because this Agent exists?

If the answer is only:

> "It has another role name",

that is not enough.

---

## 3. Distinguish three kinds of diversity

TradingAgents helps reveal an important distinction.

### Evidence diversity

Different research units obtain genuinely different evidence.

For example:

Market data

Fundamentals

News / macro

Sentiment

These can reveal different facts about the same investment question.

This is the strongest reason to separate research work.

### Reasoning diversity

Different reviewers examine the same evidence
using different hypotheses or analytical lenses.

For example:

- What supports the thesis?
- What would invalidate it?
- Which assumption is weakest?
- What alternative explanation fits the same evidence?

This may uncover blind spots.

But it does not create new external evidence.

### Persona diversity

Different Agents are instructed to behave as:

Bull

Bear

Aggressive

Conservative

Neutral

without receiving different evidence or tools.

Persona diversity can stimulate alternative reasoning,
but it must not be mistaken for independent evidence.

The hierarchy should usually be:

Evidence diversity
>
Reasoning diversity
>
Persona diversity.

---

## 4. Multi-Agent research is strongest when evidence domains differ

TradingAgents separates research into specialized analyst domains.

The reusable principle is:

> Split research when the evidence itself has
> meaningfully different sources, tools, or expertise requirements.

For example, one company question may involve:

Market behavior

Financial statements

Industry / macro conditions

News

Alternative sentiment data

These sources have different:

- retrieval methods;
- failure modes;
- update frequencies;
- definitions;
- context requirements.

Separate research contexts can therefore improve coverage.

But this does not mean investment-lab should always create
one permanent Agent for every data category.

The split should follow the research problem.

A task involving only a financial filing
may need one Agent.

A task requiring five independent evidence domains
may justify several.

---

## 5. Separate evidence collection from synthesis

A useful architecture is:

Independent evidence collection
↓
Structured outputs
↓
Synthesis
↓
Decision

This is preferable to allowing every Agent
to continuously rewrite one shared conversation.

Why?

Because it makes it easier to inspect:

- what each researcher actually found;
- which source produced which claim;
- where disagreement first appeared;
- what synthesis changed;
- whether later conclusions lost important evidence.

The analyst stage should primarily answer:

> What evidence did we obtain?

The synthesis stage should answer:

> What does the combined evidence imply?

Those are different jobs.

---

## 6. Context isolation can be valuable without hiding shared results

TradingAgents explicitly resets the LangGraph message history
between analyst nodes.

The durable idea is not the exact `RemoveMessage` implementation.

It is:

> Independent research tasks should not automatically inherit
> every previous tool trace, failed query, and reasoning fragment.

A clean research context can reduce:

- prompt contamination;
- attention dilution;
- irrelevant tool history;
- accidental anchoring;
- context-window growth.

But isolation does not require complete state separation.

A useful pattern is:

Researcher A context
→ structured result

Researcher B fresh context
→ structured result

Shared state
→ stores both results

Synthesis
→ consumes the results.

Browser should distinguish:

fresh reasoning context

from

shared canonical evidence.

---

## 7. Prefer structured contracts between stages

TradingAgents increasingly uses structured schemas
between some workflow stages.

The reusable principle is:

> Important Agent-to-Agent handoffs should have
> a clear semantic contract.

Instead of passing only a long essay,
a research result may explicitly contain:

- conclusion;
- evidence;
- uncertainty;
- key metrics;
- contradicting evidence;
- unresolved questions;
- recommended next check.

Structured output makes downstream reasoning easier to inspect.

However:

Structured schema
≠
truth.

A confidently structured hallucination is still wrong.

Evidence provenance remains necessary.

---

## 8. Adversarial review should attack claims, not perform a role

TradingAgents contains Bull/Bear debate.

Its implementation shows an important boundary:

The Bull and Bear roles receive the same upstream research
and do not independently retrieve external evidence.

They therefore cannot create new external facts.

They can still create reasoning diversity by:

- challenging assumptions;
- proposing counterexamples;
- emphasizing neglected risks;
- testing alternative interpretations.

This can be useful.

But a stronger adversarial-review pattern is:

Claim
↓
Counter-hypothesis
↓
What evidence would discriminate between them?
↓
Retrieve / verify that evidence
↓
Update judgment

rather than:

Bull persona
vs
Bear persona.

For important research,
the strongest critic should ideally have permission
to search for disconfirming evidence.

---

## 9. Do not force debate into every research task

Debate creates cost.

It can also create artificial disagreement.

If evidence is already:

clear,

low-risk,

well-verified,

and internally consistent,

forcing multiple Agents to argue opposing positions
may produce rhetoric rather than insight.

Browser should trigger deeper adversarial review
when there is a concrete reason, such as:

- material evidence conflict;
- high uncertainty;
- high-cost decision;
- fragile assumptions;
- extreme valuation disagreement;
- suspicious financial evidence;
- unresolved regulatory or competitive risk.

The purpose of adversarial review is:

find failure modes,

not:

produce equal amounts of bullish and bearish prose.

---

## 10. Risk research and risk enforcement are different jobs

TradingAgents uses Aggressive, Conservative,
and Neutral risk personas.

These roles can provide qualitative perspectives.

But they do not create deterministic portfolio constraints.

investment-lab should distinguish:

### Qualitative risk research

Examples:

- regulatory uncertainty;
- geopolitical exposure;
- management credibility;
- competitive disruption;
- litigation;
- business-model fragility.

Agent reasoning can help here.

### Deterministic risk enforcement

Examples:

- maximum position size;
- portfolio concentration;
- liquidity minimums;
- volatility budget;
- maximum leverage;
- stop-loss rule;
- portfolio exposure;
- transaction constraints.

Where a rule can be encoded deterministically,
it should normally be enforced by deterministic computation.

Therefore:

Agent qualitative risk review
+
deterministic risk controls

is usually stronger than:

multiple risk personas
without enforceable constraints.

---

## 11. Minimize information bottlenecks between stages

TradingAgents includes several sequential roles:

Analysts
→ Researchers
→ Research Manager
→ Trader
→ Risk Debate
→ Portfolio Manager.

Each handoff can add useful specialization.

But every handoff can also lose information.

For example,
the Trader consumes the Research Manager's investment plan
rather than the full original analyst evidence.

This illustrates a general risk:

Compression
→ Compression
→ Compression
→ Decision

may gradually remove uncertainty,
minority evidence,
or important caveats.

Browser should therefore ask for each intermediate stage:

> Does this stage add a distinct function?

If not,
consider removing it.

A shorter decision chain is often easier to audit.

---

## 12. Multi-Agent architecture should be proportional to the task

A useful default is:

Simple task
→ simple topology.

Complex task
→ only as much decomposition as necessary.

Examples:

Single factual lookup
→ one Agent.

One filing plus deterministic calculations
→ one research Agent + calculation tools.

Company research across several independent evidence domains
→ several specialized researchers + synthesis.

High-risk decision with conflicting evidence
→ specialized researchers + targeted adversarial review + quality gate.

Do not build a simulated investment bank
for every question.

The process cost should remain proportional
to the value and uncertainty of the research.

---

## 13. Reflection is not model learning

TradingAgents records earlier decisions,
later observes short-horizon outcomes,
and generates retrospective lessons.

This can be useful as a research log.

But Browser must distinguish:

Persistent memory
≠
model training.

Reflection text
≠
reinforcement learning.

Past outcome
≠
proof that the original reasoning was correct or incorrect.

A five-day price move can contradict a trade direction
without invalidating a long-term business thesis.

Likewise,
a profitable outcome can occur for the wrong reason.

Any reflection system should therefore track separately:

Original hypothesis

Expected horizon

Expected evidence

Observed outcome

What actually changed

What remains uncertain.

---

## 14. Reflection must obey time boundaries

Historical reflection introduces a serious risk:

future information can leak backward into simulated research.

When evaluating historical decisions,
Browser must verify:

At simulated date T,
what information was actually available?

A lesson generated using T+5 outcome data
must not be available to a decision simulated at T+1.

This is the same general principle as
look-ahead bias in quantitative research.

Memory systems do not remove
the need for temporal discipline.

---

## 15. Do not infer framework superiority from the published backtest

TradingAgents' official paper reports strong results.

But the evidence does not establish that
the multi-Agent architecture itself caused those results.

Important limits include:

- no Single-Agent LLM baseline;
- no component ablation for debate or risk layers;
- a short reported test window;
- limited publicly tabulated ticker results;
- no reported statistical significance analysis;
- unclear treatment of several real-world trading frictions.

The paper and the current 2026 codebase
also belong to different implementation generations.

The paper used an earlier model / workflow configuration,
while the reviewed current code uses a later architecture
and different default models.

Therefore:

Reported backtest performance
≠
proof of current framework performance.

And:

TradingAgents performance
≠
proof that Multi-Agent is better than Single-Agent.

Treat the paper as:

reported historical evidence,

not adoption proof.

---

## 16. Cost is part of architecture quality

TradingAgents illustrates that multi-Agent design
has structural cost.

Each additional stage may add:

- LLM calls;
- tool calls;
- latency;
- repeated evidence;
- formatting failure risk;
- state complexity;
- provider cost;
- retry complexity.

The original paper itself reported
a relatively large number of model and tool calls per prediction.

Current code may differ.

Browser should therefore evaluate:

Incremental research value
÷
Incremental orchestration cost.

A workflow that produces slightly richer prose
at many times the cost
may be worse engineering.

---

## 17. A practical Single-Agent vs Multi-Agent routing rule

Start with one Agent unless there is a concrete reason to split.

Move toward multiple Agents when at least one of these is true:

### Different evidence domains

The task requires genuinely different sources,
tools, or expertise.

### Independent verification

An important claim deserves a second,
independent evidence path.

### High-value adversarial challenge

The decision is costly enough that
actively searching for falsifying evidence is worthwhile.

### Context isolation

One research lane would become so large
that separate clean contexts materially improve quality.

### Parallelizable research

Independent evidence lanes can proceed separately
without shared mutable state.

Do not add Agents primarily for:

- role-play;
- impressive organization charts;
- symmetric bull/bear prose;
- artificial committee structure.

---

## 18. Prefer targeted challenge over permanent debate teams

A useful investment-lab pattern may be:

Research
↓
Detect uncertainty / contradiction
↓
Spawn targeted critic
↓
Critic receives explicit falsification mission
↓
Critic may retrieve new evidence
↓
Synthesis

rather than:

Every task
↓
Bull
↓
Bear
↓
Manager.

This keeps adversarial work connected
to an actual unresolved question.

The critic's job should be:

break or strengthen the hypothesis,

not:

perform pessimism.

---

## 19. Separate research quality control from investment action

TradingAgents eventually converts research
into Buy / Hold / Sell decisions.

investment-lab should not automatically do this.

Research may legitimately end with:

- insufficient evidence;
- unresolved contradiction;
- watch condition;
- experiment needed;
- data gap;
- thesis weakened but not falsified.

Do not force every research workflow
to produce a trade action.

Research quality
and
portfolio action

are separate decisions.

---

## 20. Do not inherit these automatically

Do not automatically copy:

- the exact Agent count;
- the exact analyst names;
- mandatory Bull/Bear debates;
- Aggressive / Conservative / Neutral personas;
- fixed debate-round counts;
- the full simulated trading-firm hierarchy;
- the Trader intermediary layer;
- LangGraph-specific state machinery;
- SQLite checkpoint implementation;
- current provider defaults;
- current data-vendor choices;
- exact prompts;
- full-report repetition between debate nodes;
- current memory format;
- current five-day reflection horizon;
- reported historical trading performance.

These are implementation choices or examples.

They are not investment-lab requirements.

---

## 21. Potential future investment-lab pattern

A lightweight reusable architecture worth testing is:

Independent evidence lanes
↓
Structured evidence package
↓
Synthesis
↓
Conditional adversarial review
↓
Deterministic checks
↓
Final judgment

Possible evidence lanes might include:

Company fundamentals

Market / price evidence

Industry / competition

Macro / policy

News / event evidence

But the actual lanes should be chosen
for the research question.

Do not create permanent Agents
before repeated work proves the need.

---

## 22. Current investment-lab judgment

Current hypothesis:

**REFERENCE**

TradingAgents is useful primarily as:

- a concrete multi-Agent architecture benchmark;
- an example of evidence-domain decomposition;
- an example of context management between research stages;
- a source of structured handoff ideas;
- a useful counterexample showing where persona diversity
  can be confused with evidence diversity.

The strongest reusable ideas are:

Evidence diversity

Context isolation

Structured stage contracts

Conditional adversarial review

Proportional orchestration

Deterministic hard-risk constraints
plus qualitative Agent risk analysis.

However:

investment-lab should not currently depend on TradingAgents,
copy its complete graph,
or assume its multi-Agent debates improve investment performance.

The preferred direction is:

Study the mechanisms
↓
Borrow only clearly useful patterns
↓
Test them in real investment-lab research
↓
Create local patterns or Skills only after repeated evidence

not:

Install TradingAgents
↓
Make investment-lab conform to its organization chart.

---

## 23. Live-check boundary

Do not rely on this Guidance alone for:

- the current TradingAgents Agent roster;
- current default LLM models;
- current provider support;
- current data vendors;
- current prompts;
- current LangGraph implementation;
- current memory / reflection behavior;
- installation instructions;
- current benchmark performance;
- current supported markets;
- current API configuration.

These are version-sensitive facts.

For those questions:

return to the current canonical repository
and current first-party documentation.

Canonical repository:

https://github.com/TauricResearch/TradingAgents

Evidence snapshot used during this distillation:

TradingAgents:
a33fd4c0f134485a43553a2c23a63cb14adbd88f

investment-lab reviewed harvest:
3c283f33923aaac03035ad2e5f06d7ef25824d96
