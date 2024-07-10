from aiohttp import web
from plugins import web_server
import pyromod.listen
from pyrogram import Client
from pyrogram.enums import ParseMode
import sys
from datetime import datetime
from config import API_HASH, APP_ID, LOGGER, TG_BOT_TOKEN, TG_BOT_WORKERS, FORCE_SUB_CHANNEL1, FORCE_SUB_CHANNEL2, CHANNEL_IDS, PORT
import pyrogram.utils

pyrogram.utils.MIN_CHANNEL_ID = -1009147483647


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

        if FORCE_SUB_CHANNEL1:
            try:
                link = (await self.get_chat(FORCE_SUB_CHANNEL1)).invite_link
                if not link:
                    await self.export_chat_invite_link(FORCE_SUB_CHANNEL1)
                    link = (await self.get_chat(FORCE_SUB_CHANNEL1)).invite_link
                self.invitelink = link
            except Exception as a:
                self.LOGGER(__name__).warning(a)
                self.LOGGER(__name__).warning(
                    "Bot can't Export Invite link from Force Sub Channel!")
                self.LOGGER(__name__).warning(
                    f"Please Double check the FORCE_SUB_CHANNEL_1 value and Make sure Bot is Admin in channel with Invite Users via Link Permission, Current Force Sub Channel Value: {FORCE_SUB_CHANNEL1}")
                self.LOGGER(__name__).info(
                    "\nBot Stopped. Join https://t.me/DarkHumorHub_Bot for support")
                sys.exit()
        if FORCE_SUB_CHANNEL2:
            try:
                link = (await self.get_chat(FORCE_SUB_CHANNEL2)).invite_link
                if not link:
                    await self.export_chat_invite_link(FORCE_SUB_CHANNEL2)
                    link = (await self.get_chat(FORCE_SUB_CHANNEL2)).invite_link
                self.invitelink2 = link
            except Exception as a:
                self.LOGGER(__name__).warning(a)
                self.LOGGER(__name__).warning(
                    "Bot can't Export Invite link from Force Sub Channel!")
                self.LOGGER(__name__).warning(
                    f"Please Double check the FORCE_SUB_CHANNEL_2 value and Make sure Bot is Admin in channel with Invite Users via Link Permission, Current Force Sub Channel Value: {FORCE_SUB_CHANNEL2}")
                self.LOGGER(__name__).info(
                    "\nBot Stopped. Join https://t.me/DarkHumorHub_Bot for support")
                sys.exit()

        for channel_id in CHANNEL_IDS:
            try:
                db_channel = await self.get_chat(channel_id)
                self.db_channel = db_channel
                test = await self.send_message(chat_id=db_channel.id, text="Test Message")
                await test.delete()
                self.LOGGER(__name__).info(
                    f"Successfully tested channel ID: {channel_id}")
            except Exception as e:
                self.LOGGER(__name__).warning(e)
                self.LOGGER(__name__).warning(
                    f"Make sure the bot is an admin in DB channel, and double-check the CHANNEL_ID value. Current value: {channel_id}")
                self.LOGGER(__name__).info(
                    "\nBot Stopped. Join https://t.me/DarkHumorHub_Bot for support")
                sys.exit()

        self.set_parse_mode(ParseMode.HTML)
        self.LOGGER(__name__).info(
            f"Bot Running..!\n\nCreated by \n@LeadModerator")
        self.LOGGER(__name__).info(f"""_▂▃▄▅▆▇█▓▒░ASV░▒▓█▇▆▅▄▃▂_""")
        self.username = usr_bot_me.username
        # web-response
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, PORT).start()

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped.")
