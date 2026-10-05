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



from analyzedata import fastestoverall

def fastestoverall_chart(session):
    
    data = fastestoverall(session)
    sectors = ['S1', 'S2', 'S3', 'Total']
    best = [data['overall']['s1'],data['overall']['s2'], data['overall']['s3'], data['overall']['lap']]
    actual =[data['lap']['s1'], data['lap']['s2'],data['lap']['s3'],data['lap']['lap']]


    fig = go.Figure()
    fig.add_trace(go.Bar(x=sectors, y=best, name='theoretical best'))
    fig.add_trace(go.Bar(x=sectors,y=actual,name='actual best'))
    fig.show()