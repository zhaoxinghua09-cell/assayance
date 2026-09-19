# Assayance

**试真法 · Falsifiable Assurance**

> A coined theoretic term in the **LGD (凡自治之物 · 全程治理论)** theory stack.
> Theory-layer zero-collision: the descriptive English name is settled by others; the coined term is ours.

---

## The claim

> **A check that has never been observed failing has not been shown to be capable of failing.**
> **Therefore it is not yet a check — it is a decoration.**

Every assurance artifact makes the same promise: *if this were broken, I would tell you.* That promise is testable, and almost nobody tests it. A gate that cannot fail, a test that cannot go red, a policy that defaults to allow, an evidence artifact nobody recomputes, a document that describes a safeguard the code does not contain — all of these read as **assurance** while producing **none**.

**Assayance** is the discipline of **assaying your own instruments before you trust them.** It takes the oldest test in the world — rub the metal on the stone and see whether the streak is different — and applies it to the things that are supposed to do the telling.

## Why the term was coined

The descriptive lane is closed, and the Greek lane closed very recently. Both facts were measured, not assumed.

| Candidate | Finding | Verdict |
|---|---|---|
| `falsifiability` | Popper, settled | 🔴 taken |
| `negative control` | laboratory standard, settled | 🔴 taken |
| `mutation testing` | software standard, settled | 🔴 taken |
| `calibration` / `检定` | metrology standard, settled | 🔴 taken |
| `Basanos` (βάσανος, touchstone) | [`g-jensen/basanos`](https://github.com/g-jensen/basanos) — "an acceptance test framework for agentic orchestration"; `project-basanos` — "an agentic rules engine", BLOCK/ALLOW verdicts | 🔴 taken, **in this exact lane** |
| `Dokimasia` (δοκιμασία, scrutiny) | `deevus/dokimasia` — "pytest-first acceptance testing for agent capabilities" | 🔴 taken, in this lane |
| `Elenchus` (ἔλεγχος, cross-examination) | `elenchus-mcp` — "adversarial verification system" | 🔴 taken, in this lane |
| `Probatio` | `frenck/probatio` — data validation library | 🔴 taken |
| `Trutina` | an eval harness | 🔴 taken |
| `Assayance` | no repository, no technical use found | 🟢 **free** |

**The finding worth keeping:** the Greek vocabulary of *testing* has been systematically claimed by the 2025–26 wave of agent-verification tooling — touchstone, scrutiny, and cross-examination all now name agent test harnesses. The metaphor space is occupied; the discipline is not.

**Assayance** names the *discipline* rather than the act — the same move that made **Assurability** name the property rather than the relationship. `Assay` is already the verb for *determining genuineness by testing*; nothing else claimed the noun.

## Boundary — what this is not

- **Not a standard, and not a conformance claim.** Nothing here asserts compliance with any regulation, framework or specification.
- **Not first.** Every ingredient is public and old: falsifiability is Popper's; controls are the laboratory's; deliberate breakage is mutation testing's; instrument verification is metrology's; default-deny is policy-as-code's. What is named here is their **convergence into one discipline applied to assurance claims themselves**, plus five operational rules that make that convergence checkable.
- **Not a claim of novelty over any single idea.** Three independent projects appeared in the wild during this work (`falsify-ml`, `mutiny`'s "falsification gate", and the agent-testing harnesses above) using parts of the same intuition. The timing is convergent, which means the idea is in the air — it does **not** mean the term or the method is ours to claim exclusively.
- **No results promised.** No defect-escape rate, no cost saving, no pass rate. The method's only product is a stronger kind of *no*.

## T0 · The precursor: prior art before invention

Before building the instrument, check whether the instrument exists. One afternoon's work produced fourteen defects — **not one of them discovered by searching; every one discovered by getting it wrong.** They sat in domains with mature solutions: mutation testing, linter rule-testing protocols, fail-closed policy engines, generated-artifact drift detection, reproducible builds.

Three retrieval recipes, each measured rather than reasoned:

| | Recipe | The measurement behind it |
|---|---|---|
| **R1** | Write the query **like a repository name** — two or three words, not a sentence. | `gh search repos` matches name, description and topics. It does **not** index READMEs. Thirteen of fourteen long-phrase queries returned zero; the same questions in short form hit 4/4. A zero that means "my query was bad" is not evidence that nobody has done it. |
| **R2** | Sort by stars, then **read the last-commit date anyway.** | Sorting by stars surfaced 262k- and 214k-star aggregator repositories at the top of a search for coding agents — neither of which is a coding agent. A popularity proxy is not an identity judgment (T5). A 49k-star tool that has not committed in four months is a relic, not an option. |
| **R3** | Use a **ladder** of queries and record which rung hit. | A ladder that accepts the *first non-empty* result selected a one-star, three-year-stale script and filed it under "existing solutions". That is worse than a blank: a blank tells you to look; a stale one-star entry tells you you already did. |

**Rule derived:** the acceptance criterion is itself under test. Ask of any threshold you are about to call "pass": *would this also pass when nothing was satisfied?* Both defects found in the scanner were of this family — a wrong JSON field name that made every query fail loudly (which is why it was caught), and a credibility threshold set at "non-empty" (which is why it was not).

## The five tests

Run all five against any assurance artifact — a gate, a test, a policy, an evidence file, a document, a claim.

### T1 · The negative control（反照）

> **Every negative conclusion needs a positive control.**
> A check that has never been observed failing has not been shown to be capable of failing.

**How to run it.** Break the thing the check is supposed to catch, then run the check. It must fail. Restore, then run again: it must pass. Do this for every rule, every time the rule changes.

**What failure looks like.** A gate with no negative control is indistinguishable from `exit 0`. It will be green in every CI run, including the runs where the defect shipped.

**Recorded instance.** Seven end-to-end controls were written against the release-feed generator. The first version asserted exit codes only — and the harness used `cmd | tail; echo $?`, so `$?` was *tail's* exit code. **Every control printed the correct failure and returned 0.** If this had been CI, all seven would have passed while proving nothing. Only capturing the exit code without a pipe exposed it. The generator also found, in the same session, that its own content fingerprint covered the entries but not the site fields — so editing the headline or the base URL changed every published page **without moving the digest**, and the clock check let it through. A fingerprint over "the content" is worthless if "the content" is not defined.

### T2 · Absence must reach the exit code（落码）

> If *the thing that should be there is not there* is recorded as a log line, a neutral marker, or a skip, it will never produce a non-zero exit — and the gate is blind exactly where it matters most.

**How to run it.** For every required input, ask: if it were missing, what is the process exit code? If the answer is not "non-zero", the requirement is decorative.

**What failure looks like.** A summary counter that says `fail=0` while three required fields are empty, because "missing" was tracked in a fourth bucket that the exit code never reads.

**Recorded instance.** A linter rule pointed at a file that did not exist returned success — *the target was absent, so there was nothing to complain about.* A validator read an unreadable file, printed the error, and continued. Both were fixed by making absence a counted failure with a non-zero exit. The general form: **a suppression or skip mechanism is a hole in the gate, and it must be counted and reported, not respected silently.**

### T3 · The criterion is itself under test（审据）

> Before treating a criterion as "pass", ask: *would it also pass when nothing was satisfied?*

**How to run it.** Take the weakest possible input that technically satisfies the rule. If it passes, the criterion is wrong, not the input.

**What failure looks like.** "Non-empty" as a quality bar; ">0 results" as coverage; "the file exists" as correctness; a severity label assigned at publication and never measured.

**Recorded instance.** A retrieval ladder accepted the first non-empty result and selected a ★1, three-year-stale script. A rule was shipped with a stated severity but no measurement of its false-positive rate. Both are the same defect: **an acceptance criterion that was never itself accepted.**

### T4 · A description is a claim（兑现）

> A comment, docstring, README or policy that asserts behaviour is a **claim about the world**. It must be tested or deleted. There is no third option.

**How to run it.** Grep your own documentation for necessity claims — *"without this it breaks"*, *"this guard prevents X"*, *"always runs before Y"*. Then break it and check.

**What failure looks like.** Three of ten recorded defects in one project were docstrings describing behaviour the code did not have. The fix is not to soften the wording; it is to make the sentence true or remove it.

**Recorded instance.** A comment asserted that a particular token in a regular expression was load-bearing — without it, the pattern would misclassify a URL as a foreign repository. The claim was plausible, well-reasoned, and **false**: both spellings passed every test case. It had been written from reasoning, never from measurement. The corrected rule in that repository now reads: *do not assert a necessity you have not measured.*

### T5 · A proxy is not an identity judgment（辨身）

> When a cheap metric stands in for a decision, it will eventually be mistaken for the decision.

**How to run it.** Name the metric. Name the decision it stands in for. Name the case where they disagree. If the metric wins by default, the proxy has become the judgment.

**What failure looks like.** Ranking by stars and reading the top result as "the answer"; counting issues as engagement; treating a green badge as evidence of correctness; reporting a correct artifact next to a wrong number.

**Recorded instance.** Ranked by stars, a search for coding agents returned aggregator repositories at 262k, 214k and 146k stars — the first two are link collections, not agents. Separately, a manifest generator wrote a correct file and **printed a wrong number**, because a loop variable shadowed the name it reported. The artifact was right; the report was wrong; the report is what gets read. **A value that is displayed anywhere needs its own route to verification.**

## Applying it in ten minutes

```text
1. List every assurance artifact you rely on.            (gates, tests, policies, badges, evidence files)
2. For each: break the thing it protects. Does it fail?  (T1 — if you have never seen it fail, that is the finding)
3. For each required input: what is the exit code if it is missing?   (T2)
4. For each threshold: does it pass when nothing is satisfied?        (T3)
5. Grep your docs for necessity claims. Break one.                    (T4)
6. Name one metric you report. Find a case where it disagrees with the decision it stands for. (T5)
```

Two corollaries that cost the most to learn:

> **A passing run and a correct report are two different things.**

> **Missing must be loud.** Silence is the most expensive possible output, because it is indistinguishable from success.

## Falsifiability conditions

This method is a claim, so it must state what would refute it.

- **T1 is bounded if** a project can be shown catching the same classes of silent failure at the same rate *without* ever observing a control fail. That would make the control optional rather than constitutive.
- **The domain is narrower than claimed if** the dominant cost of failure in practice is crashes and non-zero exits rather than silent passes. This method addresses the second category and has nothing to say about the first.
- **The discipline degrades to advice if** the five tests cannot be mechanised — if applying them requires a human to notice, rather than a script to disagree. The published tooling exists to make that answer measurable rather than asserted.
- **The term is not defensible** if a prior use of `Assayance` as a technical term in assurance or verification is produced. Two candidate names were discarded during this work for exactly that reason; this one is offered on the same terms.

## Real-world referents (mapped, not invented)

| Domain | Referent | What maps |
|---|---|---|
| Metrology | instrument verification against reference standards | You verify the **instrument**, not the measurement — T1 |
| Laboratory science | positive and negative controls; placebo arm | The control is not optional — T1 |
| Toxicology | confirmatory second assay after a screening hit | Adjacent but distinct: they re-test the *sample*; this re-tests the *instrument* |
| Aviation | airworthiness demonstration by flight test | A system must be **shown to respond**, not shown to exist |
| Software | mutation testing, fault injection, canary deploys | T1 mechanised |
| CI/CD | required checks, branch protection, fail-closed defaults | T2 |
| Policy as code | default-deny evaluation | T2 |
| Accounting | reconciliation against an independent record | The number that is reported needs a second computation — T5 |

## Where the evidence lives

The method and the catalogue are deliberately separate, so that neither is a copy of the other:

| | |
|---|---|
| **This repository** | the **doctrine** — what the five tests are, why they hold, what would refute them |
| **[silent-failure-catalog](https://github.com/zhaoxinghua09-cell/silent-failure-catalog)** | the **catalogue** — fourteen documented silent failure modes, each with a reproduction and a self-check, plus runnable detectors |

Twelve defects are recorded there with the control that found each one: ten in the catalogue's own tooling, two in the release-feed generator. Two further defects were found by a prior-art scanner before it produced any usable output — one made it fail loudly, the other passed quietly on a stale one-star result.

## Position in the stack

| | |
|---|---|
| **Theory ID** | TH-META-014 |
| **Domain code** | META (cross-domain, meta-layer) |
| **Parent** | TH-META-006 LGD 全程治理论 — *有籍 · 有证 · 有门禁* |
| **Relation to the three laws** | Assayance governs the **validity of the instruments** that LGD's three laws are enforced with. 有门禁 (LGD-III) asks *is there a gate*; Assayance asks *is the gate a gate*. |
| **Companion angles** | Terminance · Mnemoship · Culpachain · Runtigil · Assurability |
| **Collision verdict** | Descriptive lane 🔴 (Popper · laboratory control · mutation testing · metrology) → Greek test-vocabulary 🔴 (four terms, all taken by agent-testing tooling in 2025–26) → **coined term 🟢** |

## Citation

If you use or cite this method, please reference:

> Zhao, S. (2026). *Assayance: Falsifiable Assurance — five tests for assurance that can fail*. SynomosAI.
> https://github.com/zhaoxinghua09-cell/assayance

## Theory stack

- **LGD — 凡自治之物 · 全程治理论 (Lifecycle Governance Doctrine)** — the parent framework: *有籍 · 有证 · 有门禁* across the full life of an autonomous thing.
- **Cross-domain angle matrix** — 5 angles × 13+ domains.
- Companion angles: Terminance · Mnemoship · Culpachain · Runtigil · Assurability.

## Author

**赵兴华 / Steven Zhao · China**
ORCID [0009-0001-0512-1237](https://orcid.org/0009-0001-0512-1237) · GitHub [@zhaoxinghua09-cell](https://github.com/zhaoxinghua09-cell)

Proposed and named 2026-09-19. Co-created with 老二 (Paredros), AI research partner.
Human authorship, judgment, and final responsibility rest with the author.

## License

Theory names and definitions — all rights reserved by the author. Any citation, use, or extension shall trace back to this source. The method described may be applied freely; attribution is requested.

---

## 中文要点

**一句话**：**没被看见失败过的检查，还不算检查。**

**它治的病**：门禁恒绿、测试不会红、策略默认放行、证据没人重算、文档写着代码里没有的防线——这些都**看起来像保障，实际产出为零**。

**为什么不叫"试金石"**：实测发现，希腊语里所有"检验"词——βάσανος（试金石）、δοκιμασία（资格审查）、ἔλεγχος（盘问）——**在 2025–26 这一波 AI agent 测试工具里已被逐个占满**，而且占的正是我们这个赛道。所以改用铸词 **Assayance（试真法）**：`assay` 本来就是"通过测试判定真伪"的意思，而这个名词没人占。**这个结论是测出来的，不是推出来的。**

**五条判据**：

| | 判据 | 要问的那句话 |
|---|---|---|
| **T1 反照** | 每个否定结论都要配阳性对照 | 把它要防的东西弄坏，它会不会红？从没红过的检查，无法证明它**能**红。 |
| **T2 落码** | 缺失必须进退出码 | 该有的东西没有时，退出码是多少？答不出"非零"的，就是装饰。 |
| **T3 审据** | 验收标准本身是被检对象 | 什么都不满足时，这条判据会不会**也**通过？ |
| **T4 兑现** | 描述即声明 | 注释/docstring 声称的行为，要么测它，要么删它，没有第三条路。 |
| **T5 辨身** | 代理指标不是身份判断 | 你用哪个便宜数字代替了决定？它和那个决定在什么情况下不一致？ |

**T0 前置步**：动手前先查有没有现成方案。三条检索配方（全为实测）：检索词要**像仓库名**、排序后**必须看最近提交时间**、**用检索词阶梯并记录是哪一条命中的**。

**两条代价最大的推论**：

> **跑通 ≠ 报对** —— 产物是对的、打印出来的数是错的，而**被读走的是那个数**。

> **缺失必须吵** —— 沉默是最贵的输出，因为它和成功长得一模一样。

**边界（别夸大）**：不是标准、不声称合规、**不声称首创**——这些零件全是公开的旧东西（波普尔的可证伪性、实验室对照、变异测试、计量学的器具检定、策略即代码的默认拒绝）。这里命名的，是它们**收敛成一套用来管"保障声明"本身的规矩**这件事。也不承诺任何效果。

**可证伪条件**（这也是它的一部分）：如果有人在从没观察过对照失败的情况下，能以同样比率抓住同类静默失败 → T1 的必要性受限；如果实践中主要代价是崩溃而非静默通过 → 适用范围比声称的窄；如果这五条无法机械化 → 它退化为建议。

**已发布的地图**｜**教义**在本仓（五条判据 + 为何成立 + 什么能证伪它）；**证据**在 [silent-failure-catalog](https://github.com/zhaoxinghua09-cell/silent-failure-catalog)（14 条静默失败模式 + 可运行检测器 + 12 条带对照记录的自抓缺陷）。
