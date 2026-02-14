from __future__ import annotations

import logging
from datetime import date, datetime, time
from zoneinfo import ZoneInfo

import discord
from discord.ext import commands, tasks

from bot.services.sheets_client import SheetsClient

LOGGER = logging.getLogger(__name__)


class FridayPostsCog(commands.Cog):
    def __init__(
        self,
        bot: commands.Bot,
        sheets_client: SheetsClient,
        channel_id: int,
        timezone_name: str,
    ) -> None:
        self.bot = bot
        self.sheets_client = sheets_client
        self.channel_id = channel_id
        self.timezone = ZoneInfo(timezone_name)
        self._last_posted_date: date | None = None

        run_time = time(hour=12, minute=0, tzinfo=self.timezone)
        self.post_friday_question.change_interval(time=run_time)
        self.post_friday_question.start()

    def cog_unload(self) -> None:
        self.post_friday_question.cancel()

    @tasks.loop(hours=24)
    async def post_friday_question(self) -> None:
        now = datetime.now(tz=self.timezone)
        if now.weekday() != 4:
            return

        today = now.date()
        if self._last_posted_date == today:
            return

        await self._send_question_for_date(today)

    @post_friday_question.before_loop
    async def before_post_loop(self) -> None:
        await self.bot.wait_until_ready()

    @commands.command(name="postfriday")
    @commands.has_permissions(administrator=True)
    async def post_friday_now(self, ctx: commands.Context) -> None:
        """Manual override for admins."""
        today = datetime.now(tz=self.timezone).date()
        await self._send_question_for_date(today)
        await ctx.send("Tried posting today's Friday question.")

    async def _send_question_for_date(self, post_date: date) -> None:
        question = self.sheets_client.get_question_for_date(post_date)
        if question is None:
            LOGGER.warning("No question found for %s", post_date)
            return

        channel = self.bot.get_channel(self.channel_id)
        if channel is None:
            channel = await self.bot.fetch_channel(self.channel_id)

        if not isinstance(channel, discord.abc.Messageable):
            LOGGER.error("Configured channel %s is not messageable", self.channel_id)
            return

        message = f"**Question #{question.number} ({question.post_date:%m/%d/%Y})**\n{question.question}"
        await channel.send(message)
        self._last_posted_date = post_date
        LOGGER.info("Posted Friday question for %s", post_date)


async def setup(bot: commands.Bot) -> None:
    settings = bot.settings  # type: ignore[attr-defined]
    sheets_client = SheetsClient(
        api_key=settings.google_sheets_api_key,
        sheet_id=settings.google_sheet_id,
        value_range=settings.google_sheet_range,
    )
    await bot.add_cog(
        FridayPostsCog(
            bot=bot,
            sheets_client=sheets_client,
            channel_id=settings.discord_channel_id,
            timezone_name=settings.post_timezone,
        )
    )
