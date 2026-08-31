# ai-berkshire — Investment Research Guidance for investment-lab

> **Status:** Repo-native advisory methodology / research guidance
>
> **Canonical primary source:** https://github.com/xbtlin/ai-berkshire
>
> **Current project research:**
> `#6 Evaluate ai-berkshire for investment research skills`
>
> **Evidence package:**
> `../ai-berkshire-source-harvest.md`
>
> **Reviewed upstream snapshot:**
> `fef5533145e2a505c7e07592d61165c7485a98b9`
>
> **Reviewed investment-lab harvest:**
> `38cd168de0c46574be22861d7875e44049d597be`
>
> **Current investment-lab hypothesis:**
> `REFERENCE` — selected methods are useful candidates for local adaptation,
> but investment-lab should not depend on ai-berkshire as a framework.

This document is not ai-berkshire documentation.

It records selected research disciplines that may improve Browser judgment
when designing company, industry, management, earnings, and investment-thesis research.

ai-berkshire does not override investment-lab project rules,
verified evidence, experiment results, or later investment-lab decisions.

Its value-investing worldview is also not automatically
investment-lab's investment philosophy.

---

## 1. When Browser should consult this guidance

Consult this Guidance when the current problem materially involves:

- researching one company;
- understanding a business model;
- management quality or capital allocation;
- industry structure or supply-chain positioning;
- financial statement analysis;
- earnings review;
- testing an investment thesis;
- monitoring whether an earlier thesis has changed;
- designing evidence discipline for AI investment research;
- deciding whether multiple independent research agents would add value.

Do not consult it merely because the topic is "investment".

For factor research, signal analysis, machine-learning stock selection,
or quantitative backtesting, Qlib Guidance is normally more relevant.

For live facts such as:

- current financial statements;
- current share price;
- management changes;
- current competitors;
- current regulation;
- latest earnings;
- current APIs or upstream Skill implementations;

return to current primary sources.

This Guidance stores relatively durable research principles,
not permanent factual snapshots.

---

## 2. Separate research method from investment philosophy

The most important boundary in ai-berkshire is:

> A useful research discipline
> is not the same thing as
> a correct investment philosophy.

ai-berkshire is strongly influenced by Buffett,
Munger, Duan Yongping, Li Lu, and value investing.

That perspective can generate useful questions.

For example:

- What would make this company fail?
- Is management doing what it previously promised?
- What facts would invalidate the thesis?
- Are reported profits supported by cash flow?
- What assumptions are hidden inside valuation?

These questions are broadly useful.

But rules such as:

- require ten-year certainty;
- require a specific margin of safety;
- reject companies after several years of negative FCF;
- require particular ROE or margin thresholds;
- force every company into a moat score;
- require a buy / sell conclusion;

are investment-style choices or heuristics.

Browser must not silently convert them into
investment-lab-wide rules.

---

## 3. Start with evidence quality before interpretation

One of the strongest reusable ideas is:

> Before asking "What does this mean?",
> first ask "How trustworthy is the evidence?"

Research quality depends on both:

Information availability
+
Evidence quality.

A company with abundant information creates one risk:

> repeating market consensus without independent verification.

A company with sparse information creates another:

> inventing plausible-looking details to fill the gaps.

Browser should therefore explicitly distinguish:

- directly verified facts;
- secondary-source claims;
- calculations;
- estimates;
- interpretations;
- unresolved uncertainty.

When evidence is weak,
the correct output can be:

> We do not know yet.

More analysis is not automatically better than
clearly stated uncertainty.

---

## 4. Important financial facts should be independently checked

ai-berkshire contains useful discipline around financial data verification.

The durable principle is not a particular website
or one fixed numerical tolerance.

It is:

> Important financial facts should not depend on one unverified number.

For material values such as:

- revenue;
- profit;
- cash flow;
- share count;
- market capitalization;
- valuation multiples;
- debt;
- currency conversions;

Browser should prefer primary filings
and independently check important calculations when practical.

