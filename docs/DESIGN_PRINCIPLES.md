# Design Principles

These principles are the immovable constraints of the **Postgres Query Intelligence Engine**.

They are not guidelines.
They are filters.

If a design choice violates even one of these, it does not belong in this system.

---

## 1. Make the Database’s Thinking Visible

PostgreSQL already makes intelligent decisions.
The problem is that those decisions are mostly *silent*.

This system exists to externalize that reasoning.

Every feature must help answer at least one of these questions:

* What decision did PostgreSQL make?
* Why did it make that decision?
* What trade-offs were involved?

If the system cannot explain *why* something happened, it should not attempt to judge it.

---

## 2. Prefer Deterministic Rules Over Probabilistic Guessing

Core intelligence in this system is rule-based.

* Sequential scan on large table
* Nested loop with high cardinality
* Mismatch between estimated and actual rows

These are not opinions. They are repeatable signals.

LLMs, heuristics, or fuzzy reasoning may **augment** explanations, but they never replace deterministic analysis.

The system must remain:

* Inspectable
* Testable
* Debatable

If a conclusion cannot be traced back to a concrete signal, it is invalid.

---

## 3. Optimize for Understanding, Not Just Performance

A faster query that no one understands is a future incident waiting to happen.

This system prioritizes:

* Clear explanations over clever optimizations
* Explicit trade-offs over one-sided recommendations
* Teaching the *why*, not just the *what*

Success is not measured by milliseconds saved.
It is measured by how confidently a human can reason about the query afterward.

---

## 4. Respect Context and Uncertainty

There is no universally “bad” query.

A query that is slow in one environment may be acceptable in another.

Therefore:

* Signals must be contextualized
* Confidence levels must be explicit
* Assumptions must be stated

The system should say:

> “This is likely inefficient *because…*”

—not—

> “This is wrong.”

---

## 5. Keep the Surface Area Small and Intentional

Every additional feature increases cognitive load.

This system prefers:

* Fewer concepts
* Clear boundaries
* Shallow abstractions

If a feature:

* Adds complexity without improving clarity
* Requires hidden state
* Exists mainly to look impressive

—it does not belong.

---

## Final Principle (Non-Negotiable)

> The system must earn trust through transparency.

No magic.
No silent automation.
No unexplained conclusions.

Only visible reasoning.
