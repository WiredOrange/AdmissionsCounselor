from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    discord_token: str
    discord_channel_id: int
    google_sheets_api_key: str
    google_sheet_id: str
    google_sheet_range: str = "Sheet1!A:C"
    post_timezone: str = "America/New_York"



def load_settings() -> Settings:
    load_dotenv()

    token = os.getenv("DISCORD_TOKEN", "")
    channel_id = os.getenv("DISCORD_CHANNEL_ID", "")
    sheets_api_key = os.getenv("GOOGLE_SHEETS_API_KEY", "")
    sheet_id = os.getenv("GOOGLE_SHEET_ID", "")
    sheet_range = os.getenv("GOOGLE_SHEET_RANGE", "Sheet1!A:C")
    timezone = os.getenv("POST_TIMEZONE", "America/New_York")

    missing = [
        key
        for key, value in {
            "DISCORD_TOKEN": token,
            "DISCORD_CHANNEL_ID": channel_id,
            "GOOGLE_SHEETS_API_KEY": sheets_api_key,
            "GOOGLE_SHEET_ID": sheet_id,
        }.items()
        if not value
    ]

    if missing:
        missing_keys = ", ".join(missing)
        raise ValueError(f"Missing required environment variables: {missing_keys}")

    return Settings(
        discord_token=token,
        discord_channel_id=int(channel_id),
        google_sheets_api_key=sheets_api_key,
        google_sheet_id=sheet_id,
        google_sheet_range=sheet_range,
        post_timezone=timezone,
    )
