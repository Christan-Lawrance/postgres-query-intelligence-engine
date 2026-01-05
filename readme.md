# Postgres Query Intelligence Engine

A **backend-only, production-grade query observability and intelligence system** for PostgreSQL.

This project captures real SQL queries, analyzes their performance over time, explains execution plans, and generates **LLM-assisted performance recommendations** — all **without any frontend**.

This is **not a CRUD app**. It is an **internal platform / infra-style tool**.

---

## 🚀 What Problem This Solves

Modern applications suffer from:

* Slow queries discovered too late
* Lack of historical performance context
* Over-reliance on intuition instead of evidence
* Blind trust in AI-generated advice

This engine answers:

* *Which queries are slow?*
* *Are they consistently slow or just spikes?*
* *What is PostgreSQL actually doing internally?*
* *What should be optimized — and how confident are we?*

---

## 🧠 Core Capabilities

### 1️⃣ Query Instrumentation (Automatic)

* Hooks into **SQLAlchemy engine events**
* Captures:

  * Raw SQL
  * Execution time
  * Row counts
* Normalizes queries to track **query patterns**, not literals

### 2️⃣ Time-Series Performance Tracking

* Separates:

  * `queries` (identity)
  * `query_executions` (events)
* Enables aggregation, trend analysis, and historical comparison

### 3️⃣ Slow Query Analysis Engine

* Defines what "slow" means (policy-driven)
* Aggregates execution metrics
* Runs **EXPLAIN ANALYZE (FORMAT JSON)** safely
* Detects scan patterns (Seq Scan / Index Scan)

### 4️⃣ LLM Insight Engine (Optional, Safe)

* Uses an LLM **only after analysis**
* Produces:

  * Summary
  * Detailed explanation
  * Confidence score
* Output is:

  * Strictly validated with **Pydantic**
  * Guarded by system-level confidence checks
* LLM failures never break the system

### 5️⃣ Production-Grade GraphQL API

* Read-only observability API
* **No N+1 queries** (explicit batch loading)
* Explore:

  * Queries
  * Executions
  * Analyses
  * Recommendations

---

## 🧱 Tech Stack

* **Python 3.10+**
* **PostgreSQL**
* **SQLAlchemy** (ORM + instrumentation)
* **Alembic** (manual migrations only)
* **Strawberry GraphQL**
* **Pydantic** (LLM contract enforcement)
* **OpenAI API** (LLM insights)

No frontend. No frameworks hiding logic.

---

## 📂 Project Structure (Simplified)

```
app/
├── analysis/              # Slow query detection & EXPLAIN logic
├── db/                    # SQLAlchemy base, session, migrations
├── instrumentation/       # SQLAlchemy event listeners
├── graphql/               # Batched GraphQL API
├── llm/                   # LLM client, prompts, schemas
├── models/                # ORM models
├── services/              # Orchestration services
scripts/
├── test_instrumentation.py
├── run_analysis.py
├── run_llm.py
├── run_graphql.py
├── demo_run.py
```

---

## ▶️ How to Run (Local)

### 1️⃣ Prerequisites

* PostgreSQL running
* Database created
* Python virtual environment

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run migrations

```bash
alembic upgrade head
```

### 4️⃣ Run full pipeline demo

```bash
python scripts/demo_run.py
```

### 5️⃣ Start GraphQL API

```bash
python scripts/run_graphql.py
```

Open:

```
http://localhost:8000/graphql
```

---

## 🧪 Example GraphQL Query

```graphql
query {
  queries(limit: 5) {
    id
    normalizedSql
    totalExecutions
    analyses {
      executionTimeMs
      seqScanDetected
    }
    recommendations {
      severity
      confidenceScore
      summary
    }
  }
}
```

---

## 🔐 Design Principles (Why This Is Different)

* **Schema-first, code-second**
* **Manual Alembic migrations only**
* **No ORM magic in service logic**
* **No N+1 queries in GraphQL**
* **LLM output treated as untrusted input**
* **Confidence ≠ certainty**

Every layer is explicit, testable, and explainable.

---

## 🧠 What This Project Demonstrates

* Deep SQLAlchemy internals knowledge
* PostgreSQL execution plan understanding
* Safe LLM integration patterns
* Production GraphQL design
* Observability-first system thinking

This project is suitable for:

* Senior backend interviews
* Platform / infra roles
* AI + backend system discussions

---

## 🏁 Status

**Phase 8 complete. Project finished.**

Future extensions (optional):

* Confidence calibration via outcomes
* Recommendation deduplication strategies
* Async LLM workers
* Metrics export (Prometheus)

---

## 🧩 One-Line Summary

> A production-grade PostgreSQL query observability engine with safe, confidence-aware LLM insights — built the way internal platform tools are actually built.
