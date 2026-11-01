import streamlit as st
import fastf1
from getdata import get_session
import charts

st.set_page_config(page_title="Slipstream", layout="wide")
st.header("Standings")

with st.sidebar:
    st.subheader("Season")
    year=st.number_input("Year", min_value=2018,max_value=2026, value=2024)
    load=st.button("Load Year", width="stretch")
if load:
    try:
        with st.spinner("Loading races"):
            calendar= fastf1.get_event_schedule(year)
            calendar=calendar[calendar['EventFormat'] != 'testing']
            races = calendar['EventName'].tolist()
            last = races[-1]
            session =get_session(year,last,'R')

            st.session_state['standings_year'] =year
            st.session_state['standings_races'] = races
            st.session_state['standings_session'] =session
    except Exception as e:
        st.error(f"Error: {e}")
if 'standings_year' in st.session_state:
    year= st.session_state['standings_year']
    races=st.session_state['standings_races']
    session=st.session_state['standings_session']

    st.caption(f"{year} Season")
    tab1, tab2, tab3 = st.tabs(["Driver Standings", "Team Standings", "Championship Battle"])
    with tab1:
        st.plotly_chart(
            charts.driverstandings_chart(year,races,session),
            width="stretch")
    with tab2:
        st.plotly_chart(
            charts.teamstandings_chart(year,races,session),
            width="stretch")
    with tab3:
        st.plotly_chart(
            charts.championshipbattle_chart(year,races,session),
            width="stretch")