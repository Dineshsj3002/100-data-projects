-- Revised CREATE TABLE statement
CREATE TABLE netflix_titles (
    show_id VARCHAR(10) PRIMARY KEY,
    type VARCHAR(10),
    title TEXT,
    director TEXT,
    "cast" TEXT, -- "cast" is a reserved keyword
    country TEXT,
    date_added DATE,
    release_year INT,
    rating VARCHAR(10),
    duration TEXT,
    listed_in TEXT,
    description TEXT
);
