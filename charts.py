from getdata import get_session
from analyzedata import fastest_lap
import plotly.express as px
import plotly.graph_objects as go 
from plotly.subplots import make_subplots
import pandas as pd





def fastestlap_chart(session, drivers):
    times = []
    for driver in drivers:
        time = fastest_lap(session,driver)
        times.append(time)
    
    
    fig = px.bar(x=drivers,y=times, title='fastest lap')
    fig.update_xaxes(title_text='driver')
    fig.update_yaxes(title_text='lap time')
    return fig