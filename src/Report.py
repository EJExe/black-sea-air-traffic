import psycopg2
import time 
import pandas as pd
from DBcomm import DBConnect

def GetReportModelAndAirlineByHour(): 
    conn = DBConnect() 
    q = """SELECT DATE_TRUNC('hour',timestamp) as timeH , aircraft_model, aircraft_airline_company, COUNT(*) AS flight_count
    FROM public.flighttable GROUP BY timeH,aircraft_model,aircraft_airline_company
    ORDER BY timeH DESC, flight_count DESC"""
    q = pd.read_sql_query(q,conn)
    conn.close()
    return q

def GetReportModelAndAirlineByDay(): 
    conn = DBConnect() 
    q = """SELECT DATE_TRUNC('day',timestamp) as timeD , aircraft_model, aircraft_airline_company, COUNT(*) AS flight_count
    FROM public.flighttable GROUP BY timeD,aircraft_model,aircraft_airline_company
    ORDER BY timeD DESC, flight_count DESC"""
    q = pd.read_sql_query(q,conn)
    conn.close()
    return q

def GetReportModelByHour(): 
    conn = DBConnect() 
    q = """SELECT DATE_TRUNC('hour',timestamp) as timeH , aircraft_model, COUNT(*) AS flight_count
    FROM public.flighttable GROUP BY timeH,aircraft_model
    ORDER BY timeH DESC, flight_count DESC"""
    q = pd.read_sql_query(q,conn)
    conn.close()
    return q

def GetReportModelByDay(): 
    conn = DBConnect() 
    q = """SELECT DATE_TRUNC('day',timestamp) as timeD , aircraft_model, COUNT(*) AS flight_count
    FROM public.flighttable GROUP BY timeD,aircraft_model
    ORDER BY timeD DESC, flight_count DESC"""
    q = pd.read_sql_query(q,conn)
    conn.close()
    return q

def GetReportAirlineByHour(): 
    conn = DBConnect() 
    q = """SELECT DATE_TRUNC('hour',timestamp) as timeH , aircraft_airline_company, COUNT(*) AS flight_count
    FROM public.flighttable GROUP BY timeH,aircraft_airline_company
    ORDER BY timeH DESC, flight_count DESC"""
    q = pd.read_sql_query(q,conn)
    conn.close()
    return q

def GetReportAirlineByDay(): 
    conn = DBConnect() 
    q = """SELECT DATE_TRUNC('day',timestamp) as timeD , aircraft_airline_company, COUNT(*) AS flight_count
    FROM public.flighttable GROUP BY timeD,aircraft_airline_company
    ORDER BY timeD DESC, flight_count DESC"""
    q = pd.read_sql_query(q,conn)
    conn.close()
    return q