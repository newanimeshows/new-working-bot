import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
from bot import Bot
from config import ADMINS, CHANNEL_IDS, DISABLE_CHANNEL_BUTTON
from helper_func import encode


@Bot.on_message(filters.private & filters.user(ADMINS) & ~filters.command(['start', 'users', 'broadcast', 'batch', 'genlink', 'stats']))
async def channel_post(client: Client, message: Message):
    reply_text = await message.reply_text("Please Wait...!", quote=True)

    post_messages = []
    for channel_id in CHANNEL_IDS:
        try:
            post_message = await message.copy(chat_id=channel_id, disable_notification=True)
            post_messages.append((channel_id, post_message))
        except FloodWait as e:
            await asyncio.sleep(e.x)
            post_message = await message.copy(chat_id=channel_id, disable_notification=True)
            post_messages.append((channel_id, post_message))
        except Exception as e:
            print(e)
            await reply_text.edit_text("Something went Wrong..!")
            return

    links = []
    for channel_id, post_message in post_messages:
        converted_id = post_message.id * abs(channel_id)
        string = f"get-{converted_id}"
        base64_string = await encode(string)
        link = f"https://t.me/{client.username}?start={base64_string}"
        links.append(link)

        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(
            "🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])

        if not DISABLE_CHANNEL_BUTTON:
            try:
                await post_message.edit_reply_markup(reply_markup)
            except Exception as e:
                print(e)
                pass

    if links:
        links_text = "\n\n".join(links)
        await reply_text.edit(f"<b>Here are your links</b>\n\n{links_text}", reply_markup=reply_markup, disable_web_page_preview=True)


@Bot.on_message(filters.channel & filters.incoming & filters.chat(CHANNEL_IDS))
async def new_post(client: Client, message: Message):

    if DISABLE_CHANNEL_BUTTON:
        return

    for channel_id in CHANNEL_IDS:
        if message.chat.id == channel_id:
            converted_id = message.id * abs(channel_id)
            string = f"get-{converted_id}"
            base64_string = await encode(string)
            link = f"https://t.me/{client.username}?start={base64_string}"
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(
                "🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
            try:
                await message.edit_reply_markup(reply_markup)
            except Exception as e:
                print(e)
                pass
            break
