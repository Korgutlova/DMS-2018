CREATE TABLE IF NOT EXISTS reservation (
    pk varchar(100) PRIMARY KEY,
    data jsonb NOT NULL
);

COPY reservation (data) FROM '/data/out/reservation.csv' (FORMAT csv, header)
