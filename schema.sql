CREATE TABLE restaurants (
    id SERIAL PRIMARY KEY,
    name VARCHAR (50) NOT NULL,
    location POINT NOT NULL,
    description VARCHAR(500),
    visible INTEGER NOT NULL
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR (20) UNIQUE NOT NULL,
    password VARCHAR NOT NULL,
    role INTEGER
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    restaurant_id INTEGER REFERENCES restaurants,
    user_id INTEGER REFERENCES users,
    stars INTEGER NOT NULL,
    comment VARCHAR (500)
);

CREATE TABLE restaurantinformation (
    id SERIAL PRIMARY KEY,
    restaurant_id INTEGER REFERENCES restaurants,
    key VARCHAR (50) NOT NULL,
    value VARCHAR (500) NOT NULL,
    visible INTEGER NOT NULL
);

CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR (50) UNIQUE NOT NULL,
    visible INTEGER NOT NULL
);

CREATE TABLE restaurantsingroups (
    group_id INTEGER REFERENCES groups,
    restaurant_id INTEGER REFERENCES restaurants
);
