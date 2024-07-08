# Jishu Developer
# Don't Remove Credit 🥺
# Telegram Channel @Madflix_Bots
# Backup Channel @JishuBotz
# Developer @JishuDeveloper

import os
import asyncio
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
from bot import Bot
from config import ADMINS, FORCE_MSG, START_MSG, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, PROTECT_CONTENT
from helper_func import subscribed, encode, decode, get_messages
from database.database import add_user, del_user, full_userbase, present_user

# add time im seconds for waiting before delete
# 1 minute = 60, 2 minutes = 60×2=120, 5 minutes = 60×5=300
SECONDS = int(os.getenv("SECONDS", "60"))


@Bot.on_message(filters.command('start') & filters.private & subscribed)
async def start_command(client: Client, message: Message):
    id = message.from_user.id
    if not await present_user(id):
        try:
            await add_user(id)
        except:
            pass
    text = message.text
    if len(text) > 7:
        try:
            base64_string = text.split(" ", 1)[1]
        except:
            return
        string = await decode(base64_string)
        argument = string.split("-")
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
            except:
                return
            if start <= end:
                ids = range(start, end + 1)
            else:
                ids = []
                i = start
                while True:
                    ids.append(i)
                    i -= 1
                    if i < end:
                        break
        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except:
                return
        temp_msg = await message.reply("Please wait...")
        try:
            messages = await get_messages(client, ids)
        except:
            await message.reply_text("Something went wrong..!")
            return
        await temp_msg.delete()

        sent_messages = []  # Initialize the sent_messages list

        for msg in messages:
            if bool(CUSTOM_CAPTION) & bool(msg.document):
                caption = CUSTOM_CAPTION.format(
                    previouscaption="" if not msg.caption else msg.caption.html, filename=msg.document.file_name)
            else:
                caption = "" if not msg.caption else msg.caption.html

            if DISABLE_CHANNEL_BUTTON:
                reply_markup = msg.reply_markup
            else:
                reply_markup = None

            try:
                f = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                sent_messages.append(f)  # Add the sent message to the list

            except FloodWait as e:
                await asyncio.sleep(e.x)
                f = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                sent_messages.append(f)  # Add the sent message to the list

            except:
                pass

        # Inform the user about deletion and wait for SECONDS before deleting
        k = await client.send_message(chat_id=message.from_user.id, text="<b>❗️ <u>ᴜʀɢᴇɴᴛ</u> ❗️</b>\n\nʏᴏ, ʟɪsᴛᴇɴ ᴜᴘ! ᴛʜɪs ᴇᴘɪsᴏᴅᴇ / ꜰɪʟᴇ ɪs ᴏɴ ᴛʜᴇ ᴄʜᴏᴘᴘɪɴɢ ʙʟᴏᴄᴋ, sᴇᴛ ᴛᴏ ᴠᴀɴɪsʜ ɪɴ 10 ᴍɪɴᴜᴛᴇs (ᴛʜᴀɴᴋs ᴛᴏ ᴘᴇsᴋʏ ᴄᴏᴘʏʀɪɢʜᴛ ɪssᴜᴇs).\n\n📌 ʜᴜʀʀʏ ᴀɴᴅ sᴘʀᴇᴀᴅ ɪᴛ ᴛᴏ ᴀɴᴏᴛʜᴇʀ ᴘʟᴀᴄᴇ, sᴛᴀʀᴛ ᴛʜᴇ ᴅᴏᴡɴʟᴏᴀᴅ ᴀsᴀᴘ!", parse_mode=ParseMode.HTML)
        await asyncio.sleep(SECONDS)

        # Delete each file and update the user
        for msg in sent_messages:
            try:
                await msg.delete()
            except:
                pass

        await k.edit_text("Nᴀɴɪ???😨😧 \nMʏ ᴀɴɪᴍᴇ ᴄᴏʟʟᴇᴄᴛɪᴏɴ? ᴅᴜsᴛ! Dᴀᴛᴀ ɢʀᴇᴍʟɪɴs, ᴛʜɪs ɪs ᴀ sʜᴀʀɪɴɢᴀɴ-ʟᴇᴠᴇʟ ᴏꜰꜰᴇɴsᴇ! \n\nOɴᴇ ʀᴇϙᴜᴇsᴛ, ᴀɴᴅ ᴍʏ ʙᴀɴᴋᴀɪ ᴏꜰ ᴠᴇɴɢᴇᴀɴᴄᴇ ʀᴇsᴛᴏʀᴇs ᴡᴀɪꜰᴜs ᴀɴᴅ ʙᴀᴛᴛʟᴇs! Yᴏᴜ ᴡɪʟʟ ʀᴇɢʀᴇᴛ ᴛʜɪs!   🔥💪")

    else:
        if await subscribed(client, message):
            # Handle commands when user starts without a specific request
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "⚡️🇦​​​​​🇧​​​​​🇴​​​​​🇺​​​​​🇹​​​​​ 🇲​​​​​🇪​​​​⚡️​", callback_data="about"),
                        InlineKeyboardButton(
                            "❌ 🇨​​​​​🇱​​​​​🇴​​​​​🇸​​​​​🇪​​​​ ❌ ​", callback_data="close")
                    ]
                ]
            )
        await message.reply_text(
            text=START_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username=None if not message.from_user.username else '@' + message.from_user.username,
                mention=message.from_user.mention,
                id=message.from_user.id
            ),
            reply_markup=reply_markup,
            disable_web_page_preview=True,
            quote=True
        )
        return


# =====================================================================================##

WAIT_MSG = """"<b>Processing ...</b>"""

REPLY_ERROR = """<code>Use this command as a replay to any telegram message without any spaces.</code>"""

# =====================================================================================##


@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client, message: Message):
    buttons = [
        [
            InlineKeyboardButton(text="Join Channel", url=client.invitelink)
        ]
    ]
    try:
        buttons.append(
            [
                InlineKeyboardButton(
                    text='Try Again',
                    url=f"https://t.me/{client.username}?start={message.command[1]}"
                )
            ]
        )
    except IndexError:
        pass

    await message.reply(
        text=FORCE_MSG.format(
            first=message.from_user.first_name,
            last=message.from_user.last_name,
            username=None if not message.from_user.username else '@' + message.from_user.username,
            mention=message.from_user.mention,
            id=message.from_user.id
        ),
        reply_markup=InlineKeyboardMarkup(buttons),
        quote=True,
        disable_web_page_preview=True
    )


@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await full_userbase()
    await msg.edit(f"{len(users)} users are using this bot")


@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    if message.reply_to_message:
        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0

        pls_wait = await message.reply("<i>Broadcasting Message.. This will Take Some Time</i>")
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await del_user(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1

        status = f"""<b><u>Broadcast Completed</u></b>

<b>Total Users:</b> <code>{total}</code>
<b>Successful:</b> <code>{successful}</code>
<b>Blocked Users:</b> <code>{blocked}</code>
<b>Deleted Accounts:</b> <code>{deleted}</code>
<b>Unsuccessful:</b> <code>{unsuccessful}</code>"""

        return await pls_wait.edit(status)

    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()
