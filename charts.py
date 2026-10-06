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






def consistency_chart(session, driver):

    laps=session.laps
    filter = laps[laps['Driver']==driver]
    filter=filter[filter['IsAccurate']==True]
    filter=filter[filter['Deleted']==False]
    filter=filter[filter['TrackStatus']=='1']
    filter=filter[filter['LapTime'].notna()]

    filter = filter.copy()
    filter['seconds'] = filter['LapTime'].dt.total_seconds()

    lapnumbers = filter['LapNumber'].tolist()
    laptimes = filter['seconds'].tolist()
    mean = sum(laptimes) / len(laptimes)
    std = filter['seconds'].std()
    


    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x = lapnumbers,
        y = laptimes,
        mode='lines+markers',
        line=dict(color='pink') ))
    fig.add_hrect(
        y0= mean - std,
        y1 = mean +std,
        fillcolor='blue',
        opacity=0.33,
        line_width = 0 )
        #annotation_text = '+- 1 std',
        #annotation_position = 'top left' )
   
    fig.add_hline(
        y=mean,
        line_dash= 'dash',
        line_color = 'red'
    )

    fig.update_layout(
        title= f'{driver} consistency',
        
        xaxis_title = 'lap',
        yaxis_title = 'laptime',
        template='plotly_dark')
    return fig







from analyzedata import quali_progress

def qualiprog_chart(session, driver):


    data = quali_progress(session, driver)
    parts = []
    times = []

    if data['q1'] is not None:
        parts.append('Q1')
        times.append(data['q1'])
    if data['q2'] is not None:
        parts.append('Q2')
        times.append(data['q2'])
    if data['q3'] is not None:
        parts.append('Q3')
        times.append(data['q3'])

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=parts,
        y=times,
        mode = 'lines + markers',
        marker= dict(size = 12 ),
        line = dict(color='cyan', width = 3),
        name=driver ))


    fig.update_layout(
        title=f'{driver} quali progress ',
        xaxis_title = 'qualifying session',
        yaxis_title = 'lap times',
        template = 'plotly_dark' )
    return fig