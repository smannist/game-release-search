# Description

Video game release search and management

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

## Current state, testing the application and future

All planned features are working. If you want to test admin features, you can use the following account:

| Username | Password |
| -------- | -------- |
| admin    | admin    |

The application can be tested at [Heroku](https://game-release-search.herokuapp.com/).

Plans for the future:

- Better UI
- Small icons for games
- More descriptive error handling / confirmation messages
- Dynamic pop-ups instead of flash messaging (much nicer)

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

Create database tables:

```
psql < schema/schema.sql
```

And finally to run the application:

```
flask --app app.py run
```
