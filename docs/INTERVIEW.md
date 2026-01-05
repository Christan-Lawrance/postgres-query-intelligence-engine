# Interview Preparation — Postgres Query Intelligence Engine

This document contains **concise, interview-ready answers** based entirely on the design and implementation of this project.

Each answer is structured to demonstrate **real production thinking**, not textbook knowledge.

---

## ❓ How did you avoid N+1 in GraphQL?

* I intentionally avoided field-level resolvers that trigger per-object database queries.
* All required data is fetched at the **root query level** using explicit batch queries.
* Results are grouped in memory and assembled into GraphQL types.
* This guarantees a **constant number of database queries**, regardless of result size.

**Key point:** GraphQL is treated as an orchestration layer, not a data-access layer.

---

## ❓ How do you prevent LLM hallucinations?

* The LLM is never trusted blindly.
* All LLM output must match a **strict Pydantic schema**.
* Any deviation (extra text, missing fields, invalid values) causes the output to be rejected.
* The system applies additional guardrails to confidence scores.
* LLM failures never affect core system functionality.

**Key point:** LLM output is treated like untrusted external input.

---

## ❓ How do you ensure database integrity?

* Foreign key constraints are used wherever data has ownership semantics.
* Derived tables use `ON DELETE CASCADE` to prevent orphaned records.
* All schema changes are applied via **manual Alembic migrations**.
* The database schema is treated as source code and reviewed intentionally.

**Key point:** Integrity is enforced at the database layer, not assumed in application code.

---

## ❓ What happens if PostgreSQL fails?

* Query instrumentation is non-blocking and failure-safe.
* If Postgres is unavailable, the application continues operating normally.
* Observability data is skipped, not retried aggressively.
* No user-facing functionality depends on observability writes.

**Key point:** Observability systems must never bring down production systems.

---

## ❓ What happens if the LLM fails?

* The LLM is strictly optional.
* Failures result in missing recommendations, not system errors.
* All LLM calls are wrapped in exception handling.
* The system continues collecting and analyzing performance data.

**Key point:** Intelligence is additive; reliability is mandatory.

---

## ❓ Why did you separate queries, executions, and analysis?

* Queries represent identity.
* Executions represent time-series events.
* Analysis represents interpretation.

This separation enables aggregation, historical analysis, and conditional reasoning without data duplication.

---

## ❓ Why is confidence different from severity?

* Severity answers: *How bad is this if true?*
* Confidence answers: *How sure are we that this is true?*

Severity is deterministic and system-owned.
Confidence is evidence-based and conservatively guarded.

---

## ❓ Why did you choose GraphQL over REST?

* The data is highly relational and exploratory.
* Clients need flexible access patterns without over-fetching.
* GraphQL allows a clean read-only observability API.

Batching ensures performance predictability.

---

## ❓ How is this different from a CRUD application?

* No user-driven writes.
* Heavy emphasis on instrumentation and derived data.
* Data is generated automatically by system behavior.
* The system reasons about behavior instead of storing user input.

This is closer to an internal platform or observability tool.

---

## ❓ How would you scale this system?

* Move analysis and LLM steps to async workers.
* Partition execution tables by time.
* Add retention policies for old executions.
* Cache GraphQL read paths.

The architecture already supports these changes.

---

## ❓ What was the hardest bug you faced?

* ORM relationship lazy-loading causing missing data in services.
* Fixed by explicitly fetching required entities in service logic.

This reinforced the principle of avoiding implicit ORM behavior.

---

## ❓ What does this project demonstrate about your engineering style?

* I design schemas before code.
* I think in failure modes.
* I don’t overtrust frameworks or AI.
* I value correctness and observability over shortcuts.

---

## 🧠 Closing Tip for Interviews

When discussing this project:

* Emphasize *why* decisions were made
* Discuss tradeoffs openly
* Frame it as an internal platform tool

This positions you as a senior backend engineer, not a framework user.
