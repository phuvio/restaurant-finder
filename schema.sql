CREATE TABLE restaurants (
    id SERIAL PRIMARY KEY,
    name VARCHAR (50)
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR (20) UNIQUE,
    password VARCHAR (50),
    is_admin BOOLEAN
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    restaurant_id INTEGER REFERENCES restaurants,
    user_id INTEGER REFERENCES users,
    stars INTEGER,
    comment VARCHAR (500)
);

CREATE TABLE restaurantinformation (
    id SERIAL PRIMARY KEY,
    restaurant_id INTEGER REFERENCES restaurants,
    key VARCHAR (50) UNIQUE,
    value VARCHAR (500)
);

CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR (50) UNIQUE
);

CREATE TABLE restaurantsingroups (
    group_id INTEGER REFERENCES groups,
    restaurant_id INTEGER REFERENCES restaurants
);
