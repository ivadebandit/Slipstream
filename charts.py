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



from analyzedata import qualipositions 


def chart_qualipositions(driver, circuit, years):
    data = qualipositions(driver, circuit, years)
    
    yearslist = list(data.keys())
    positions = list(data.values())
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=yearslist,
        y=positions,
        mode = 'lines+markers',
        marker = dict(size=14),
        name=driver ))

    fig.update_yaxes(autorange = 'reversed', title_text='position', dtick=1)
    fig.update_xaxes(title_text = 'year', dtick=1)
    fig.update_layout(
        title= f'{driver} quali results at {circuit}',
        template= 'plotly_dark' )
    return fig




def racepositions_chart(driver, circuit,years):
    from analyzedata import racepositions

    data = racepositions(driver, circuit,years)
    races = list(data.keys())
    positions=list(data.values())

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=races,
        y=positions,
        mode='lines+markers',
        marker=dict(size=13),
        name=driver ))

    fig.update_yaxes(autorange= 'reversed', title_text='Position', dtick=1)
    fig.update_xaxes(title_text='Year', dtick=1)
    fig.update_layout(
        title=f'{driver} race results at {circuit}',
        template='plotly_dark' )
    return fig



def bestlapsq_chart(driver,circuit,years):

    from analyzedata import bestlaps_quali
    data = bestlaps_quali(driver, circuit,years)

    yearss = list(data.keys())
    times = list(data.values())

    fig= go.Figure()
    fig.add_trace(go.Scatter(
        x=yearss,
        y=times,
        mode='lines+markers',
        marker=dict(size=12),
        name=driver))
    
    
    fig.update_xaxes(title_text='year', dtick=1)
    
    fig.update_yaxes(title_text='laptime')
    fig.update_layout(
        title= f'{driver} best quali laps at {circuit}',
        template= 'plotly_dark')

    fig.show()



def fastestalltime_chart(circuits, years):

    from analyzedata import fastest_all_time

    times =[]
    names=[]

    for i in circuits:    
        data = fastest_all_time(i,years)

        names.append(i)
        times.append(data['time'])
    fig= px.bar(x=names,y=times, title='fastest lap all time')
    fig.update_xaxes(title_text='circuit')
    fig.update_yaxes(title_text='fastest lap')
    return fig




def driverstandings_chart(year, races):
    from analyzedata import driverstandings
    data= driverstandings(year,races)

    standings = sorted(data.items(), key=lambda x:x[1], reverse=True)
    top10 = standings[:10]

    drivers=[]
    points=[]
    for driver, pointss in top10:
        drivers.append(driver)
        points.append(pointss)
    fig=px.bar(x=drivers, y=points, title='driver standings (top 10)')
    fig.update_xaxes(title_text='Driver')
    fig.update_yaxes(title_text='points')

    return fig




def teamstandings_chart(year,races):

    from analyzedata import teamstandings
    data=teamstandings(year,races)

    standings=sorted(data.items(),key=lambda x: x[1], reverse=True)
    teams=[]
    points=[]
    for team, pts in standings:
        teams.append(team)
        points.append(pts)

    fig= px.bar(x=teams, y=points, title='constructor standings')
    fig.update_xaxes(title_text='team')
    fig.update_yaxes(title_text='points')
    return fig






def boxboxchart(session):
    from analyzedata import boxbox
    data=boxbox(session)


    drivers=[]
    length=[]
    laps=[]

    for box in data:
        drivers.append(box['driver'])
        length.append(round(box['duration'],2))
        laps.append(box['lap'])


    fig=px.bar(x=drivers, y=length, title='pitstop durations')
    fig.update_xaxes(title_text='driver')
    fig.update_yaxes(title_text='duration')

    return fig



from analyzedata import racepace

def racepace_chart(session,driver):
    data= racepace(session,driver)

    stints =list(data.keys())
    laptimes=list(data.values())
    fig =px.bar(x=stints, y=laptimes,title=f'{driver} race pace')
    fig.update_xaxes(title_text='stint', dtick=1)
    fig.update_yaxes(title_text='average laptime',template= 'plotly_dark')
    return fig






