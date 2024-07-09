from aiohttp import web
from plugins import web_server
from pyrogram import Client
from pyrogram.enums import ParseMode
import sys
import asyncio
from datetime import datetime, timedelta
from config import API_HASH, APP_ID, LOGGER, TG_BOT_TOKEN, TG_BOT_WORKERS, FORCE_SUB_CHANNEL1, FORCE_SUB_CHANNEL2, CHANNEL_ID, PORT


class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_hash=API_HASH,
            api_id=APP_ID,
            plugins={
                "root": "plugins"
            },
            workers=TG_BOT_WORKERS,
            bot_token=TG_BOT_TOKEN
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        self.uptime = datetime.now()

        try:
            db_channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = db_channel
            test = await self.send_message(chat_id=db_channel.id, text="Test Message")
            await test.delete()
        except Exception as e:
            self.LOGGER(__name__).warning(e)
            self.LOGGER(__name__).warning(
                f"Make Sure bot is Admin in DB Channel, and Double check the CHANNEL_ID Value, Current Value {CHANNEL_ID}")
            self.LOGGER(__name__).info(
                "\nBot Stopped. Ask at @DarkHumorHub_bot for support for support")
            sys.exit()

        self.set_parse_mode(ParseMode.HTML)
        self.LOGGER(__name__).info(
            f"Bot Running..!\n\nCreated by \n@LeadModerator")
        self.LOGGER(__name__).info(f"""▂▃▄▅▆▇█▓▒░ASV░▒▓█▇▆▅▄▃▂""")
        self.username = usr_bot_me.username

        # Start the web server
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, PORT).start()

        # Schedule the periodic check for force sub channels
        self.schedule_periodic_check()

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped.")

    def schedule_periodic_check(self):
        interval = timedelta(seconds=10)  # Adjust the interval as needed
        self.loop.create_task(self.periodic_check(interval))

    async def periodic_check(self, interval):
        while True:
            await self.check_force_sub_channel(FORCE_SUB_CHANNEL1, "invitelink")
            await self.check_force_sub_channel(FORCE_SUB_CHANNEL2, "invitelink2")
            await asyncio.sleep(interval.total_seconds())

    async def check_force_sub_channel(self, channel_id, attribute):
        if channel_id:
            try:
                chat = await self.get_chat(channel_id)
                invite_link = await self.export_chat_invite_link(channel_id)
                setattr(self, attribute, invite_link)
            except Exception as e:
                self.LOGGER(__name__).warning(e)
                self.LOGGER(__name__).warning(
                    "Bot can't Export Invite link from Force Sub Channel!")
                self.LOGGER(__name__).warning(
                    f"Please Double check the FORCE_SUB_CHANNEL value and Make sure Bot is Admin in channel with Invite Users via Link Permission, Current Force Sub Channel Value: {channel_id}")
                self.LOGGER(__name__).info(
                    "\nBot Stopped. Join https://t.me/DarkHumorHub_bot for support")
                sys.exit()

# Example usage in your main script:


async def main():
    bot = Bot()
    await bot.start()
    await bot.idle()

if __name__ == '__main__':
    asyncio.run(main())
