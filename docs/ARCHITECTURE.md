# Architecture Overview

This document describes the high-level architecture of the **Postgres Query Intelligence Engine**.

The goal of this architecture is not complexity or cleverness.
It is *clarity of responsibility*, *traceability of decisions*, and *ease of reasoning*.

---

## High-Level Flow

1. A user submits a SQL `SELECT` query for analysis.
2. The system validates and normalizes the query.
3. The query is classified to determine its dominant behavioral pattern.
4. An execution plan is generated (or accepted as input) and parsed.
5. The plan is converted into a structured internal representation.
6. Deterministic rules analyze the plan and query structure.
7. Inefficiency signals are detected and contextualized.
8. Findings are assembled into a structured analysis result.
9. A human-readable explanation is produced.
10. (Optional) An LLM augments the explanation for clarity and summarization.

At every stage, intermediate outputs are explicit and inspectable.

---

## Main Components

The system is composed of a small number of well-defined components.
Each component does one job and exposes clear inputs and outputs.

### 1. Query Intake & Normalization

**Purpose**
Establish a clean, predictable starting point for analysis.

**Responsibilities**

* Accept raw SQL input
* Perform basic validation
* Normalize formatting, aliases, and casing
* Reject unsupported query types early

This layer prevents downstream logic from compensating for malformed input.

---

### 2. Query Classifier

**Purpose**
Understand *what kind of work* the query is asking the database to do.

**Responsibilities**

* Analyze query structure
* Identify dominant patterns (joins, aggregates, filters)
* Provide descriptive classification metadata

This component does not judge performance.
It provides context for later stages.

---

### 3. Execution Plan Generator

**Purpose**
Obtain PostgreSQL’s view of how the query will be executed.

**Responsibilities**

* Generate `EXPLAIN` / `EXPLAIN ANALYZE` plans in controlled environments
* Accept pre-generated plans when execution is not possible
* Ensure plan output is complete and consistent

This component treats the database as the source of truth for execution intent.

---

### 4. Plan Parser

**Purpose**
Translate raw execution plans into structured, navigable data.

**Responsibilities**

* Parse plan output formats
* Build an internal plan tree representation
* Preserve hierarchy, costs, row estimates, and actuals

All downstream intelligence depends on this representation being correct.

---

### 5. Rule Engine (Core Intelligence)

**Purpose**
Detect inefficiencies using deterministic, explainable rules.

**Responsibilities**

* Evaluate plan nodes and query metadata
* Detect known inefficiency patterns
* Attach reasoning and evidence to each finding

This is the heart of the system.
Every rule must be traceable, testable, and explainable.

---

### 6. Context Evaluator

**Purpose**
Avoid absolute judgments by applying situational awareness.

**Responsibilities**

* Consider dataset size and growth patterns
* Adjust severity based on context
* Surface assumptions and uncertainty

This component ensures the system remains advisory, not authoritarian.

---

### 7. Explanation Builder

**Purpose**
Convert technical findings into human understanding.

**Responsibilities**

* Assemble structured analysis results
* Generate plain-English explanations
* Separate facts from interpretations

If this component fails, the system has failed its primary goal.

---

### 8. LLM Augmentation Layer (Optional)

**Purpose**
Improve accessibility without compromising correctness.

**Responsibilities**

* Rephrase explanations for clarity
* Summarize findings and trade-offs
* Never introduce new conclusions

This layer enhances communication, not intelligence.

---

### 9. API Layer

**Purpose**
Expose the system’s capabilities in a flexible, introspective way.

**Responsibilities**

* Accept analysis requests
* Orchestrate internal components
* Return structured and deterministic responses

The API layer contains no business logic.

---

## Responsibility Boundaries

Each component:

* Owns a single concern
* Has explicit inputs and outputs
* Can be tested in isolation

No component is allowed to:

* Mutate database state
* Make hidden decisions
* Depend on implicit global context

---

## Why GraphQL

GraphQL is chosen not for trendiness, but for alignment with the problem domain.

Query analysis is inherently exploratory: users may want classifications, plan details, detected issues, explanations, or summaries — often in different combinations. GraphQL allows clients to request *exactly* the depth and shape of analysis they need without over-fetching or rigid endpoint design.

More importantly, GraphQL’s strongly typed schema acts as living documentation for the system’s reasoning model. It forces clarity around what the system knows, what it infers, and what it explains. As the engine evolves, GraphQL enables additive growth without breaking existing consumers.

In short: GraphQL matches the system’s need for introspection, flexibility, and explicit structure.

---

## Architectural Summary

This architecture favors:

* Explicit data flow
* Deterministic reasoning
* Human-centered explanations

It avoids:

* Hidden magic
* Implicit coupling
* Premature optimization

The result is a system that can be understood end-to-end — by both machines and humans.

---