def tiredeg_chart(session,driver):
    from analyzedata import tiredeg

    data=tiredeg(session,driver)

    stints=[]
    degs=[]
    compounds=[]


    for stint in data:
        stints.append(stint['stint'])
        degs.append(stint['deg'])
        compounds.append(stint['compound'])

    fig=px.bar(x=stints, y=degs,title=f'{driver} tire degradation per stint')
    fig.update_xaxes(title_text='stint', dtick=1)
    fig.update_yaxes(title_text='degradation')
    return fig






def teammategappace_chart(session,d1,d2):
    from analyzedata import teammategap_pace
    data= teammategap_pace(session,d1,d2)
    drivers = [d1,d2]

    paces = [data['pace1'],data['pace2']]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=drivers,y=paces, name ='avg pace'))

    fig.update_layout(
        title='pace diff between two drivers',
        xaxis_title='driver',
        yaxis_title='pace',
        template='plotly_dark' )
    return fig





def trackevo_chart(session):
    from analyzedata import trackevo
    data=  trackevo(session)

    laps=[]
    bests=[]
    times=[]

    for d in data:
        laps.append(d['lap'])
        times.append(d['time'])
        bests.append(d['best'])

    fig=go.Figure()
    #fig.add_trace(go.Scatter(x=laps,y=times, mode='markers',name='laptime', line=dict(
     #   color='gray',width=1)))
    fig.add_trace(go.Scatter(x=laps,y=bests,mode='markers',name='session best',line=dict(
        color='red', width=1.7)))
    fig.update_layout(
        title='track evolution',
        xaxis_title='lap',
        yaxis_title='lap time',
        template='plotly_dark')

    return fig




def drszones_chart(session,driver):

    from analyzedata import drs_zones
    data=drs_zones(session,driver)

    telemetry=data['telemetry']
    zones=data['zones']

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=telemetry['Distance'],
        y=telemetry['Speed'],
        mode='lines',
        name='speed',
        line=dict(color='white', width=2)))

    for zone in zones:

        fig.add_vrect(
            x0=zone['start'],
            x1=zone['end'],
            fillcolor='lightgreen',
            opacity=0.4,
            line_width=0)

    fig.update_layout(
        title=f'{driver} drs zones on speed trace',
        xaxis_title='distance',
        yaxis_title= 'speed',
        template='plotly_dark')
    return fig

#  check for 2026 in docs!!



def h2h_chart(races, d1,d2, years):
    from analyzedata import h2h
    data =h2h(d1,d2, races,years)
    circuits = list(data.keys())

    d1wins=[]
    d2wins=[]

    for circuit in circuits: 
        d1wins.append(data[circuit]['d1_wins'])
        d2wins.append(data[circuit]['d2_wins'])

    fig=go.Figure()
    fig.add_trace(go.Bar(x=circuits, y=d1wins,name=d1))
    fig.add_trace(go.Bar(x=circuits,y=d2wins,name=d2))
    fig.update_layout(
        title=f'{d1} vs {d2} h2h',
        xaxis_title='circuit',
        yaxis_title='qualifying wins',
        barmode='group',
        template='plotly_dark')
    return fig




def wetdrycomp_chart(races,drivers):
    from analyzedata import wetdrycomp

    data=wetdrycomp(races,drivers)
    drivers2 = []
    wetpos =[]
    drypos=[]

    for driver in drivers:
        if driver in data:
            drivers2.append(driver)
            wetpos.append(data[driver]['wet'])
            drypos.append(data[driver]['dry'])

    fig = go.Figure()
    fig.add_trace(go.Bar(x=drivers2,y=wetpos, name='wet'))
    fig.add_trace(go.Bar(x=drivers2,y=drypos,name='dry'))

    fig.update_layout(
        title='wet  vs dry performance',
        xaxis_title='driver',
        yaxis_title='avg position',
        barmode='group',
        template='plotly_dark')

    fig.update_yaxes(autorange= 'reversed', dtick=1)
    return fig





