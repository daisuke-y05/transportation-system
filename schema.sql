CREATE TABLE IF NOT EXISTS transportation (

    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    name TEXT NOT NULL,
    month TEXT NOT NULL,

    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,

    departure TEXT NOT NULL,
    destination TEXT NOT NULL,

    transport TEXT NOT NULL,
    trip_type TEXT NOT NULL,

    fare INTEGER NOT NULL,

    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS submissions (

    name TEXT NOT NULL,
    month TEXT NOT NULL,

    submitted_at TIMESTAMP NOT NULL,

    UNIQUE(name, month)

);