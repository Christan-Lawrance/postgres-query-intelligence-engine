# Non-Goals

This document exists to prevent scope creep, false expectations, and self-deception.

If a feature sounds impressive but violates the intent below, it does **not** belong in this project.

---

## What This System Is **Not** Trying to Be

* **Not an auto-optimizer**
  This system will not magically rewrite queries and guarantee performance gains. Databases are contextual; pretending otherwise is irresponsible.

* **Not a PostgreSQL replacement or extension**
  We do not compete with PostgreSQL’s planner, optimizer, or execution engine. We observe and interpret — we do not override.

* **Not a production traffic interceptor**
  Queries are analyzed intentionally, not silently intercepted from live systems.

* **Not an APM or observability platform**
  There is no continuous monitoring, alerting, dashboards, or time-series metrics.

* **Not a GUI-first tool**
  There will be no web UI, charts, or dashboards. Insight comes from analysis, not visuals.

---

## What This System Will Deliberately Avoid

* ❌ Executing queries on behalf of users
* ❌ Mutating schemas, indexes, or data
* ❌ Making production decisions automatically
* ❌ Chasing 100% accuracy or completeness
* ❌ Supporting every edge case in SQL syntax

If something cannot be explained clearly, it should not be automated.

---

## Philosophical Non-Goals

* **No illusion of certainty**
  Query performance is probabilistic and data-dependent. The system will surface confidence and doubt, not pretend omniscience.

* **No abstraction for abstraction’s sake**
  If a rule or layer does not improve understanding, it does not exist.

* **No teaching beginners**
  This is not a SQL tutorial. Users are expected to bring baseline competence.

---

## Final Line in the Sand

> This project values *understanding over automation* and *clarity over cleverness*.

Anything that violates this — no matter how tempting — is a non-goal.
