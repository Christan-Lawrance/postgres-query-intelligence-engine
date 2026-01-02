# Architectural Decisions — Postgres Query Intelligence Engine

This document records **why** certain design choices were made. These decisions are intentional and reflect production-grade backend thinking rather than convenience or tutorials.

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
