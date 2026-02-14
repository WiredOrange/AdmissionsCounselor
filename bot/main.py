from __future__ import annotations

import logging

import discord
from discord.ext import commands

from bot.config import Settings, load_settings


class AdmissionsCounselorBot(commands.Bot):
    def __init__(self, settings: Settings) -> None:
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(command_prefix="!", intents=intents)
        self.settings = settings

    async def setup_hook(self) -> None:
        await self.load_extension("bot.cogs.friday_posts")


def run() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    settings = load_settings()
    bot = AdmissionsCounselorBot(settings)
    bot.run(settings.discord_token)


if __name__ == "__main__":
    run()
