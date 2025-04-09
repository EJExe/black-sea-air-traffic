import requests
import psycopg2
import csv 
import os 
from datetime import datetime
from datetime import date 
from dotenv import load_dotenv
import time 
from DBcomm import DBConnect

def BlackSeaFilter (lat,lon):
    blackSeaBorders = {
    "lat_min": 41.0,
    "lat_max": 46.0,
    "lon_min": 28.0,
    "lon_max": 42.0
        }
    if ( blackSeaBorders["lat_min"] < lat and blackSeaBorders["lat_max"] > lat and blackSeaBorders["lon_min"] < lon and blackSeaBorders["lon_max"] > lon ) :
        return True
    else: return False

def SaveToFile(data: dict):
    filepath = "flights.csv"
    file_exists = os.path.exists(filepath) and os.path.getsize(filepath) > 0
    with open('flights.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

def SortData(info: list) -> dict:
    def safe_get(index):
        try:
            return str(info[index]) if info[index] is not None else ""
        except IndexError:
            return ""

    return {
        'icao': safe_get(0),
        'lat': safe_get(1),
        'lon': safe_get(2),
        'altitude': safe_get(3),
        'speed': safe_get(4),
        'heading': safe_get(5),
        'model': safe_get(8),
        'registration': safe_get(9),
        'startPoint': safe_get(11),
        'endPoint': safe_get(12),
        'flightNumber': safe_get(13),
        'aircraftName': safe_get(16),
        'airline': safe_get(18)
    }

def GetInfoAboutFlights ():
    bounds = "46.5, 42.5, 41.0, 28.5"  # lat_max, lon_max, lat_min, lon_min
    url = f"https://data-cloud.flightradar24.com/zones/fcgi/feed.js?bounds={bounds}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    aircraft_data = {k: v for k, v in data.items() if k not in ['full_count', 'version']}

    for aircraft_id, info in aircraft_data.items():
        lat = info[1]
        lon = info[2]
        if ( BlackSeaFilter(lat,lon) == True ):
            print(aircraft_id," ",info[16])
            dictinfo = SortData(info)
            rec = { 
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'aircraft_id': aircraft_id,
                **dictinfo
            }
            SaveToFile(rec)
            SaveToDataBD(rec)

def SaveToDataBD( data : dict): 
    try: 
        conn = DBConnect()
        if conn is None:
            print("Error: No connection to DB.")
            return
        cur = conn.cursor()
        cur.execute("""INSERT INTO aircrafts (aircraft_id, model, aircraft_name, registration, airline_company)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (aircraft_id) DO NOTHING""", 
            (data['aircraft_id'], data['model'], data['aircraftName'], 
            data['registration'], data['airline']))

        cur.execute("""INSERT INTO flights (aircraft_id, timestamp, lat, lon, altitude, speed, heading, icao)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", 
        (data['aircraft_id'], data['timestamp'], data['lat'], data['lon'], 
        data['altitude'], data['speed'], data['heading'], data['icao']))

        conn.commit()
        cur.close()
        conn.close() 
    except Exception as e: 
        print("Error: Cant add to BD: ", str(e))

def main() : 
    load_dotenv()
    GetInfoAboutFlights()

main()
