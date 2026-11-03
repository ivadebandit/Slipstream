import streamlit as st
st.set_page_config(page_title="Slipstream", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;600&family=Inter:wght@400;500;600&display=swap');
    html, body, [class*="css"], .stApp, .stMarkdown, p, span, label, input, select {
        font-family: 'Inter', sans-serif !important; }
    h1, h2, h3, h4, h5, h6 {
        font-family: 'IBM Plex Sans', sans-serif !important; }
    .material-symbols-rounded, .material-icons, [data-testid="stSidebarCollapseButton"] span {
        font-family: 'Material Symbols Rounded', 'Material Icons' !important;}
    </style>
""", unsafe_allow_html=True)

pg = st.navigation([
    st.Page("pages/1_Race_Pace.py", title="Pace & Tires", default=True),
    st.Page("pages/Race_Strategy.py", title="Strategy"),
    st.Page("pages/sessiondata.py", title="Sesssion Data"),
    st.Page("pages/standings.py", title="Standings"),
    st.Page("pages/qualifying.py", title="Qualifying and Telemetry"),
    st.Page("pages/comparisons.py", title="Driver Comparisons"),
    st.Page("pages/history.py", title="Historical Track Data")])
pg.run()