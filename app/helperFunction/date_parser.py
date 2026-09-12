from datetime import datetime, date
from fastapi import HTTPException, Query, status


def parse_flexible_date(value: str | date) -> date:
    """
    Parses flexible date inputs:
    - date object
    - YYYY-MM-DD (e.g. 2026-09-07)
    - DD/MM/YYYY or D/M/YYYY (e.g. 7/09/2026, 07/09/2026)
    - DD-MM-YYYY or D-M-YYYY (e.g. 07-09-2026)
    - YYYY/MM/DD
    """
    if isinstance(value, date):
        return value

    if not isinstance(value, str):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid date type. Expected string or date object."
        )

    clean_str = value.strip()
    formats = [
        "%Y-%m-%d",    # ISO standard: 2026-09-07
        "%d/%m/%Y",    # UK/India format: 07/09/2026 or 7/09/2026
        "%d-%m-%Y",    # Dash format: 07-09-2026 or 7-9-2026
        "%Y/%m/%d",    # Slash ISO: 2026/09/07
        "%m/%d/%Y",    # US format fallback: 09/07/2026
    ]

    for fmt in formats:
        try:
            return datetime.strptime(clean_str, fmt).date()
        except ValueError:
            continue

    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=f"Invalid date format: '{value}'. Supported formats are YYYY-MM-DD, DD/MM/YYYY, or DD-MM-YYYY."
    )


def parse_date_query(
    attendance_date: str = Query(
        ...,
        description="Date in YYYY-MM-DD or DD/MM/YYYY format (e.g. 2026-09-07 or 7/09/2026)"
    )
) -> date:
    """FastAPI Query parameter dependency for flexible date parsing."""
    return parse_flexible_date(attendance_date)
