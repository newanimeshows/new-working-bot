from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode
from bot import Bot
from config import OWNER_ID

# Set to track users who are expected to send a message to the owner
pending_users = set()

# /help command
@Bot.on_message(filters.command('help') & filters.private)
async def help_command(client: Client, message: Message):
    help_text = """
<b>✨ Here are the available commands:</b> ✨

- <b>/start</b> - Start the bot.
- <b>/help</b> - Show this help message.
- <b>/owner</b> - Get information about the bot owner.
- <b>/bots</b> - List other bots created by the owner.
- <b>/owner_msg</b> - Send a message to the bot owner.
    """
    await message.reply_text(
        help_text,
        parse_mode=ParseMode.HTML
    )

# /owner_msg command
@Bot.on_message(filters.command('owner_msg') & filters.private)
async def owner_msg_command(client: Client, message: Message):
    user_id = message.from_user.id
    user_mention = message.from_user.mention

    if user_id in pending_users:
        await message.reply_text(
            "📝 You have already initiated a message to the owner. Please send your message.",
            parse_mode=ParseMode.HTML
        )
    else:
        pending_users.add(user_id)
        await message.reply_text(
            f"👋 Hey {user_mention},\n\nPlease type and send the message you want to deliver to the owner.",
            parse_mode=ParseMode.HTML
        )

# Message handler to capture messages from users in pending_users
@Bot.on_message(filters.private & filters.text & ~filters.commands())
async def forward_to_owner(client: Client, message: Message):
    user_id = message.from_user.id
    if user_id in pending_users:
        user_mention = message.from_user.mention
        user_username = f"@{message.from_user.username}" if message.from_user.username else "No Username"

        # Forward the user's message to the owner
        forwarded_message = f"""
<b>📩 New Message from {user_mention}</b>
<b>🆔 User ID:</b> <code>{user_id}</code>
<b>👤 Username:</b> {user_username}

<b>📝 Message:</b>
{message.text}
        """
        try:
            await client.send_message(
                chat_id=OWNER_ID,
                text=forwarded_message,
                parse_mode=ParseMode.HTML
            )
            await message.reply_text(
                "✅ Your message has been successfully sent to the owner. Thank you!",
                parse_mode=ParseMode.HTML
            )
        except Exception as e:
            await message.reply_text(
                "❌ There was an error sending your message. Please try again later.",
                parse_mode=ParseMode.HTML
            )
            print(f"Error forwarding message to owner: {e}")
        finally:
            pending_users.remove(user_id)
    else:
        # If the user hasn't initiated /owner_msg, ignore or handle accordingly
        await message.reply_text(
            "⚠️ To send a message to the owner, please use the /owner_msg command first.",
            parse_mode=ParseMode.HTML
        )

# /owner command
@Bot.on_message(filters.command('owner') & filters.private)
async def owner_command(client: Client, message: Message):
    owner_info = """
<b>✨ Bot Owner:</b> ✨

👤 <b>Name:</b> [Owner Name]
📧 <b>Contact:</b> [Owner's Contact Info]

For more bots, type <b>/bots</b>.
    """
    await message.reply_text(
        owner_info,
        parse_mode=ParseMode.HTML
    )