Simple deterministic calculations should preferably be performed
with deterministic tools rather than LLM mental arithmetic.

Examples include:

Market capitalization
=
Share price × Shares outstanding

or explicit valuation formulas.

If two sources disagree,
do not average them mechanically.

First investigate:

- accounting definition;
- GAAP / Non-GAAP differences;
- reporting period;
- currency;
- share-class treatment;
- restatements;
- source freshness.

The exact thresholds used by ai-berkshire
are implementation choices,
not universal investment-lab rules.

---

## 5. Expose assumptions instead of hiding them inside a number

Valuation models can create false precision.

A model can be mathematically correct
while its assumptions are unreasonable.

When Browser uses valuation,
important assumptions should remain visible.

For example:

- expected growth;
- margins;
- return on invested capital;
- reinvestment requirements;
- cost of capital;
- terminal assumptions;
- scenario probabilities;
- currency and inflation basis.

Useful practice:

Assumption
↓
Calculation
↓
Sensitivity
↓
Interpretation

Do not present the final valuation number
without showing which assumptions dominate it.

ai-berkshire contains specific rules such as
particular discount-rate bands,
terminal-growth ranges,
and an `r-g` minimum spread.

Those are upstream heuristics and snapshot-specific assumptions.

They may inspire checks,
but must not become permanent investment-lab financial laws.

---

## 6. Research should try to break the thesis

A strong research process should not only accumulate supporting evidence.

It should actively search for:

> What would make this idea wrong?

Useful questions include:

- Why might a knowledgeable investor avoid this company?
- What would destroy the business model?
- Which assumption is most fragile?
- Which competitor could invalidate the thesis?
- What regulatory change would matter?
- Which management behavior would change our judgment?
- Which financial metric would contradict the story?

This is more durable than adopting a fixed
"bear case" checklist.

The objective is falsification:

Hypothesis
↓
Evidence that should be true
↓
Evidence that would break it
↓
Future observation

Browser should preserve contrary evidence
instead of resolving every disagreement
into a single confident narrative.

---

## 7. Management research should focus on observable behavior

"Good management" is too vague to be useful.

A more useful research question is:

> What has management repeatedly done?

Possible evidence includes:

- previous promises versus later results;
- acquisitions and their later outcomes;
- buybacks and issuance;
- capital allocation;
- dilution;
- responses to mistakes;
- treatment of shareholders;
- changes in disclosure;
- strategic consistency;
- governance events.

The reusable principle from ai-berkshire is:

> Evaluate management through historical observable behavior,
> not personality impressions.

Specific numerical scoring thresholds
should remain hypotheses or implementation choices,
not universal rules.

---

## 8. Earnings analysis should prioritize new information

A quarterly earnings review should not become
a complete company research report every quarter.

Its main question is:

> What new evidence changed since the previous thesis?

Useful areas include:

- revenue and margin changes;
- cash-flow quality;
- balance-sheet changes;
- segment changes;
- guidance;
- management commitments;
- accounting policy changes;
- customer concentration;
- stock-based compensation;
- related-party transactions;
- unusual footnotes.

This encourages incremental research
rather than repeatedly rewriting the same company description.

---

## 9. Track thesis change separately from price change

One of the most reusable ideas in ai-berkshire is
explicit thesis tracking.

Before relying on an investment thesis,
write down the important assumptions.

Later events can then be classified approximately as:

Improved
/
Unchanged
/
Weakened

The important distinction is:

Fact changed
≠
Price changed
≠
Wording changed.

A stock falling sharply does not by itself mean
the business thesis weakened.

A rising stock does not prove
the thesis improved.

Likewise, two reports using different language
may describe exactly the same underlying facts.

Browser should compare new evidence against
the earlier hypothesis,
not against the emotional direction of the price.

---

## 10. Use multiple Agents only when independence adds information

ai-berkshire frequently uses multiple research Agents.

The reusable lesson is not:

> Four Agents are always better than one.

