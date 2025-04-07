CREATE TABLE IF NOT EXISTS public.flighttable(
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL, 
    aircraft_id VARCHAR(20) NOT NULL,
    icao VARCHAR(20), 
    lat NUMERIC(10,6),
    lon NUMERIC(10,6),
    aircraft_name VARCHAR(50),
    aircraft_model VARCHAR(50),
    aircraft_airline_company VARCHAR(50),
    altitude NUMERIC(12,6),
    speed NUMERIC(12,3)
);
