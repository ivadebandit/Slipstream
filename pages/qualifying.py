import streamlit as st
from getdata import get_session
import charts

st.set_page_config(page_title="Slipstream", layout="wide")
st.header("Qualifying and Telemetry")

with st.sidebar:
    st.subheader("Session")
    year=st.number_input("Year", min_value=2018, max_value=2026, value=2026)
    race=st.text_input("Race", value="Suzuka")
    sessiontype=st.selectbox("Session Type", ["Q"])
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
        st.error(f"Error {e}")
if 'session' in st.session_state:
    session=st.session_state['session']
    year=st.session_state['year']
    race=st.session_state['race']
    sessiontype=st.session_state['session_type']
    st.caption(f"{race} {year} / {sessiontype}")


    drivers=session.results['Abbreviation'].dropna().unique().tolist()
    if len(drivers) < 2:
        st.write("Add more drivers")
    else:
        with st.sidebar:
            selected=st.multiselect(
                "Drivers",
                drivers,
                default=drivers[:min(2, len(drivers))],
                max_selections=10)
        if selected:
            tab1, tab2=st.tabs(["Qualifying Pace", "Telemetry"])
            with tab1:

                if sessiontype != "Q":
                    st.write("Choose qualifying session")
                else:
                    for driver in selected:
                        st.subheader(driver)
                        st.plotly_chart(
                            charts.qualiprog_chart(session,driver),
                            width="stretch")
                        st.plotly_chart(
                            charts.perfectlap_chart(session,driver),
                            width="stretch")
            with tab2:
                for driver in selected:
                    st.subheader(driver)
                    st.plotly_chart(
                        charts.drszones_chart(session,driver),
                        width="stretch")
                st.subheader("Delta Comparison")
                if len(selected) == 2:
                    d1=selected[0]
                    d2=selected[1] 
                    st.plotly_chart(
                        charts.delta_chart(d1,d2,session),
                        width="stretch")
                else:
                    st.write("Choose exactly 2 drivers")


