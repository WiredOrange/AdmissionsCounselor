from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

from googleapiclient.discovery import build


@dataclass(frozen=True)
class FridayQuestion:
    post_date: date
    number: str
    question: str


class SheetsClient:
    def __init__(self, api_key: str, sheet_id: str, value_range: str) -> None:
        self._service = build("sheets", "v4", developerKey=api_key)
        self._sheet_id = sheet_id
        self._value_range = value_range

    def get_question_for_date(self, target_date: date) -> Optional[FridayQuestion]:
        response = (
            self._service.spreadsheets()
            .values()
            .get(spreadsheetId=self._sheet_id, range=self._value_range)
            .execute()
        )

        rows = response.get("values", [])
        if len(rows) <= 1:
            return None

        for row in rows[1:]:
            if len(row) < 3:
                continue

            parsed_date = _parse_sheet_date(row[0])
            if parsed_date != target_date:
                continue

            return FridayQuestion(
                post_date=parsed_date,
                number=row[1].strip(),
                question=row[2].strip(),
            )

        return None


def _parse_sheet_date(raw_value: str) -> Optional[date]:
    value = raw_value.strip()

    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y"):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue

    return None
