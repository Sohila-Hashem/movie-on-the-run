from functools import lru_cache
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import  ContextTypes
from app.services.Movies.movies_service import MovieCategoryMap

@lru_cache()
def get_categories_keyboard():
    categories = MovieCategoryMap.get_supported_categories()
    keyboard = [
        [InlineKeyboardButton(category.replace('_', ' ').title(), callback_data=category)]
        for category in categories
    ]
    return InlineKeyboardMarkup(keyboard)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to Movies4U bot, What's your Movie choice for today 😀?",
        reply_markup=get_categories_keyboard()
    )

async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await update.callback_query.answer()

    message = update.effective_message
    await message.reply_text(
        "What's your Movie choice for today 😀?",
        reply_markup=get_categories_keyboard()
    )