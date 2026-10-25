import streamlit as st
from getdata import get_session
from charts import fastestlap_chart, driverstandings_chart

st.set_page_config(page_title="Slipstream", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;600&family=Inter:wght@400;500;600&display=swap');
    html, body, [class*="css"], .stApp, .stMarkdown, p, span, label, input, select {
        font-family: 'Inter', sans-serif !important;}
    h1, h2, h3, h4, h5, h6 {
        font-family: 'IBM Plex Sans', sans-serif !important;}
        .material-symbols-rounded, .material-icons, [data-testid="stSidebarCollapseButton"] span {
        font-family: 'Material Symbols Rounded', 'Material Icons' !important;}
        .main-title {
        font-family: 'IBM Plex Sans', sans-serif !important;
        font-size: 36px;
        font-weight: 600; 
        margin-bottom: 0;
        padding-bottom: 0;}
    </style>
""", unsafe_allow_html=True)


st.markdown('<div class="main-title">Slipstream</div>', unsafe_allow_html=True)
with st.sidebar:
    st.header("Session")
    year = st.number_input("Year", min_value=2018, max_value=2026, value=2026)
    event = st.text_input("Event", value="Yas Marina")
    session_type = st.selectbox("Session Type", ["Q", "R"])
    load_btn = st.button("Load Session", use_container_width=True)
if load_btn:
    with st.spinner("Loading data"):
        try:
            session = get_session(year, event, session_type)
            st.caption(f"{event} {year} / {session_type}")
            tab1, tab2 = st.tabs(["Laps", "Standings"])
            with tab1:
                drivers = ["ALB", "HAM", "NOR", "ALO", "GAS"]
                fig1 = fastestlap_chart(session, drivers)
                st.plotly_chart(fig1, use_container_width=True)
            with tab2:
                fig2 = driverstandings_chart(year,[event],session)
                st.plotly_chart(fig2, use_container_width=True)
        except Exception as e:
            st.error(f"Error: {e}")