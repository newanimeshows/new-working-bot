from pyrogram import __version__
from bot import Bot
from config import OWNER_ID
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery


@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    if data == "about":
        await query.message.edit_text(
            text=f"<b>○ Creator : <a href='tg://user?id={OWNER_ID}'>🄰🄺🄳 ⚝ [ PRIME ]</a>\n○ Language : <code>Python 3</code>\n○ Anime Channel: <a href='https://t.me/Anime_keeda'>Anime Keeda</a>\n○ Movie Channel :<a href='https://t.me/MovieWalaX'>Movie-Wala-X</a>\n○ Source :<a href='https://t.me/Anime_keeda'>Click here</a></b>",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("ᴄʟᴏꜱᴇ", callback_data="close")
                    ]
                ]
            )
        )
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass
