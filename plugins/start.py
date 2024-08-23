import os
import asyncio
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
from bot import Bot
from config import ADMINS, FORCE_MSG, START_MSG, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, PROTECT_CONTENT
from helper_func import subscribed, decode, get_messages
from database.database import add_user, present_user, del_user, full_userbase

# Add time in seconds for waiting before deleting
SECONDS = int(os.getenv("SECONDS", "600"))

@Bot.on_message(filters.command('start') & filters.private & subscribed)
async def start_command(client: Client, message: Message):
    user_id = message.from_user.id

    # Add user to database if not present
    if not await present_user(user_id):
        try:
            await add_user(user_id)
        except Exception as e:
            print(f"Error adding user: {e}")
            pass

    text = message.text

    if len(text) > 7:
        try:
            base64_string = text.split(" ", 1)[1]
            string = await decode(base64_string)
            argument = string.split("-")

            if len(argument) == 3:
                try:
                    start = int(int(argument[1]) / abs(client.db_channel.id))
                    end = int(int(argument[2]) / abs(client.db_channel.id))
                    ids = range(start, end + 1) if start <= end else []
                except Exception as e:
                    print(f"Error parsing argument: {e}")
                    return

            elif len(argument) == 2:
                try:
                    ids = [int(int(argument[1]) / abs(client.db_channel.id))]
                except Exception as e:
                    print(f"Error parsing argument: {e}")
                    return

            temp_msg = await message.reply("Wait A Second...")
            try:
                messages = await get_messages(client, ids)
            except Exception as e:
                await message.reply_text("Something went wrong..!")
                return
            await temp_msg.delete()
            
            snt_msgs = []
            
            for msg in messages:
                caption = CUSTOM_CAPTION.format(
                    previouscaption="" if not msg.caption else msg.caption.html,
                    filename=msg.document.file_name
                ) if bool(CUSTOM_CAPTION) and bool(msg.document) else "" if not msg.caption else msg.caption.html

                reply_markup = msg.reply_markup if not DISABLE_CHANNEL_BUTTON else None

                try:
                    snt_msg = await msg.copy(
                        chat_id=message.from_user.id,
                        caption=caption,
                        parse_mode=ParseMode.HTML,
                        reply_markup=reply_markup,
                        protect_content=PROTECT_CONTENT
                    )
                    await asyncio.sleep(0.5)
                    snt_msgs.append(snt_msg)
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    snt_msg = await msg.copy(
                        chat_id=message.from_user.id,
                        caption=caption,
                        parse_mode=ParseMode.HTML,
                        reply_markup=reply_markup,
                        protect_content=PROTECT_CONTENT
                    )
                    snt_msgs.append(snt_msg)
                except Exception as e:
                    print(f"Error copying message: {e}")
                    pass
            
            k = await message.reply_text(
                "<b>𝐀𝐭𝐭𝐞𝐧𝐭𝐢𝐨𝐧! 🚨</b>\n\n 🌸 𝐃𝐮𝐞 𝐓𝐨 𝘾𝙤𝙥𝙮𝙧𝙞𝙜𝙝𝙩 𝙄𝙨𝙨𝙪𝙚𝙨, 𝐅𝐢𝐥𝐞 𝐖𝐢𝐥𝐥 𝐁𝐞 𝐝𝐞𝐥𝐞𝐭𝐞𝐝 𝐢𝐧 10 𝐦𝐢𝐧𝐮𝐭𝐞𝐬!\n\n 🌸 𝙎𝗮𝘃𝗲 𝗧𝗵𝗲𝘀𝗲 𝗙𝗶𝗹𝗲𝘀 𝗜𝗻 𝗬𝗼𝘂𝗿 𝗦𝗮𝘃𝗲𝗱 𝗠𝗲𝘀𝘀𝗮𝗴𝗲𝘀! 📂\n\n  🌸 𝗠𝘂𝘀𝘁 𝗝𝗼𝗶𝗻 <a href='https://t.me/newanimeshow'>@𝙉𝙚𝙬_𝘼𝙣𝙞𝙢𝙚_𝙎𝙝𝙤𝙬𝙨 </a>𝗔𝗻𝗱 <a href='https://t.me/newanimeshowsgroup'>@𝘼𝙣𝙞𝙢𝙚_𝙂𝙧𝙤𝙪𝙥</a> 𝗧𝗼 𝗨𝘀𝗲 𝗠𝗲..! ✨",
                disable_web_page_preview=True
            )
            await asyncio.sleep(SECONDS)

            for snt_msg in snt_msgs:
                try:
                    await snt_msg.delete()
                    await k.edit_text("𝗧𝗛𝗘 𝗙𝗜𝗟𝗘𝗦 𝗛𝗔𝗦 𝗕𝗘𝗘𝗡 𝗗𝗘𝗟𝗘𝗧𝗘𝗗!!")
                except Exception as e:
                    print(f"Error deleting message: {e}")
                    pass
            return

        except Exception as e:
            print(f"Error in command processing: {e}")
            await message.reply_text("Something went wrong..!")
            return

    else:
        # Handle 'else' case
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("ᴀʙᴏᴜᴛ", callback_data="about"),
                    InlineKeyboardButton("ᴄʟᴏꜱᴇ", callback_data="close")
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
