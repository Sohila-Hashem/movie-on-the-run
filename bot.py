import os
import re
import logging
from dotenv import load_dotenv
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    CallbackQueryHandler,
)

from app.services.Movies.movies_service import MovieCategory
from app.services.Movies.movies_api_service import MovieAPIService

from app.services.Trailers.trailers_api_service import TrailerAPIService

from app.handlers.app_commands import menu_command, start_command
from app.handlers.movies_commands import MovieServiceHandlers
from app.handlers.messages import handle_messages

from app.utils.API_Client import APIClient
from telegram import Update

load_dotenv()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# Error Handler
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.exception(
        'Unhandled exception while processing update "%s": %s', update, context.error
    )
    message = getattr(update, "effective_message", None) if update is not None else None
    if message is not None:
        await message.reply_text("Something went wrong. Please try again later!")


def build_app(bot_token: str):
    """Build and configure the Telegram bot application."""

    app = ApplicationBuilder().token(bot_token).build()

    # adding handlers for commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CallbackQueryHandler(menu_command, pattern="menu"))
    app.add_handler(CommandHandler("menu", menu_command))

    movie_service_handlers = MovieServiceHandlers(
        MovieAPIService(
            APIClient(
                base_url="https://api.themoviedb.org/3/",
                headers={"accept": "application/json"},
                params={
                    "api_key": os.getenv("MOVIES_API_KEY"),
                    "language": "en-US",
                    "with_original_language": "en",
                    "include_adult": "false",
                    "sort_by": "popularity.desc",
                    "vote_average.gte": 6,
                    "vote_count.gte": 50,
                    "primary_release_date.gte": "1998-01-01",
                },
            )
        ),
        TrailerAPIService(
            APIClient(
                base_url="https://api.themoviedb.org/3/",
                headers={"accept": "application/json"},
                params={
                    "api_key": os.getenv("MOVIES_API_KEY"),
                    "language": "en-US",
                },
            )
        ),
    )
    # Movies handlers
    for category in MovieCategory:
        handler = movie_service_handlers.suggest_movie(category)
        app.add_handler(CommandHandler(category.name.lower(), handler))
        app.add_handler(
            CallbackQueryHandler(handler, pattern=re.escape(category.name.lower()))
        )

    # adding handlers for messages
    app.add_handler(MessageHandler(filters.TEXT, handle_messages))

    # adding error handler
    app.add_error_handler(error)

    return app


if __name__ == "__main__":
    if os.getenv("ENV") == "production":
        webhook_url = os.getenv("WEBHOOK_URL")
        bot_token = os.getenv("BOT_TOKEN_PROD")
        app = build_app(bot_token)
        # running the bot through a webhook technique
        app.run_webhook(
            listen="0.0.0.0",
            port=int(os.environ.get("PORT", 10000)),
            url_path="telegram",
            webhook_url=f"{webhook_url}/telegram",
        )
    else:
        bot_token = os.getenv("BOT_TOKEN_DEV")
        app = build_app(bot_token)
        # running the bot through a polling technique
        app.run_polling()
