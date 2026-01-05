# ""
# This code turns raw EXPLAIN data → LLM insight → validated recommendation, while making sure:
# the LLM never writes garbage
# confidence is never over-trusted
# failures never break the system
# """


from pydantic import ValidationError

from app.db.session import get_session
from app.models import QueryAnalysis, Recommendation, Query

from app.llm.llm import LLM
from app.llm.prompts import build_prompt
from app.llm.pydantic_schemas import LLMRecommendationSchema

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


CONFIDENCE_MIN = 0.1  # Below this, we discard the recommendation
CONFIDENCE_MAX = (
    0.95  # Above this, we cap the confidence to avoid over-trusting the LLM
)


def _validate_confidence(
    llm_confidence: float, seq_scan: bool, exec_time_ms: float | None
) -> float:
    """
    System-level confidence validation.

    The LLM is the primary authority.
    The system applies guardrails to prevent overconfidence
    when evidence is weak or incomplete.
    """
    confidence = llm_confidence

    # Hard clamp - never trust raw LLM confidence blindly
    confidence = max(0.0, min(confidence, 1.0))  # Clamp to [0.0, 1.0]

    # If no sequential scan
    if not seq_scan:
        confidence *= 0.8  # Reduce confidence by 20%

    # If execution time is missing or None
    if exec_time_ms is None or exec_time_ms < 200:
        confidence *= 0.8  # Reduce confidence by 20%

    # Cap maximum confidence / system-level ceiling
    confidence = max(CONFIDENCE_MIN, min(confidence, CONFIDENCE_MAX))

    return round(confidence, 2)


def generate_recommendation(analysis_id: int) -> None:
    """
    Generates and persists an LLM-based recommendation for a query analysis.

    This function is fail-safe:
    - Validation errors are expected and swallowed
    - System errors are isolated
    - No invalid data is ever written
    """

    session = get_session()

    try:
        # Fetch Analysis
        # analysis = session.query(QueryAnalysis).get(analysis_id)
        analysis = session.get(QueryAnalysis, analysis_id)  # SQLAlchemy 2.0 style
        if not analysis:
            return

        # Fetch Query
        query = session.get(Query, analysis.query_id)
        if not query:
            return

        # Build Prompt
        prompt = build_prompt(
            sql=query.raw_example_sql,
            plan_json=analysis.plan_json,
            seq_scan=analysis.seq_scan_detected,
            exec_time_ms=analysis.execution_time_ms,
        )
        # print(prompt)

        # Query LLM
        llm = LLM()
        raw_response = llm.execute(prompt)
        # print(f"Raw LLM Response: {raw_response}")

        # Validate LLM Response
        try:
            llm_validated_output = LLMRecommendationSchema.model_validate_json(
                raw_response
            )
        except ValidationError as e:
            logger.error(f"Validation error for LLM response: {raw_response}")
            logger.exception(e)
            # Expected failure: bad json, missing fields, wrong types
            session.rollback()
            return

        # System-level severrity logic
        severity = "high" if analysis.seq_scan_detected else "medium"

        # System-level confidence validation
        final_confidence = _validate_confidence(
            llm_confidence=llm_validated_output.confidence_score,
            seq_scan=analysis.seq_scan_detected,
            exec_time_ms=analysis.execution_time_ms,
        )

        # Persist Recommendation
        recommendation = Recommendation(
            query_id=analysis.query_id,
            severity=severity,
            summary=llm_validated_output.summary,
            details=llm_validated_output.details,
            confidence_score=final_confidence,
        )
        session.add(recommendation)
        session.commit()

    except Exception:
        session.rollback()
    finally:
        session.close()
