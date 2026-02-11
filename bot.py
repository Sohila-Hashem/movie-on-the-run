import os
from dotenv import load_dotenv
load_dotenv('config/.env')
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

from app.services.Movies.movies_service import MovieService, MovieCategoryMap
from app.services.Trailers.trailer_service import TrailerService

from app.services.Trailers.trailer_api_service import TrailerAPIServiceManager
from app.services.Movies.movie_api_service import MovieAPIServiceManager

from app.handlers.app_commands import menu_command, start_command
from app.handlers.movies_commands import MovieServiceHandlers
from app.handlers.messages import handle_messages

from app.utils.API_Client import APIClient


# Error Handler
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f'Update "{update}"\n caused error "{context.error}"')
    await update.message.reply_text("Something went wrong. Please try again later!")

# run app
if __name__ == '__main__':
    bot_token = os.getenv("BOT_API_TOKEN")

    app = ApplicationBuilder().token(bot_token).build()

    # adding handlers for commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('menu', menu_command))
    app.add_handler(CallbackQueryHandler(menu_command, pattern='^menu$'))

    movieServiceHandlers = MovieServiceHandlers(
        MovieService(MovieAPIServiceManager.get_instance(APIClient(
                    base_url='https://api.themoviedb.org/3/',
                    headers={
                        'accept': 'application/json'
                    },
                    params={
                        "api_key": os.getenv('MOVIES_API_kEY'),
                        'language': 'en-US',
                        'with_original_language': 'en',
                        "include_adult": "false",
                        "include_video": "true",
                        "sort_by": "popularity.desc",
                        "vote_average.gte": 7,
                        "release_date.gte":'2011-01-01'
                    }))),
        TrailerService(TrailerAPIServiceManager.get_instance(APIClient(
            base_url='https://api.themoviedb.org/3/', headers={
                'accept': 'application/json'
            }, params={
                "api_key": os.getenv('MOVIES_API_kEY'),
                'language': 'en-US'
            })))
    )
    # Movies handlers
    for category in MovieCategoryMap.get_supported_categories():
        handler = movieServiceHandlers.suggest_movie(category)
        app.add_handler(CommandHandler(category, handler))
        app.add_handler(CallbackQueryHandler(handler, pattern=f'^{category}$'))
    
    # adding handlers for messages
    app.add_handler(MessageHandler(filters.TEXT, handle_messages))

    # adding error handler
    app.add_error_handler(error)

    # running the bot through a polling technique
    print('Polling...')
    app.run_polling(poll_interval=3)