# AdmissionsCounselor

Collegiate Racing League's Discord Bot.

## Current module: Friday Question Poster

This bot is structured in modules (Discord cogs) so you can add future features without rewriting core bot setup.

### What it does
- Every **Friday at 12:00 PM Eastern** (`America/New_York`), it checks your Google Sheet.
- It looks for a row whose date matches that Friday.
- It posts the matching question to your configured Discord channel.

Message format:

```text
Question #<number> (<mm/dd/yyyy>)
<question text>
```

## Google Sheet format

The configured range defaults to `Sheet1!A:C`, with header row in row 1:

| date       | number | question |
|------------|--------|----------|
| 2026-01-09 | 1      | ...      |

Accepted date formats in the `date` column:
- `YYYY-MM-DD`
- `MM/DD/YYYY`
- `MM/DD/YY`

## Setup

1. Create a Discord bot in the Developer Portal and copy its token.
2. Enable **Message Content Intent** for your bot.
3. Invite the bot to your server.
4. Create a Google Cloud project and enable the **Google Sheets API**.
5. Create an API key and allow it to access your sheet data.
6. Ensure your sheet is readable by that API key context (or publicly readable if using unrestricted key).

Copy `.env.example` to `.env` and fill values:

```bash
cp .env.example .env
```

Required environment variables:
- `DISCORD_TOKEN`
- `DISCORD_CHANNEL_ID`
- `GOOGLE_SHEETS_API_KEY`
- `GOOGLE_SHEET_ID`

Optional:
- `GOOGLE_SHEET_RANGE` (default: `Sheet1!A:C`)
- `POST_TIMEZONE` (default: `America/New_York`)

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m bot.main
```

## Commands

- `!postfriday` (admin only): manually tries to post the question for today's date.

## Extending the bot

Add new modules under `bot/cogs/` and load them in `bot/main.py` via `setup_hook`.
