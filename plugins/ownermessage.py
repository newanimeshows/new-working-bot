import os
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.enums import ParseMode
from bot import Bot
from config import OWNER_ID  # Ensure that OWNER_ID is defined in your config.py

# /help command
@Bot.on_message(filters.command('help') & filters.private)
async def help_command(client: Client, message: Message):
    help_text = """
✨ Here are the available commands: ✨

- /start - Start the bot.
- /help - Show this help message.
- /owner - Get information about the bot owner.
- /bots - List other bots created by the owner.
    """
    await message.reply_text(
        help_text,
        parse_mode=ParseMode.MARKDOWN
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
        parse_mode=ParseMode.MARKDOWN
    )

# Callback query handler for the "Continue" button
@Bot.on_callback_query(filters.regex("continue"))
async def continue_callback(client: Client, callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        "Please send me the message you'd like to send to the owner."
    )

    # Create a handler to capture the next message
    @Bot.on_message(filters.private & filters.text & ~filters.command)
    async def capture_message(client: Client, message: Message):
        if message.reply_to_message and message.reply_to_message.text == "Please send me the message you'd like to send to the owner.":
            # Forward the user's message to the owner
            await client.send_message(
                chat_id=OWNER_ID,
                text=f"📩 Message from {message.from_user.mention}:**\n\n{message.text}",
                parse_mode=ParseMode.MARKDOWN
            )
            await message.reply("Your message has been sent to the owner. Thank you!")

            # Remove the capture_message handler after it has been used
            Bot.remove_handler(capture_message, group=0)

# /owner command
@Bot.on_message(filters.command('owner') & filters.private)
async def owner_command(client: Client, message: Message):
    owner_info = """
✨ **Bot Owner: ✨

👤 Name: [Owner Name]
📧 Contact: [Owner's Contact Info]

For more bots, type /bots.
    """
    await message.reply_text(
        owner_info,
        parse_mode=ParseMode.MARKDOWN
    )
