import streamlit as st
import pandas as pd
import psycopg2
import pydeck as pdk

from DBcomm import DBConnect
from Report import GetReportModelAndAirlineByDay
from Report import GetReportModelAndAirlineByHour
from Report import GetReportAirlineByDay
from Report import GetReportAirlineByHour
from Report import GetReportModelByDay
from Report import GetReportModelByHour

def GetData() : 
    conn = DBConnect()
    q = pd.read_sql_query('''SELECT f.*, a.model, a.aircraft_name, a.airline_company
    FROM public.flights f
    JOIN public.aircrafts a ON f.aircraft_id = a.aircraft_id''',conn)
    conn.close()
    return q

def GetFlightData():
    conn = DBConnect()
    df = pd.read_sql_query("""SELECT f.timestamp, f.aircraft_id, f.lat, f.lon,
    a.model, a.aircraft_name, a.registration, a.airline_company
    FROM flights f
    JOIN aircrafts a ON f.aircraft_id = a.aircraft_id
    ORDER BY f.aircraft_id, f.timestamp
    """, conn)
    conn.close()
    return df

def GetAircraftWay():
    data = GetData()
    data["lat"] = pd.to_numeric(data["lat"], errors="coerce")
    data["lon"] = pd.to_numeric(data["lon"], errors="coerce")
    data = data.dropna(subset=["icao", "lat", "lon", "timestamp"])
    data = data.sort_values(by=["icao", "timestamp"])

    lines = []
    for icao in data["icao"].unique():
        group = data[data["icao"] == icao].copy()
        group = group.dropna(subset=["lat", "lon"])

        lons = list(group["lon"])
        lats = list(group["lat"])

        for i in range(len(lons) - 1):
            lon1, lat1 = lons[i], lats[i]
            lon2, lat2 = lons[i + 1], lats[i + 1]

            if lon1 != lon2 or lat1 != lat2:
                lines.append({
                    "from_lon": lon1,
                    "from_lat": lat1,
                    "to_lon": lon2,
                    "to_lat": lat2
                })

    line_df = pd.DataFrame(lines)

    if not line_df.empty:
        st.pydeck_chart(pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state=pdk.ViewState(
                latitude=data["lat"].mean(),
                longitude=data["lon"].mean(),
                zoom=6,
                pitch=0
            ),
            layers=[
                pdk.Layer(
                    "LineLayer",
                    data=line_df,
                    get_source_position='[from_lon, from_lat]',
                    get_target_position='[to_lon, to_lat]',
                    get_width=2,
                    get_color='[255, 0, 0]'
                )
            ]
        ))
    else:
        st.pydeck_chart(pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state=pdk.ViewState(
                latitude=data["lat"].mean(),
                longitude=data["lon"].mean(),
                zoom=6,
                pitch=0
            ),
            layers=[
                pdk.Layer(
                    "ScatterplotLayer",
                    data=data,
                    get_position='[lon, lat]',
                    get_radius=3000,
                    get_color='[0, 100, 200]',
                    pickable=True,
                )
            ]
        ))

def main():
    st.title("Самолеты над Черным Морем")
    q = GetData()
    GetAircraftWay()

    if not q.empty:
        repByHour = GetReportModelAndAirlineByHour()
        repByDay = GetReportModelAndAirlineByDay()

        st.header("Таблица со всеми самолетами")
        unique_planes = q.drop_duplicates(subset=["aircraft_id"])
        unique_planes = unique_planes[["aircraft_id", "model", "airline_company", "aircraft_name", "icao"]]
        st.dataframe(unique_planes.reset_index(drop=True))

        if (not repByHour.empty and not repByDay.empty): 
            st.header("Таблица: Количество рейсов по моделям самолётов и авиакомпаниям в заданной акватории за час.")
            st.dataframe(repByHour)
            st.header("Таблица: Количество рейсов по моделям самолётов и авиакомпаниям в заданной акватории за день.")
            st.dataframe(repByDay)

        repByHour = GetReportModelByHour()
        repByDay = GetReportModelByDay()
        if (not repByHour.empty and not repByDay.empty): 
            st.header("Таблица: Количество рейсов по моделям самолётов в заданной акватории за час.")
            st.dataframe(repByHour)
            st.header("Таблица: Количество рейсов по моделям самолётов в заданной акватории за день.")
            st.dataframe(repByDay)

        repByHour = GetReportAirlineByHour()
        repByDay = GetReportAirlineByDay()
        if (not repByHour.empty and not repByDay.empty): 
            st.header("Таблица: Количество рейсов по авиакомпаниям в заданной акватории за час.")
            st.dataframe(repByHour)
            st.header("Таблица: Количество рейсов по авиакомпаниям в заданной акватории за день.")
            st.dataframe(repByDay)
    else:
        st.write("Нет Данных")


main() 
#http://localhost:8501