import sys
import os

# Add the root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from app.services.analysis_services import analyze_slow_queries


if __name__ == "__main__":
    analyze_slow_queries(limit=3)
