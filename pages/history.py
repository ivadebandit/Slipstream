import streamlit as st
import charts
from getdata import get_session
import fastf1

st.set_page_config(page_title="Slipstream",layout="wide")
st.header("Historical Circuit Stats")
with st.sidebar:
    st.subheader("Base Session")
    year=st.number_input("Year", min_value=2018,max_value=2026, value=2026)
    race=st.text_input("Race",value="Monza")
    load=st.button("Load Session", width="stretch")
if load:
    try:
        with st.spinner("Loading base session"):
            session=get_session(year,race,"R")
            st.session_state['histsession']=session
            calendar= fastf1.get_event_schedule(year)
            calendar=calendar[calendar['EventFormat'] != 'testing']
            st.session_state['histraces'] = calendar['EventName'].tolist()
    except Exception as e:
        st.session_state.pop('histsession', None)
        st.session_state.pop('histraces', None)
        st.error(f"Error: {e}")
if 'histsession' in st.session_state:
    session=st.session_state['histsession']
    allraces= st.session_state['histraces']
    drivers= session.results['Abbreviation'].dropna().unique().tolist()

    with st.sidebar:
        st.divider()
        st.subheader("Historical setup")
        driver=st.selectbox("Driver",drivers,index=0)
        circuit=st.selectbox("Circuit", allraces, index=0)
        years=st.multiselect("Years", [2018,2019,2020,2021,2022,2023,2024,2025,2026],
                             default=[2022,2023,2024,2025,2026])
    if len(years) < 2:
        st.write("Please select at least 2 years")
    else:
        st.caption(f"{driver} at {circuit} across {len(years)} years")
        tab1,tab2,tab3 = st.tabs(["Race History", "Qualifying History", "All time record"])
        with tab1:
            st.subheader(f"{driver} Race Positions")
            st.plotly_chart(
                charts.racepositions_chart(driver,circuit,years),
                width="stretch")

            st.subheader(f"{driver} Finsh stats")
            st.plotly_chart(
                charts.finishstats_chart(driver,circuit,years),
                width="stretch")
        with tab2:
            st.subheader(f"{driver} Qualifying Positions")
            st.plotly_chart(
                charts.chart_qualipositions(driver,circuit,years),
                width="stretch")
            st.subheader(f"{driver} Best Qualifying Laps")
            st.plotly_chart(
                charts.bestlapsq_chart(driver,circuit,years),
                width="stretch")
        with tab3:

            st.subheader(f"All Time Fastest Lap at {circuit}")
            st.plotly_chart(
                charts.fastestalltime_chart([circuit], years),
                width="stretch")

            
                                                                                