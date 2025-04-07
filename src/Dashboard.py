import streamlit as st
import pandas as pd
import psycopg2

from DBcomm import DBConnect
from Report import GetReportModelAndAirlineByDay
from Report import GetReportModelAndAirlineByHour
from Report import GetReportAirlineByDay
from Report import GetReportAirlineByHour
from Report import GetReportModelByDay
from Report import GetReportModelByHour

def GetData() : 
    conn = DBConnect()
    q = pd.read_sql_query('SELECT * FROM public.flighttable',conn)
    conn.close()
    return q

def main() : 
    st.title("Самолеты над Черным Морем")
    q = GetData()
    if not q.empty: 
        repByHour = GetReportModelAndAirlineByHour()
        repByDay = GetReportModelAndAirlineByDay()
        st.map(q[['lat','lon']])
        st.header("Таблица со всеми самолетами")
        st.dataframe(q)
        if (not repByHour.empty and not repByDay.empty): 
            st.header("""Таблица "Количество рейсов по моделям самолётов и авиакомпаниям в заданной акватории за час." """)
            st.dataframe(repByHour)
            st.header("""Таблица "Количество рейсов по моделям самолётов и авиакомпаниям в заданной акватории за день." """)
            st.dataframe(repByDay)

        repByHour = GetReportModelByHour()
        repByDay = GetReportModelByDay()
        if (not repByHour.empty and not repByDay.empty): 
            st.header("""Таблица "Количество рейсов по авиакомпаниям в заданной акватории за час." """)
            st.dataframe(repByHour)
            st.header("""Таблица "Количество рейсов по авиакомпаниям в заданной акватории за день." """)
            st.dataframe(repByDay)

        repByHour = GetReportAirlineByHour()
        repByDay = GetReportAirlineByDay()
        if (not repByHour.empty and not repByDay.empty): 
            st.header("""Таблица "Количество рейсов по моделям самолётов в заданной акватории за час." """)
            st.dataframe(repByHour)
            st.header("""Таблица "Количество рейсов по моделям самолётов в заданной акватории за день." """)
            st.dataframe(repByDay)
    else: st.write("Нет Данных")

main() 