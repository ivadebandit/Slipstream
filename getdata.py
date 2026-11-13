import tif1
import fastf1
import streamlit as st
def get_session(year, gp, identifier):
    session = tif1.get_session(year, gp, identifier)
    return session

@st.cache_data
def races(year):
    schedule=fastf1.get_event_schedule(year)
    schedule=schedule[schedule['EventFormat'] != 'testing']
    return schedule['EventName'].tolist()