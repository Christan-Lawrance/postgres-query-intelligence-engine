import sys
import os

# Add the root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from app.db.session import get_session
from app.models import QueryAnalysis
from app.services.recommendation_services import generate_recommendation


session = get_session()
analysis = session.query(QueryAnalysis).first()
session.close()

if analysis:
    generate_recommendation(analysis.id)
    print("sUCCESS")
