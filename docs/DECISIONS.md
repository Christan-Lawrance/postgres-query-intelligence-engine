# Architectural Decisions — Postgres Query Intelligence Engine


This document captures **key design decisions** made while building the Postgres Query Intelligence Engine.

Each decision explains **why a certain approach was chosen and what tradeoffs were consciously accepted**.

These are not accidental outcomes — they are deliberate architectural choices.

---

## 1. Why `queries` and `query_executions` are separate

We intentionally separate **query identity** from **query execution events**.

* A single logical SQL query can execute thousands of times with different parameters.
* Storing every execution as a new query record would explode cardinality and make analysis noisy.
* By normalizing SQL (replacing literals with placeholders), we can treat similar queries as the same *query pattern*.
* This separation enables meaningful aggregation:

  * average execution time per query
  * slowest query patterns
  * frequency analysis
* This mirrors how real observability tools (APM, database monitors) model query behavior.

**Result:** cleaner data, better insights, and scalable analytics.

---

## 2. Why EXPLAIN ANALYZE output is stored as JSON

Postgres provides `EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)` specifically for machine consumption.

* Query plans are hierarchical and deeply nested; forcing them into relational tables is brittle.
* JSONB allows us to:

  * store the full plan losslessly
  * query specific fields later if needed
  * evolve analysis logic without schema migrations
* Different Postgres versions may add/remove plan fields — JSON absorbs this safely.
* Parsing everything upfront is unnecessary and premature optimization.

**Result:** future-proof storage with minimal schema churn.

---

## 3. Why recommendations are non-critical data

LLM-generated recommendations are **derived intelligence**, not source-of-truth data.

* The system must function correctly even if:

  * the LLM is unavailable
  * the API key is revoked
  * recommendations are deleted
* Treating recommendations as optional avoids coupling core logic to external services.
* This also allows:

  * re-generating insights later with improved prompts or models
  * comparing multiple recommendation versions

**Result:** system remains deterministic, stable, and testable.

---

## 4. Why Alembic migrations are written manually

Automatic migration generation hides critical decisions and often produces unsafe SQL.

* Manual migrations force deliberate thinking about:

  * backward compatibility
  * data backfills
  * index creation on large tables
* Production databases require control over:

  * locking behavior
  * rollout strategy
  * downgrade safety
* Writing migrations by hand builds long-term confidence with schema evolution.

**Result:** predictable deployments and fewer production surprises.

---

## 5. Why schema evolution is staged (core → analysis → intelligence)

The database schema is intentionally layered:

1. Core capture (`queries`, `query_executions`)
2. Analysis (`query_analysis`)
3. Intelligence (`recommendations`)

* This allows the system to deliver value early without waiting for all features.
* Each layer can evolve independently.
* Failures in higher layers never impact data capture.

**Result:** resilient architecture with clear responsibility boundaries.

---

## 6. Why this project is backend-only

This system is designed for engineers and automation, not end users.

* All value is exposed via structured APIs.
* Visualization is intentionally out of scope.
* This keeps the project focused on:

  * data modeling
  * performance
  * correctness

**Result:** deeper backend mastery without frontend distraction.

---


## 1️⃣ Why the LLM Is Optional

The LLM is treated as an **augmentation layer**, not a core dependency.

### Decision

* The system must function fully **without** the LLM.
* Query capture, analysis, and metrics collection never depend on AI output.

### Rationale

* LLM availability is not guaranteed (rate limits, outages, cost)
* Observability systems must never block on external services
* Performance analysis must remain deterministic

### Tradeoff

* Without the LLM, explanations are less human-friendly
* With the LLM, insight quality improves, but correctness never depends on it

This ensures the system is **robust first, intelligent second**.

---

## 2️⃣ Why Recommendations Are Non-Blocking

Recommendations are **advisory artifacts**, not execution-critical data.

### Decision

* Failure to generate a recommendation must never:

  * break ingestion
  * block analysis
  * corrupt data

### Rationale

* Recommendations are derived, not primary data
* Blocking on recommendations would couple core observability to interpretation
* In production, partial insight is better than system failure

### Tradeoff

* Some slow queries may temporarily lack recommendations
* System reliability is preserved under all failure modes

This mirrors how real observability and APM systems behave.

---

## 3️⃣ Why Confidence ≠ Certainty

Confidence represents **evidence strength**, not correctness.

### Decision

* Confidence is stored as a numeric score
* It reflects how strongly the data supports a recommendation
* It does **not** claim guaranteed improvement

### Rationale

* Database performance is context-dependent
* The same optimization can help or hurt depending on workload
* Overstating certainty leads to dangerous automation

### Tradeoff

* Requires users to exercise judgment
* Avoids false authority from AI-generated advice

The system is explicit about uncertainty instead of hiding it.

---

## 4️⃣ Why Severity Is System-Owned

Severity indicates **impact**, not interpretation.

### Decision

* Severity is derived deterministically from observed signals
* The LLM is not allowed to decide severity

### Rationale

* Severity must be consistent across time and queries
* LLMs are probabilistic and context-sensitive
* Mixing interpretation with policy leads to drift

### Tradeoff

* Severity logic may be simpler than an LLM could express
* Guarantees predictable behavior and comparability

Severity answers: *How bad is this if true?*
Confidence answers: *How sure are we that this is true?*

Keeping them separate preserves clarity.

---

## 🧠 Closing Principle

> The system owns truth.
> The LLM offers perspective.

Every decision reinforces that boundary.

This is how AI is safely integrated into production systems.
