from telegram import Update
from telegram.ext import ContextTypes


# Message Handler
async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles the messages.

    Args:
        update (Update): The update object.
        context (ContextTypes.DEFAULT_TYPE): The context object.
    """
    bot_user = context.bot.get_me()
    bot_username = bot_user.username
    message_type: str = update.message.chat.type
    text: str = update.message.text

    if message_type == "group":
        if bot_username in text:
            text = text.replace(bot_username, "").strip()
            response: str = process_text(text)
        else:
            return

    else:
        response: str = process_text(text)

    await update.message.reply_text(response)


def process_text(text: str) -> str:
    """
    Replies to the text.

    Args:
        text (str): The text to reply to.

    Returns:
        str: The reply text.
    """
    processed_text = text.lower()

    if "hello" in processed_text:
        return "Hey there!"

    if "bye" in processed_text:
        return "Looking forward to see you again, Wish you a good day!"

    if "how are you" in processed_text:
        return "All good, thanks, and you?"

    return "I didn't get that. Can you please rephrase?"