def teammategapquali_chart(d1,d2,races,years):
    from analyzedata import teammategap_quali
    data=teammategap_quali(d1,d2,races,years)

    circuits=[]
    gaps=[]
    colors=[]
    for entry in data:
        circuits.append(f"{entry['event']} {entry['year']}")
        gaps.append(entry['gap'])

        if entry['faster'] == d1:
            colors.append('blue')
        else:
            colors.append('red')

    fig=go.Figure()
    fig.add_trace(go.Bar(x=circuits,y=gaps, name='quali gap', marker=dict(color=colors)))
    fig.update_layout(
        title=f'{d1} (blue) vs {d2} (red) quali difference',
        xaxis_title='race',
        yaxis_title='gap',
        template='plotly_dark')
    return fig





def championshipbattle_chart(year,races):
    from analyzedata import championship_battle
    data = championship_battle(year,races)

    drivers = list(data[0]['scores'].keys())
    fig=go.Figure()

    for driver in drivers:
        points=[]
        for entry in data:
            points.append(entry['scores'][driver])
        fig.add_trace(go.Scatter(

            x=races,
            y=points,
            mode='lines+markers',
            name=driver,
            marker=dict(size=6),
            line=dict(width=2)))
    fig.update_layout(
        title=f'{year} drivers standings',
        xaxis_title='race',
        yaxis_title='points',
        template='plotly_dark')
        #height=600 )
    return fig



def delta_chart(d1,d2,session):
    
    from analyzedata import delta
    data=delta(d1,d2,session)

    pcts=[]
    deltas=[]

    for entry in data:
        pcts.append(entry['distance'])
        deltas.append(entry['delta'])

    fig=go.Figure()
    fig.add_trace(go.Scatter(
        x=pcts,
        y=deltas,
        mode='lines',
        name=f'{d1} vs {d2}',
        line=dict(color='cyan', width=2)))
    fig.add_hline(y=0, line_dash='dash', line_color='white')


    fig.update_layout(
        title=f'{d1} vs {d2} delta',
        xaxis_title='lap %',
        yaxis_title=f'delta, negative = {d1} ahead',
        template='plotly_dark')
    return fig






def perfectlap_chart(session,driver):
    from analyzedata import perfectlap
    data=perfectlap(session,driver)


    sectors =['S1','S2','S3']
    best=[data['s1']['best'],   data['s2']['best'],  data['s3']['best']]
    actual=[data['s1']['actual'], data['s2']['actual'], data['s3']['actual']]

    fig=go.Figure()
    fig.add_trace(go.Bar(x=sectors, y=best, name='best possible'))
    fig.add_trace(go.Bar(x=sectors,y=actual, name='actual fastest'))
    fig.update_layout(
        title=('perfect lap vs actual fastest'),
        xaxis_title='sector',
        yaxis_title='time',
        barmode='group',
        template='plotly_dark')
    
    return fig







def lap1start_chart(session):

    from analyzedata import lap1start
    data=lap1start(session)

    sortedd = sorted(data, key=lambda x: x['change'], reverse=True)
    drivers=[]
    changes=[]
    colors=[]

    for entry in sortedd:
        drivers.append(entry['driver'])
        changes.append(entry['change'])

        if entry['change'] >=0:
            colors.append('lightgreen')
        else:
            colors.append('red')

    fig=go.Figure()
    fig.add_trace(go.Bar(x=drivers, y=changes, marker=dict(color=colors)))
    fig.update_layout(
        title='position changes on lap 1',
        xaxis_title='driver',
        yaxis_title='positions gained/lost',
        template='plotly_dark')
    return fig



# journal!!!!!!!!!!!!!!!!!!!!!!!!!1!!!!!!!!!!








def fueleffect_chart(session, driver):

    from analyzedata import fuel_effect
    data = fuel_effect(session,driver)

    stints=[]
    rates=[]

    for stint in data:
        stints.append(stint)
        rates.append(data[stint]['fuel_effect'])
    fig = px.bar(x=stints, y=rates,title= f'{driver} fuel effect per stint')
    fig.update_xaxes( title_text='stint', dtick=1)
    fig.update_yaxes(title_text='time gain per lap')
    fig.update_layout(template='plotly_dark')
    return fig





