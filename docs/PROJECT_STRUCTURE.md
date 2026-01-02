## Project Folder Structure

```text
postgres-query-intelligence-engine/
│
├── app/
│   ├── __init__.py
│   │
│   ├── core/                 # Core infrastructure (boring but critical)
│   │   ├── config.py         # Settings, env vars
│   │   ├── database.py       # SQLAlchemy engine & session
│   │   └── logging.py        # Internal logging setup
│   │
│   ├── db/
│   │   ├── base.py           # Declarative Base
│   │   ├── session.py        # Session lifecycle helpers
│   │   └── migrations/       # Alembic (manual only)
│   │
│   ├── models/               # ORM models (pure data)
│   │   ├── __init__.py
│   │   ├── query.py          # Captured SQL queries
│   │   ├── execution.py      # Execution stats
│   │   ├── analysis.py       # Explain plans & analysis results
│   │   └── recommendation.py # LLM-generated insights
│   │
│   ├── instrumentation/      # SQLAlchemy hooks (the heart)
│   │   ├── __init__.py
│   │   ├── listeners.py      # before/after cursor execute
│   │   └── profiler.py       # timing, normalization
│   │
│   ├── analysis/             # Intelligence layer
│   │   ├── __init__.py
│   │   ├── slow_query.py     # thresholds & detection
│   │   ├── patterns.py       # N+1, repeated queries, scans
│   │   └── explain.py        # EXPLAIN ANALYZE runner
│   │
│   ├── llm/                  # LLM integration (optional but clean)
│   │   ├── __init__.py
│   │   ├── client.py         # OpenAI / Gemini wrapper
│   │   └── prompts.py        # Prompt templates
│   │
│   ├── graphql/              # API layer (read-only)
│   │   ├── __init__.py
│   │   ├── schema.py         # Root schema
│   │   ├── queries.py        # GraphQL queries
│   │   └── resolvers.py      # Resolver logic
│   │
│   └── services/             # Business coordination
│       ├── __init__.py
│       ├── query_service.py  # Query stats orchestration
│       └── analysis_service.py
│
├── docs/                     # Thinking before coding
│   ├── problem_statement.md
│   ├── architecture.md
│   └── decisions.md          # Why we chose X over Y
│
├── scripts/                  # One-off operational scripts
│   └── run_explain.py
│
├── tests/                    # Optional, but structure-ready
│   ├── __init__.py
│   └── test_analysis.py
│
├── alembic.ini
├── pyproject.toml / requirements.txt
├── README.md
└── .gitignore
