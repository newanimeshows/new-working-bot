import os
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.enums import ParseMode
from bot import Bot
from config import OWNER_ID  # Ensure OWNER_ID is defined in your config.py

# /help command
@Bot.on_message(filters.command('help') & filters.private)
async def help_command(client: Client, message: Message):
    help_text = """
<b>✨ Here are the available commands:</b> ✨

- <b>/start</b> - Start the bot.
- <b>/help</b> - Show this help message.
- <b>/owner</b> - Get info about the bot owner.
- <b>/bots</b> - List other bots created by the owner.
- <b>/owner_msg</b> - Get in touch with the bot owner.
    """
    await message.reply_text(
        help_text,
        parse_mode=ParseMode.HTML
    )

# /owner_msg command
@Bot.on_message(filters.command('owner_msg') & filters.private)
async def owner_msg_command(client: Client, message: Message):
    user_mention = message.from_user.mention

    await message.reply_text(
        f"👋 Hey {user_mention},\n\nClick the button below and send your message to the owner.",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("✨ Continue ✨", callback_data="continue")]]
        ),
        parse_mode=ParseMode.HTML
    )

# Callback query handler for the "Continue" button
@Bot.on_callback_query(filters.regex("continue"))
async def continue_callback(client: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    
    # Send a message with a link to the owner's Telegram account
    await callback_query.message.edit_text(
        "Click the button below to send your message directly to the owner:",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Send Message", url=f"tg://resolve?domain=1196934318")]]
        ),
        parse_mode=ParseMode.HTML
    )

    # Inform the user that they can also send a message directly
    await callback_query.message.reply_text(
        "Alternatively, you can type your message here, and I will forward it to the owner.",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("✨ Continue ✨", callback_data=f"continue_{user_id}")]]
        ),
        parse_mode=ParseMode.HTML
    )

# Callback query handler for capturing user messages
@Bot.on_callback_query(filters.regex("continue_"))
async def continue_capture_message_callback(client: Client, callback_query: CallbackQuery):
    user_id = int(callback_query.data.split("_")[1])
    
    # Check if the callback is for the user who clicked "Continue"
    if callback_query.from_user.id == user_id:
        await callback_query.message.edit_text(
            "Please send me the message you'd like to send to the owner.",
            parse_mode=ParseMode.HTML
        )

        # Capture the next message from the user
        @Bot.on_message(filters.private & filters.text & ~filters.command)
        async def capture_message(client: Client, message: Message):
            # Forward the user's message to the owner
            await client.send_message(
                chat_id=OWNER_ID,
                text=f"<b>📩 Message from {message.from_user.mention}:</b>\n\n{message.text}",
                parse_mode=ParseMode.HTML
            )
            await message.reply("✅ Your message has been sent to the owner. Thank you!", parse_mode=ParseMode.HTML)

            # Remove the capture_message handler after it has been used
            Bot.remove_handler(capture_message, group=0)
    else:
        await callback_query.answer("This action is not authorized.", show_alert=True)

# /owner command
@Bot.on_message(filters.command('owner') & filters.private)
async def owner_command(client: Client, message: Message):
    owner_info = """
<b>✨ Bot Owner:</b> ✨

👤 <b>Name:</b> Ayan
📧 <b>Contact:</b> <a href='tg://user?id=1196934318'>@Ayan</a>

For more bots, type <b>/bots</b>.
    """
    await message.reply_text(
        owner_info,
        parse_mode=ParseMode.HTML
    )
