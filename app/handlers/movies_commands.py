import random
import html
import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from app.utils.utils import get_movie_response
from app.services.Movies.movies_service import MovieCategoryMap, IMovieService
from app.services.Trailers.trailer_service import ITrailerService

logger = logging.getLogger(__name__)


class MovieServiceHandlers:
    def __init__(
        self, movie_service: IMovieService, trailer_service: ITrailerService
    ) -> None:
        self.movie_service = movie_service
        self.trailer_service = trailer_service

    def suggest_movie(self, category):
        async def suggest_movie_command(
            update: Update, context: ContextTypes.DEFAULT_TYPE
        ):
            query = update.callback_query
            message = update.effective_message
            if query:
                await query.answer()

            try:
                await message.reply_text(f"fetching a {category} Movie for you...🚀")
                category_id = MovieCategoryMap.get_category_id(category)

                category_total_pages = self.movie_service.get_page_count(category_id)

                random_page_num = random.randint(1, min(500, category_total_pages))

                rand_page_movies_list = self.movie_service.get_movies(
                    category_id, random_page_num
                )

                if rand_page_movies_list:
                    random_movie = self.movie_service.get_random_movie(
                        rand_page_movies_list
                    )

                    await message.reply_html(get_movie_response(random_movie))

                    movie_trailers = self.trailer_service.get_movie_trailers(
                        random_movie["id"]
                    )

                    if movie_trailers:
                        filtered_movie_trailers = self.trailer_service.filter_trailers(
                            movie_trailers, "YouTube"
                        )

                        if filtered_movie_trailers and len(filtered_movie_trailers):
                            await message.reply_text(
                                "see a list of official trailers below"
                            )
                            links_html = "\n".join(
                                f'<a href="https://www.youtube.com/watch?v={x["key"]}">{html.escape(x["name"])}</a>'
                                for x in filtered_movie_trailers
                            )
                            await message.reply_html(links_html)

                    keyboard = [
                        [
                            InlineKeyboardButton(
                                f"Next {category} Movie 🎬", callback_data=category
                            )
                        ],
                        [InlineKeyboardButton("Menu 🏠", callback_data="menu")],
                    ]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    await message.reply_text("What next?", reply_markup=reply_markup)
                    return

                await message.reply_text("No movies were found for this category")
            except Exception as e:
                logger.exception(
                    "something went wrong while executing suggest_movie_command: %s", e
                )
                if message:
                    await message.reply_text(
                        "Something went wrong. Please try again later :("
                    )

        return suggest_movie_command
