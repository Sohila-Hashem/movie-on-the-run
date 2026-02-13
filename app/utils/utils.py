from functools import lru_cache
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from app.services.Movies.movies_service import MovieCategory


def get_movie_response(movie: dict) -> str:
    """Returns a formatted movie response.

    Args:
        movie (dict): The movie dictionary.

    Returns:
        str: The formatted movie response.
    """
    return f"""
<b>Title:</b> {movie.get("original_title")}\n
<b>Description:</b>\n{movie.get("overview") or "N/A"}\n
<b>Vote/Rating Avg:</b> {f"{movie.get("vote_average"):.1f}"}\n
<b>Release Date:</b> {movie.get("release_date")}\n
<b>Geners:</b> {", ".join([convert_snake_case_str_to_title(MovieCategory(genre_id).name).capitalize() for genre_id in movie.get("genre_ids")])}\n
"""


def convert_snake_case_str_to_title(snake_case_str: str) -> str:
    """Converts a snake_case string to a title case string.

    Args:
        snake_case_str (str): The snake_case string to convert.

    Returns:
        str: The title case string.
    """
    if not snake_case_str:
        return ""
    return snake_case_str.replace("_", " ").title()


@lru_cache(maxsize=100)
def get_categories_keyboard():
    """
    Returns the categories keyboard.

    Returns:
        InlineKeyboardMarkup: The categories keyboard.
    """
    keyboard = [
        [
            InlineKeyboardButton(
                convert_snake_case_str_to_title(category.name).capitalize(),
                callback_data=category.name.lower(),
            )
        ]
        for category in MovieCategory
    ]
    return InlineKeyboardMarkup(keyboard)
