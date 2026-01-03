import re


LITERAL_REGEX = re.compile(r"=\s*('[^']*'|\d+)")


def normalize_sql(sql: str) -> str:
    """
    Replace literal values with placeholders so similar queries
    map to the same normalized form.
    """
    return LITERAL_REGEX.sub("= ?", sql)
