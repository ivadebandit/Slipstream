import streamlit as st
from getdata import get_session
from charts import fastestlap_chart, driverstandings_chart

st.set_page_config(page_title="Slipstream", layout="wide")

st.markdown("<h2 style='font-weight: 400; margin-bottom: 0;'>Slipstream</h2>", unsafe_allow_html=True)

with st.sidebar:
    st.header("Session")
    year = st.number_input("Year", min_value=2018, max_value=2026, value=2026)
    event = st.text_input("Event", value="Yas Marina")
    session_type = st.selectbox("Session Type", ["Q", "R"])
    load_btn = st.button("Load Session", width=True)

if load_btn:
    with st.spinner("Loading data"):
        try:
            session = get_session(year, event, session_type)
            st.write(f"**{event} {year} - {session_type}**")
            tab1, tab2 = st.tabs(["Laps", "Standings"])
            with tab1:
                drivers = ["ALB", "HAM", "NOR", "ALO", "GAS"]
                fig1 = fastestlap_chart(session, drivers)
                st.plotly_chart(fig1,width=True)
            with tab2:
                fig2 = driverstandings_chart(year, [event], session)
                st.plotly_chart(fig2,width=True)
        except Exception as e:
            st.error(f"Error: {e}")
            