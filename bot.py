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

from app.services.Movies.movies_service import MovieService, MovieCategoryMap
from app.services.Trailers.trailer_service import TrailerService

from app.services.Trailers.trailer_api_service import TrailerAPIServiceManager
from app.services.Movies.movie_api_service import MovieAPIServiceManager

from app.handlers.app_commands import menu_command, start_command
from app.handlers.movies_commands import MovieServiceHandlers
from app.handlers.messages import handle_messages

from app.utils.API_Client import APIClient
from telegram import Update

load_dotenv("config/.env")

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
        MovieService(
            MovieAPIServiceManager.get_instance(
                APIClient(
                    base_url="https://api.themoviedb.org/3/",
                    headers={"accept": "application/json"},
                    params={
                        "api_key": os.getenv("MOVIES_API_KEY"),
                        "language": "en-US",
                        "with_original_language": "en",
                        "include_adult": "false",
                        "include_video": "true",
                        "sort_by": "popularity.desc",
                        "vote_average.gte": 7,
                        "release_date.gte": "2011-01-01",
                    },
                )
            )
        ),
        TrailerService(
            TrailerAPIServiceManager.get_instance(
                APIClient(
                    base_url="https://api.themoviedb.org/3/",
                    headers={"accept": "application/json"},
                    params={
                        "api_key": os.getenv("MOVIES_API_KEY"),
                        "language": "en-US",
                    },
                )
            )
        ),
    )
    # Movies handlers
    for category in MovieCategoryMap.get_supported_categories():
        handler = movie_service_handlers.suggest_movie(category)
        app.add_handler(CommandHandler(category, handler))
        app.add_handler(CallbackQueryHandler(handler, pattern=re.escape(category)))

    # adding handlers for messages
    app.add_handler(MessageHandler(filters.TEXT, handle_messages))

    # adding error handler
    app.add_error_handler(error)

    return app


if __name__ == "__main__":
    bot_token = os.getenv("BOT_API_TOKEN")
    webhook_url = os.getenv("WEBHOOK_URL")

    app = build_app(bot_token)

    if os.getenv("ENV") == "production":
        # running the bot through a webhook technique
        app.run_webhook(
            listen="0.0.0.0",
            port=int(os.environ.get("PORT", 10000)),
            url_path="telegram",
            webhook_url=f"{webhook_url}/telegram",
        )
    else:
        # running the bot through a polling technique
        app.run_polling()
