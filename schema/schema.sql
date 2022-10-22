CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE IF NOT EXISTS roles (
    role TEXT UNIQUE,
    user_id INT REFERENCES users(id)
)

CREATE TABLE IF NOT EXISTS platforms (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    image BYTEA
);

CREATE TABLE IF NOT EXISTS games (
    id SERIAL PRIMARY KEY,
    title TEXT,
    synopsis TEXT,
    release_date DATE,
    platform_id INT REFERENCES platforms(id) ON DELETE CASCADE,
    israted BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS ratings (
    id SERIAL PRIMARY KEY,
    rating INT,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    game_id INT REFERENCES games(id) ON DELETE CASCADE
);