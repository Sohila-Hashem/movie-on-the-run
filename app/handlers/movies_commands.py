import html
import logging
from typing import Callable
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
)
from telegram.ext import ContextTypes

from app.utils.utils import get_movie_response, convert_snake_case_str_to_title
from app.services.Movies.movies_service import MovieCategory
from app.services.Movies.movies_api_service import IMovieAPIService
from app.services.Trailers.trailers_api_service import ITrailerAPIService

logger = logging.getLogger(__name__)


class MovieServiceHandlers:
    def __init__(
        self, movies_api: IMovieAPIService, trailer_api: ITrailerAPIService
    ) -> None:
        if not movies_api or not trailer_api:
            raise ValueError("movies_api and trailer_api are required")
        self.movies_api = movies_api
        self.trailer_api = trailer_api

    def suggest_movie(self, category: MovieCategory) -> Callable:
        """
        Suggests a movie from the given category.

        Args:
            category (MovieCategory): The category of the movie.

        Returns:
            Callable: The suggest movie command.
        """
        if category not in MovieCategory:
            raise ValueError(f"Unsupported category: {category}")

        async def suggest_movie_command(
            update: Update, context: ContextTypes.DEFAULT_TYPE
        ):
            """
            Suggests a movie from the given category.

            Args:
                update (Update): The update object.
                context (ContextTypes.DEFAULT_TYPE): The context object.

            Returns:
                None
            """
            query = update.callback_query
            message = update.effective_message
            category_id = category.value
            category_name = convert_snake_case_str_to_title(
                snake_case_str=category.name
            ).capitalize()

            if query:
                await query.answer()

            try:
                await message.reply_text(
                    f"fetching a {category_name} Movie for you...🚀"
                )

                random_movie = self.movies_api.get_random_movie(category_id=category_id)
                movie_trailers = self.trailer_api.get_movie_trailers(
                    movie_id=random_movie.get("id"), sites=["YouTube"]
                )

                if not random_movie:
                    await message.reply_text(
                        "No movies were found for this category 😔"
                    )
                    return

                # reply to bot with the movie poster if any
                if random_movie.get("poster_path") or random_movie.get("backdrop_path"):
                    media_group = []
                    if random_movie.get("poster_path"):
                        media_group.append(
                            InputMediaPhoto(
                                media=f"https://image.tmdb.org/t/p/w500{random_movie.get('poster_path')}",
                                caption="Movie Poster",
                            ),
                        )
                    if random_movie.get("backdrop_path"):
                        media_group.append(
                            InputMediaPhoto(
                                media=f"https://image.tmdb.org/t/p/w500{random_movie.get('backdrop_path')}",
                                caption="Movie Backdrop",
                            ),
                        )
                    await message.reply_media_group(media=media_group)

                # reply to bot with the movie reponse
                await message.reply_html(get_movie_response(movie=random_movie))

                # reply to bot with the movie trailers if any
                if movie_trailers:
                    await message.reply_text("Watch YouTube Movie Trailers 👇")
                    for trailer in movie_trailers:
                        await message.reply_html(
                            f"<a href='https://www.youtube.com/watch?v={trailer.get('key')}'>{html.escape(trailer.get('name'))}</a>"
                        )
                else:
                    await message.reply_text(
                        "No YouTube movie trailers found for this movie"
                    )
            except Exception as e:
                logger.exception(
                    "something went wrong while executing suggest_movie_command: %s", e
                )
                if message:
                    await message.reply_text(
                        "Something went wrong. Please try again later :("
                    )

            keyboard = [
                [
                    InlineKeyboardButton(
                        f"Suggest another {category_name} movie 🎬",
                        callback_data=category.name.lower(),
                    )
                ],
                [InlineKeyboardButton("Menu 🏠", callback_data="menu")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await message.reply_text(
                "What would you like next?", reply_markup=reply_markup
            )
            return

        return suggest_movie_command
