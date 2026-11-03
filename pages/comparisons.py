import streamlit as st
from getdata import get_session
import charts
import fastf1

st.set_page_config(page_title="Slipstream", layout="wide")
st.header("Driver Comparisons")
with st.sidebar:
    st.subheader("Base session")
    year=st.number_input("Year", min_value=2018, max_value=2026, value=2026)
    race=st.text_input("Race", value="Monza")
    load=st.button("Load Session", width="stretch")
if load:
    try:
        with st.spinner("Loading base session"):
            session=get_session(year,race,"R")
        st.session_state['comp_session']=session

        calendar = fastf1.get_event_schedule(year)
        calendar = calendar[calendar['EventFormat'] != 'testing']
        st.session_state['comp_races'] = calendar['EventName'].tolist()

    except Exception as e:
        st.session_state.pop('comp_session', None)
        st.error(f"Error: {e}")
if 'comp_session' in st.session_state:
    session = st.session_state['comp_session']
    allraces = st.session_state['comp_races']
    drivers = session.results['Abbreviation'].dropna().unique().tolist()

    with st.sidebar:
        st.divider()
        st.subheader("Comparison setup")
        d1=st.selectbox("Driver 1", drivers, index=0)
        d2=st.selectbox("Driver 2", drivers,index=1)

        years=st.multiselect("Years", [2018,2019,2020,2021,2022,2023,2024,2025,2026], default=[2023,2024])
        races=st.multiselect("Races", allraces, default=[allraces[0]])
    if d1 == d2:
        st.write("Select two different drivers")
    else:
        if year not in years:
            st.warning("The base session year should be the same as the year in chosen comparison years")
        st.caption(f"Comparing {d1} and {d2}")



        tab1,tab2,tab3 = st.tabs(["Head to Head","Conditions","Career Stats"])
        with tab1:
            st.subheader(f"{d1} vs {d2} Race Pace")
            st.plotly_chart(
                charts.teammategappace_chart(session,d1,d2),
                width="stretch")
            st.subheader("Qualifying gap by circuit")
            st.plotly_chart(
                charts.teammategapquali_chart(d1,d2,races,years),
                width="stretch")

            st.subheader("Head to Head qualifying wins")
            st.plotly_chart(
                charts.h2h_chart(races,d1,d2,years,session),
                width="stretch")

        with tab2:
            st.subheader("Wet vs Dry performance")
            st.plotly_chart(
                charts.wetdrycomp_chart([session], [d1,d2]),
                width="stretch")
        with tab3:
            st.subheader("Career Stats (wins, podiums, pole positions)")
            st.plotly_chart(
                charts.careerstats_chart(years,races, [d1,d2]),
                width="stretch")
