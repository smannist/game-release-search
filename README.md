# Description

The application allows the user to search for the latest video game releases on most modern platforms (e.g. PC, PS5) as well as rate them based on their level of interest.

## Features

- The user can create a new account, which can then be used to sign in to the application
- The user will be able to see a list of all available platforms
- By selecting a platform the user will be able to preview all upcoming video game releases on that platform
- The user can view additional information about the game (release date, synopsis, etc.)
- The user can rate the selected video game based on their level of interest
- The user can see a list of video games they have previously rated
- The administrator can edit, add, and remove platforms and / or games
- The administrator can see a list of all video game ratings
- The administrator can delete video game ratings

## Current state, testing the application and future ideas

All planned features are working.

The application can be tested at [Heroku](https://game-release-search.herokuapp.com/).

Ideas for the future:

- Better UI
- Improvements to game management
- Small game icons to game view

## Running the application locally

1. Install and run PostgreSQL database.
2. Clone the repository

Create the following .env file:

```
DATABASE_URL=database location
SECRET_KEY=secure key
```

Setup and run venv virtual environment:

```
python3 -m venv venv
source venv/bin/activate
```

Install requirements:

```
pip install -r requirements.txt
```

Populate the database:

```
psql < schema/schema.sql
```

And finally to run the application:

```
flask --app app.py run
```
