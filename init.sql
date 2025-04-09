CREATE TABLE IF NOT EXISTS aircrafts (
    aircraft_id VARCHAR(20) PRIMARY KEY,
    model VARCHAR(50),
    aircraft_name VARCHAR(50),
    registration VARCHAR(30),
    airline_company VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS flights (
    id SERIAL PRIMARY KEY,
    icao VARCHAR(20),
    aircraft_id VARCHAR(20) REFERENCES aircrafts(aircraft_id),
    timestamp TIMESTAMP NOT NULL,
    lat NUMERIC(10,6),
    lon NUMERIC(10,6),
    altitude NUMERIC(12,6),
    speed NUMERIC(12,3),
    heading NUMERIC(6,2)
);