def undercuteffect_chart(session, d1,d2):

    from analyzedata import undercuteffect
    data=undercuteffect(session, d1, d2)

    box = data[0]
    checkpoints=['before', 'after_d1_pit','after_d2_pit']
    d1_positions =[
        box['before']['d1'],
        box['after_d1_pit']['d1'],
        box['after_d2_pit']['d1']]
    d2_positions=[
        box['before']['d2'],
        box['after_d1_pit']['d2'],
        box['after_d2_pit']['d2']]


    fig=go.Figure()
    fig.add_trace(go.Bar(x=checkpoints, y=d1_positions, name=d1))
    fig.add_trace(go.Bar(x=checkpoints, y=d2_positions, name=d2))
    success = 'success' if box['success'] else 'fail'

    fig.update_layout(
        title=f'{d1} undercut vs {d2} - {success}',
        xaxis_title='checkpoint',
        yaxis_title='position',
        barmode='group',
        template='plotly_dark')
    fig.update_yaxes(autorange='reversed', dtick=1)

    return fig


    



def overcuteffect_chart(session, d1,d2):

    from analyzedata import overcuteffect
    data=overcuteffect(session, d1,d2)

    box = data[0]
    checkpoints =['before', 'afterd2pit', 'afterd1pit']
    d1_pos =[
        box['before']['d1'],
        box['afterd2pit']['d1'],
        box['afterd1pit']['d1']]
    d2_pos=[
        box['before']['d2'],
        box['afterd2pit']['d2'],
        box['afterd1pit']['d2']]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=checkpoints, y=d1_pos, name=d1))
    fig.add_trace(go.Bar(x=checkpoints, y=d2_pos, name=d2))

    success= 'success' if box['success'] else 'failed'
    fig.update_layout(
        title=f'{d1} overcut {d2} - {success}',
        xaxis_title='checkpoints',
        yaxis_title='position',
        barmode='group',
        template='plotly_dark')

    fig.update_yaxes(autorange='reversed', dtick=1)
    return fig
# small issue with success line in output in the title chart
# too lazy to fix now will fix later








def careerstats_chart(years,races,drivers):

    from analyzedata import wins_count, podium_count, pole_count

    wins=[]
    podiums=[]
    poles=[]
    for driver in drivers:
        wins.append(wins_count(years,races,driver))
        podiums.append(podium_count(years,races,driver))
        poles.append(pole_count(years,races, driver))


    fig =go.Figure()
    fig.add_trace(go.Bar(x=drivers, y=wins, name='wins'))
    fig.add_trace(go.Bar(x=drivers,y=podiums,name='podiums'))
    fig.add_trace(go.Bar(x=drivers,y=poles,name='poles'))

    fig.update_layout(
        title=f'{driver} stats',
        xaxis_title='driver',
        yaxis_title='count',
        barmode='group',
        template='plotly_dark')

    return fig







def finishstats_chart(driver,circuit,years):

    from analyzedata import bestfinish,worstfinish, avgfinish
    best= bestfinish(driver, circuit,years)
    worst=worstfinish(driver,circuit,years)
    avg=avgfinish(driver,circuit,years)

    labels = ['best','worst','average']

    if worst == 'DNF':
        worstval= 20
        worsttext = 'DNF'
    else:
        worstval=worst
        worsttext = f'P{worst}'

    values =[best, worstval,avg]
    textlabels= [
        f'P{best}',
        worsttext,
        f'P{avg}']

    fig=go.Figure()
    fig.add_trace(go.Bar(
        x=labels,
        y=values,
        text=textlabels,
        textposition='auto',
        marker_color=['lightgreen','red','lightblue']))

    fig.update_layout(
        title=f'{driver} results at {circuit}',
        xaxis_title='stat',
        yaxis_title='position',
        template='plotly_dark')
    fig.update_yaxes(dtick=1)
    return fig




                   