from telegram import Update
from telegram.ext import ContextTypes
from app.utils.utils import get_categories_keyboard


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the start command.

    Args:
        update (Update): The update object.
        context (ContextTypes.DEFAULT_TYPE): The context object.
    """
    await update.message.reply_text(
        "Welcome to 'Movie on the Run' bot, What's your Movie choice for today 😀?",
        reply_markup=get_categories_keyboard(),
    )


async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the menu command.

    Args:
        update (Update): The update object.
        context (ContextTypes.DEFAULT_TYPE): The context object.
    """
    if update.callback_query:
        await update.callback_query.answer()

    message = update.effective_message
    await message.reply_text(
        "What's your Movie choice for today 😀?", reply_markup=get_categories_keyboard()
    )
