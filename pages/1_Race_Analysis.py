import streamlit as st
from getdata import get_session
import charts
# racepace, deg, compoundpace, stintsum, compoundusage, fueleffect
# qualiprog, perfectlap,position progresss, pos gained, start,
#box, under/overcut



st.set_page_config(page_title="Slipstream",layout="wide")
st.header("Race Analysis")

with st.sidebar:
    st.subheader("Session")
    year =st.number_input("Year", min_value=2018,max_value=2026,value=2026)
    race=st.text_input("Race", value="Interlagos")
    sessiontype = st.selectbox("Session Type", ["Q","R"])
    load= st.button("Load Session", use_container_width=True)
if load:

    try:
        with st.spinner("Loading race data"):
            session= get_session(year,race, sessiontype)

        st.session_state['session']=session
        st.session_state['year']= year
        st.session_state['race'] = race
        st.session_state['session_type'] = sessiontype
    except Exception as e:
        st.session_state.pop('session', None)
        st.error(f"Error: {e}")

if 'session' in st.session_state:
    session= st.session_state['session']
    year = st.session_state['year']
    race = st.session_state['race']
    sessiontype = st.session_state['session_type']
    st.caption(f"{race} {year} / {sessiontype}")

    drivers= session.results['Abbreviation'].dropna().unique().tolist()
    if len(drivers) < 2:

        st.write("Add more drivers")
    else:
        with st.sidebar:
            selected = st.multiselect(
                "Drivers",
                drivers,
                default=drivers[:min(3, len(drivers))],
                max_selections= 10)
        if selected:
            tab1,tab2,tab3 =st.tabs(
                ["Pace and Tires", "Strategy", "Race/quali data"])

            with tab1:
                if sessiontype =="R":
                    for driver in selected:
                        st.subheader(driver)
                        col1, col2 = st.columns(2)

                        with col1:
                            st.plotly_chart(
                                charts.racepace_chart(session,driver),
                                use_container_width=True)
                            st.plotly_chart(
                                charts.tiredeg_chart(session,driver),
                                use_container_width=True)
                            st.plotly_chart(
                                charts.stintsum_chart(session,driver),
                                use_container_width=True)
                        with  col2:
                            st.plotly_chart(
                                charts.compoundpace_chart(session,driver),
                                use_container_width=True)
                            st.plotly_chart(
                                charts.compoundusage_chart(session,driver),
                                use_container_width=True)
                            st.plotly_chart(
                                charts.fueleffect_chart(session,driver),
                                use_container_width=True)
                else:
                    for driver in selected:
                        st.subheader(driver)
                        col1,col2 =st.columns(2)

                        with col1:
                            st.plotly_chart(
                                charts.qualiprog_chart(session,driver),
                                use_container_width=True)
                        with col2:
                            st.plotly_chart(
                                charts.perfectlap_chart(session,driver),
                                use_container_width=True)
            with tab2:
                st.write("")
            with tab3: 
                st.write("")

            
            

    