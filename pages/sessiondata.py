import streamlit as st
from getdata import get_session
import charts


st.set_page_config(page_title="Slipstream", layout="wide")
st.header("Session Data")
with st.sidebar:
    st.subheader("Session")
    year=st.number_input("Year", min_value=2018,max_value=2026,value=2026)
    race=st.text_input("Race", value="Interlagos")
    sessiontype=st.selectbox("Session Type", ["Q","R"])
    load=st.button("Load Session", width="stretch")
if load:
    try:
        with st.spinner("Loading race data"):
            session=get_session(year,race,sessiontype)
        st.session_state['session']=session
        st.session_state['year']=year
        st.session_state['race']=race
        st.session_state['session_type']=sessiontype
    except Exception as e:
        st.session_state.pop('session', None)
        st.error(f"Error: {e}")
if 'session' in st.session_state:
    session=st.session_state['session']
    year=st.session_state['year']
    race=st.session_state['race']
    sessiontype=st.session_state['session_type']
    st.caption(f"{race} {year} / {sessiontype}")

    drivers=session.results['Abbreviation'].dropna().unique().tolist()
    if len(drivers) <2:
        st.write("Add more drivers")
    else:
        with st.sidebar:
            selected=st.multiselect(
                "Drivers",
                drivers,
                default=drivers[:min(3, len(drivers))],
                max_selections=10)
        if selected:
            tab1, tab2 = st.tabs(["Fastest Laps", "Track Evolution and Consistency"])
            with tab1:
                st.plotly_chart(
                    charts.fastestoverall_chart(session),
                    width="stretch")
                st.plotly_chart(
                    charts.fastestlap_chart(session,selected),
                    width="stretch")
            with tab2:
                st.plotly_chart(
                    charts.trackevo_chart(session),
                    width="stretch")
                for driver in selected:
                    st.plotly_chart(
                        charts.consistency_chart(session,driver),
                        width="stretch")
