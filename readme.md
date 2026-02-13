# Movie on the Run

Telegram bot that provides movie suggestions on the run based on your selected category.

## Demo

**Live Telegram Bot:** [@MovieOnTheRunBot](https://web.telegram.org/k/#@MovieOnTheRunBot)

## Problem

Ever struggle to decide what movie to watch? With so many streaming options and categories, it’s easy to waste time scrolling endlessly without finding anything interesting.

## Solution

I built a minimalistic Telegram bot that allows users to:

- Receive random movie suggestions from 19 different categories
- Get movie details: title, description, release date, poster, rating, and a list of official YouTube trailers if available
- Quickly view trailers from Telegram without leaving the app.
- Explore different genres effortlessly.

## Tech Stack

### Bot

- **Python 3.x**  
  Lightweight and easy to maintain without any additional frameworks.

- **python-telegram-bot**  
  Handles Telegram interactions, commands, and message formatting directly.

- **TMDB API**  
  Large API that fetches movie data in real-time, including posters, ratings, and descriptions.

## Architecture Overview (High Level)

- Telegram Bot Layer: Handles incoming messages, commands, and user interactions.
- Movie Service Layer: Queries TMDB API for random movies based on selected categories.
- Response Layer: Formats movie information and sends it back to the user in Telegram.

## Getting Started (Dev Setup)

### Prerequisites

- Python 3.10+
- python-telegram-bot v20+
- TMDB API key
- Telegram Bot Token

### Installation

1. Clone the repository:

```bash
git clone https://github.com/Sohila-Hashem/movie-on-the-run.git
```

2. Navigate to the project directory:

```bash
cd movie-on-the-run
```

3. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Set up environment variables in a .env file to run project locally:

```bash
BOT_TOKEN_DEV=your_telegram_bot_token
ENV=development
MOVIES_API_KEY=your_tmdb_api_key
```

6. Run the bot:

```bash
python bot.py
```

7. Open Telegram and start chatting with [@name_of_your_bot](https://web.telegram.org/k/#@name_of_your_bot)

## Roadmap / Features to Be Added

- [ ] Include external links for movies
- [ ] Support multi-language responses
- [ ] Allow user preferences (e.g., specific rating, release date, watch provider, language, people, region, country and etc)
