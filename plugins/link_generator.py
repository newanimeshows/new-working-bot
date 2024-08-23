from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot import Bot
from config import ADMINS
from helper_func import encode, get_message_id

# Helper function to ask for a message and validate it
async def ask_for_message(client: Client, user_id: int, prompt: str) -> Message:
    while True:
        try:
            message = await client.ask(
                text=prompt,
                chat_id=user_id,
                filters=(filters.forwarded | (filters.text & ~filters.forwarded)),
                timeout=60
            )
            msg_id = await get_message_id(client, message)
            if msg_id:
                return message, msg_id
            else:
                await message.reply("❌ Error\n\nThis Forwarded Post is not from my DB Channel or this Link is taken from DB Channel", quote=True)
        except Exception as e:
            print(f"Error while asking for message: {e}")
            return None, None

######## ---------------            BATCH COMMAND            ---------------########
@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('batch'))
async def batch(client: Client, message: Message):
    first_message, f_msg_id = await ask_for_message(client, message.from_user.id, "Forward the First Message from DB Channel (With Quotes)..\n\nOr Send the DB Channel Post Link")
    if not first_message:
        return

    second_message, s_msg_id = await ask_for_message(client, message.from_user.id, "Forward the Last Message from DB Channel (with Quotes)..\n\nOr Send the DB Channel Post Link")
    if not second_message:
        return

    # Generate batch link
    string = f"get-{f_msg_id * abs(client.db_channel.id)}-{s_msg_id * abs(client.db_channel.id)}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"

    # Generate reply markup with a share URL button
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]
    ])

    # Reply with the batch link and share URL button
    await second_message.reply_text(f"<b>Here is your link</b>\n\n{link}", quote=True, reply_markup=reply_markup)

######## ---------------            GEN LINK FOR 1 POST COMMAND            ---------------########
@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('genlink'))
async def link_generator(client: Client, message: Message):
    channel_message, msg_id = await ask_for_message(client, message.from_user.id, "Forward Message from the DB Channel (with Quotes)..\n\nOr Send the DB Channel Post Link")
    if not channel_message:
        return

    # Generate single message link
    base64_string = await encode(f"get-{msg_id * abs(client.db_channel.id)}")
    link = f"https://t.me/{client.username}?start={base64_string}"

    # Generate reply markup with a share URL button
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]
    ])

    # Reply with the single message link and share URL button
    await channel_message.reply_text(f"<b>Here is your link</b>\n\n{link}", quote=True, reply_markup=reply_markup)

######## ---------------            CUSTOM BATCH COMMAND FOR DIFFERENT FILES IN 1 LINK            ---------------########
@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('custom_batch'))
async def custom_batch(client: Client, message: Message):
    selected_message_ids = []

    # Ask for messages
    while True:
        try:
            channel_message = await client.ask(
                text="Forward a message from the DB Channel (with Quotes) or send the DB Channel post link. Send 'done' when finished.",
                chat_id=message.from_user.id,
                filters=(filters.forwarded | (filters.text & ~filters.forwarded) | filters.text),
                timeout=300
            )

            # Check if the message is the 'done' command
            if channel_message.text and channel_message.text.lower() == 'done':
                break

            # Get the message ID
            msg_id = await get_message_id(client, channel_message)
            if msg_id:
                selected_message_ids.append(msg_id)
                await channel_message.reply("✅ Message added to the batch.", quote=True)
            else:
                await channel_message.reply("❌ Error\n\nThis forwarded post is not from my DB Channel or this link is not taken from DB Channel", quote=True)
        except Exception as e:
            print(f"Error adding message to custom batch: {e}")
            return

    if not selected_message_ids:
        await message.reply("❌ No messages were added to the batch.", quote=True)
        return

    # Generate the custom batch link
    string = f"get-{'-'.join([str(msg_id * abs(client.db_channel.id)) for msg_id in selected_message_ids])}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"

    # Generate reply markup with a share URL button
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]
    ])

    # Reply with the custom batch link and share URL button
    await message.reply_text(f"<b>Here is your custom batch link</b>\n\n{link}", quote=True, reply_markup=reply_markup)

######## ---------------            UPDATE COMMAND FOR CHANGING THE OLD FILE            ---------------########
@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('update'))
async def update_post(client: Client, message: Message):
    while True:
        try:
            msg = await client.ask(
                text="Forward the message you want to update from the DB Channel or send the post link.",
                chat_id=message.from_user.id,
                filters=(filters.forwarded | (filters.text & ~filters.forwarded)),
                timeout=60
            )
        except Exception as e:
            print(f"Error asking for message to update: {e}")
            return

        msg_id = await get_message_id(client, msg)
        if msg_id:
            new_content = await client.ask(
                text="Send the new content for this post.",
                chat_id=message.from_user.id,
                filters=filters.text,
                timeout=60
            )
            await client.db_channel.edit_message_text(msg_id, new_content.text)
            await message.reply("✅ Post updated successfully.", quote=True)
            break
        else:
            await msg.reply("❌ Error\n\nThis post is not from the DB Channel or the link is invalid.", quote=True)