Multi-Agent research is useful when independent work can materially improve:

- evidence coverage;
- domain specialization;
- adversarial challenge;
- independent judgment;
- context isolation.

For example:

Business
+
Financials
+
Competition
+
Risk

can be investigated separately
and then synthesized.

But four Agents searching the same documents
with slightly different personalities
may only multiply:

- repeated searches;
- token cost;
- duplicated facts;
- superficial disagreement.

The decision should therefore be:

> Does independent context materially improve this research?

If not,
use one Agent.

Do not create extra Agents merely to imitate
Buffett, Munger, Duan Yongping, or Li Lu.

Persona diversity is not the same thing as
evidence diversity.

---

## 11. Separate research generation from quality control

Another useful architectural idea is:

Research generation
↓
Independent checking
↓
Release

A report should not become trusted merely because
the same Agent that wrote it says it is correct.

Useful independent checks can include:

- recalculating selected financial values;
- checking source provenance;
- re-reading selected primary disclosures;
- verifying units and currencies;
- checking citations;
- sampling important claims;
- testing whether assumptions are visible.

ai-berkshire uses specific mechanisms such as
15% random sampling and 1% tolerance.

Those exact numbers are implementation choices.

investment-lab should preserve the principle:

> Important research deserves an independent quality gate
> proportional to its risk and importance.

---

## 12. Do not inherit these automatically

Do not automatically import:

- Buffett / Munger / Duan Yongping / Li Lu personas;
- quotations or personality simulation;
- subjective 1–5 star ratings;
- fixed ROE / FCF / gross-margin rejection rules;
- ten-year certainty as a universal requirement;
- fixed margin-of-safety thresholds;
- mandatory buy / hold / sell conclusions;
- upstream website choices;
- hard-coded local paths;
- upstream valuation parameter bands;
- its exact 15% / 1% audit thresholds;
- publishing / WeChat article workflows;
- self-reported portfolio performance;
- upstream sample investment conclusions;
- all upstream Skills.

These may be useful examples.

They are not automatically
investment-lab architecture or investment doctrine.

---

## 13. Potential future local capabilities

The Source Harvest suggests several potentially useful
investment-lab capabilities:

company research

investment thesis tracking

earnings review

management research

financial-data verification

independent research audit

These are candidates, not commitments.

Do not create them merely because
ai-berkshire has similar Skills.

A local Skill should be created only after
investment-lab encounters a repeated research workflow
where a reusable Skill would reduce error or duplicated effort.

---

## 14. Current investment-lab judgment

Current hypothesis:

**REFERENCE**

ai-berkshire contains several valuable research disciplines.

Especially useful are:

- evidence-quality awareness;
- primary-source preference;
- independent financial verification;
- explicit uncertainty;
- falsification;
- management promise-versus-result tracking;
- incremental earnings review;
- thesis change detection;
- separating research generation from audit;
- using multiple Agents only when independence provides real value.

However:

investment-lab should not currently depend on ai-berkshire's codebase,
investment worldview,
persona structure,
or full Skill system.

The preferred direction is:

Learn methods
↓
Validate them in real investment-lab work
↓
Promote only repeated useful patterns
↓
Create local Guidance / Skills when justified

not:

Install ai-berkshire
↓
Make investment-lab conform to it.

---

## 15. Live-check boundary

Do not rely on this Guidance alone for questions such as:

- What Skills does ai-berkshire currently contain?
- How does its current Agent implementation work?
- Which tools or websites does it currently use?
- What is its latest directory structure?
- What does its newest financial-rigor code do?
- Has its multi-Agent architecture changed?
- Has a specific upstream heuristic been revised?

For those questions:

return to the current canonical repository.

Canonical repository:

https://github.com/xbtlin/ai-berkshire

Evidence snapshot used during this distillation:

ai-berkshire:
fef5533145e2a505c7e07592d61165c7485a98b9

investment-lab reviewed harvest:
38cd168de0c46574be22861d7875e44049d597be
