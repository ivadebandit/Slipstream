from getdata import get_session
from analyzedata import fastest_lap
import plotly.express as px
import plotly.graph_objects as go 
from plotly.subplots import make_subplots
import pandas as pd
import fastf1.plotting

COLORS={
    'background':'#0a0a0a',
    'paper':'#111111',
    'text':'#ffffff',
    'text_secondary':'#888888',
    'grid': '#1a1a1a',
    'border':'#2a2a2a',
    'red':'#e8002d',
    'green':'#2ecc71',
    'yellow':'#ffd700',
    'purple':'#9b59b6',
    'cyan':'#00d4ff',
    'soft':'#ff3333',
    'medium':'#ffd700',
    'hard':'#ffffff',
    'inter':'#00d632',
    'wet':'#0752c1'}
# 'Arial,Arial Black,sans-serif'



def applytheme(fig, title):
    fig.update_layout(
        title=dict(text=title, font=dict(
            size=18, 
            family='sans-serif', color=COLORS['text'])),
        template='plotly_dark',
        plot_bgcolor=COLORS['background'],
        paper_bgcolor=COLORS['paper'],
        font=dict(family='sans-serif', size=13, color=COLORS['text']),
        width=900,
        height=500,
        margin=dict(l=40, r=40, t=60, b=40),
        hoverlabel=dict(bgcolor="black", font_size=13, font_family="Arial"),
        
        xaxis=dict(
            gridcolor=COLORS['grid'], zerolinecolor=COLORS['grid'], 
            linecolor=COLORS['border']),
        yaxis=dict(
            gridcolor=COLORS['grid'],zerolinecolor=COLORS['grid'],
            linecolor=COLORS['border']),
        legend=dict(bgcolor=COLORS['paper'], bordercolor=COLORS['border'],borderwidth=1,font=dict(size=12)))
    return fig


def getcolor(session, driver_code):
    try:
        return fastf1.plotting.get_driver_color(driver_code, session)
    except:
        return COLORS['text_secondary']

def teamcolor(session, team_name):
    try:
        return fastf1.plotting.get_team_color(team_name,session)
    except:
        pass
    fallbacks={
        'Red Bull Racing': '#3671C6',
        'Red Bull': '#3671C6',
        'Ferrari': '#E8002D',
        'Mercedes': '#27F4D2',
        'McLaren': '#FF8000',
        'Aston Martin': '#229971',
        'Alpine': '#FF87BC',
        'Renault': '#FFF500',
        'Williams': '#64C4FF',
        'Racing Bulls': '#6692FF',
        'AlphaTauri': '#5C37A3',
        'Toro Rosso': '#1E3D61',
        'Haas F1 Team': '#B6BABD',
        'Haas': '#B6BABD',
        'Kick Sauber': '#52E252',
        'Alfa Romeo': '#C92D4B',
        'Sauber': '#C92D4B',
        'Racing Point': '#F596C8',
        'Force India': '#FF80C7',
        'Audi': '#F50537',
        'Cadillac': '#CCCCCC',}
    return fallbacks.get(team_name, COLORS['text_secondary'])



def fastestlap_chart(session, drivers):
    times = []
    colors=[]
    for driver in drivers:
        times.append(fastest_lap(session,driver))
        colors.append(getcolor(session,driver))
    
    
    fig = px.bar(x=drivers,y=times)

    fig.update_traces(marker_color=colors)
    fig.update_xaxes(title_text='Driver')
    fig.update_yaxes(title_text='Lap Time')
    return applytheme(fig, 'Fastest Lap Comparison')



from analyzedata import fastestoverall

def fastestoverall_chart(session):
    
    data = fastestoverall(session)
    sectors = ['S1', 'S2', 'S3', 'Total']
    best = [data['overall']['s1'],data['overall']['s2'], data['overall']['s3'], data['overall']['lap']]
    actual =[data['lap']['s1'], data['lap']['s2'],data['lap']['s3'],data['lap']['lap']]


    fig = go.Figure()
    fig.add_trace(go.Bar(x=sectors, y=best, name='Theoretical Best',marker_color=COLORS['cyan']))
    fig.add_trace(go.Bar(x=sectors,y=actual,name='Actual Best',marker_color=COLORS['yellow']))
    fig.update_xaxes(title_text='Sector')
    fig.update_yaxes(title_text='Lap Time')
    return applytheme(fig, 'Fastest Overall Sector by Sector')





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
    
    color=getcolor(session,driver)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x = lapnumbers,
        y = laptimes,
        mode='lines+markers',
        line=dict(color=color)))
    fig.add_hrect(
        y0= mean - std,
        y1 = mean +std,
        fillcolor='gray',
        opacity=0.2,
        line_width = 0 )
    fig.add_hline(
        y=mean,
        line_dash= 'dash',
        line_color = 'white')
    fig.update_xaxes(title_text='Lap')
    fig.update_yaxes(title_text='Lap Time')
    return applytheme(fig, f'{driver} Consistency')



from analyzedata import quali_progress

def qualiprog_chart(session, driver):


    data = quali_progress(session, driver)
    color= getcolor(session,driver)
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
        mode = 'lines+markers',
        marker= dict(size = 12 ),
        line = dict(color=color, width = 3),
        name=driver ))


    fig.update_layout(
        xaxis_title = 'Qualifying Session',
        yaxis_title = 'Lap Times',
        template = 'plotly_dark' )
    return applytheme(fig, f'{driver} Qualifying Progress')


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
        marker = dict(size=12),
        name=driver ))

    fig.update_yaxes(autorange = 'reversed', title_text='Position', dtick=1)
    fig.update_xaxes(title_text = 'Year', dtick=1)

    return applytheme(fig, f'{driver} Qualifying Results at {circuit}')




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
    return applytheme(fig, f'{driver} Race Results at {circuit}')


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
    
    
    fig.update_xaxes(title_text='Year', dtick=1)
    
    fig.update_yaxes(title_text='Lap Time')
    return applytheme(fig, f'{driver} Best Qualifying Laps at {circuit}')




def fastestalltime_chart(circuits, years):

    from analyzedata import fastest_all_time

    times =[]
    names=[]

    for i in circuits:    
        data = fastest_all_time(i,years)

        names.append(i)
        times.append(data['time'])
    
    fig= px.bar(x=names,y=times)

    colors=[COLORS['red'], COLORS['cyan'], COLORS['yellow'], 
            COLORS['green'], COLORS['purple']]
    bar_colors=[colors[i % len(colors)] for i in range (len(names))]
    fig.update_traces(marker_color=bar_colors)

    fig.update_xaxes(title_text='Circuit')
    fig.update_yaxes(title_text='Fastest Lap')
    return applytheme(fig, 'Fastest Lap All Time')




def driverstandings_chart(year, races,session):
    from analyzedata import driverstandings
    data= driverstandings(year,races)

    standings = sorted(data.items(), key=lambda x:x[1], reverse=True)
    drivers=[]
    points=[]
    colors=[]


    for driver, pointss in standings:
        drivers.append(driver)
        points.append(pointss)
        colors.append(getcolor(session,driver))

    fig=px.bar(x=drivers, y=points)
    fig.update_traces(marker_color=colors)
    fig.update_xaxes(title_text='Driver')
    fig.update_yaxes(title_text='Points')

    return applytheme(fig, f'{year} Driver Standings')





def teamstandings_chart(year,races,session):

    from analyzedata import teamstandings
    data=teamstandings(year,races)

    standings=sorted(data.items(),key=lambda x: x[1], reverse=True)
    teams=[]
    points=[]
    colors=[]

    for team, pts in standings:
        teams.append(team)
        points.append(pts)
        colors.append(teamcolor(session,team))

    fig= px.bar(x=teams, y=points)
    fig.update_traces(marker_color=colors)
    fig.update_xaxes(title_text='Team')
    fig.update_yaxes(title_text='Points')
    return applytheme(fig, f'{year} Constructor Standings')






def boxboxchart(session):
    from analyzedata import boxbox
    data=boxbox(session)


    drivers=[]
    length=[]
    laps=[]
    colors=[]

    for box in data:
        drivers.append(box['driver'])
        length.append(round(box['duration'],2))
        laps.append(box['lap'])
        colors.append(getcolor(session, box['driver']))


    fig=px.bar(x=drivers, y=length)
    fig.update_traces(marker_color=colors)
    fig.update_xaxes(title_text='driver')
    fig.update_yaxes(title_text='duration')

    return applytheme(fig, 'Pit Stop Durations')



from analyzedata import racepace

def racepace_chart(session,driver):
    data= racepace(session,driver)

    stints =list(data.keys())
    laptimes=list(data.values())

    
    tyre_colors= {
        'SOFT': COLORS['soft'],
        'MEDIUM': COLORS['medium'],
        'HARD': COLORS['hard'],
        'INTERMEDIATE': COLORS['inter'],
        'WET': COLORS['wet']}
    colors = []
    laps = session.laps[session.laps['Driver'] ==driver]

    for stint in stints:
        stintlaps = laps[laps['Stint']==stint]
        if not stintlaps.empty:
            compound = stintlaps.iloc[0]['Compound']
            colors.append(tyre_colors.get(compound, COLORS['text_secondary']))
        else:
            colors.append(COLORS['text_secondary'])

    fig =px.bar(x=stints, y=laptimes)
    fig.update_traces(marker_color=colors)
    fig.update_xaxes(title_text='Stint', dtick=1)
    fig.update_yaxes(title_text='Average Lap Time')
    return applytheme(fig, f'{driver} Average Lap Time per Stint')






def tiredeg_chart(session,driver):
    from analyzedata import tiredeg

    data=tiredeg(session,driver)

    stints=[]
    degs=[]
    compounds=[]

    tyre_colors= {
        'SOFT': COLORS['soft'],
        'MEDIUM': COLORS['medium'],
        'HARD': COLORS['hard'],
        'INTERMEDIATE': COLORS['inter'],
        'WET': COLORS['wet']}



    for stint in data:
        stints.append(stint['stint'])
        degs.append(stint['deg'])
        compounds.append(stint['compound'])

    colors=[tyre_colors.get(c, COLORS['text_secondary']) for c in compounds]

    fig=px.bar(x=stints, y=degs)
    fig.update_traces(marker_color=colors)
    fig.update_xaxes(title_text='Stint', dtick=1)
    fig.update_yaxes(title_text='Degradation (s/lap)')
    return applytheme(fig, f'{driver} Tire Degradation')





def teammategappace_chart(session,d1,d2):
    from analyzedata import teammategap_pace
    data= teammategap_pace(session,d1,d2)
    drivers = [d1,d2]

    paces = [data['pace1'],data['pace2']]

    colors=[getcolor(session,d1), getcolor(session,d2)]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=drivers,y=paces, marker_color=colors))

    fig.update_xaxes(title_text='Driver')
    fig.update_yaxes(title_text='Average Race Pace')
    return applytheme(fig, f'{d1} vs {d2} Race Pace')




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
    fig.add_trace(go.Scatter(
        x=laps,y=bests,mode='markers',
        name='Session Best', marker=dict(color=COLORS['red'], size=5)))
    fig.update_xaxes(title_text='Lap')
    fig.update_yaxes(title_text='Lap Time (s)')

    return applytheme(fig, 'Track Evolution')




def drszones_chart(session,driver):

    from analyzedata import drs_zones
    data=drs_zones(session,driver)

    telemetry=data['telemetry']
    zones=data['zones']
    # color=getcolor(session,driver)

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

    fig.update_xaxes(title_text='Distance (m)')
    fig.update_yaxes(title_text='Speed')
    return applytheme (fig, 'DRS Zones')



def h2h_chart(races, d1,d2, years,session):
    from analyzedata import h2h
    data =h2h(d1,d2, races,years)
    circuits = list(data.keys())

    d1wins=[]
    d2wins=[]

    for circuit in circuits: 
        d1wins.append(data[circuit]['d1_wins'])
        d2wins.append(data[circuit]['d2_wins'])

    fig=go.Figure()

    fig.add_trace(go.Bar(x=circuits, y=d1wins,name=d1,marker_color=getcolor(session,d1)))
    fig.add_trace(go.Bar(x=circuits,y=d2wins,name=d2,marker_color=getcolor(session,d2)))
    fig.update_xaxes(title_text='Circuit')
    fig.update_yaxes(title_text='Qualifying Wins')
    return applytheme(fig, f'{d1} vs {d2} Head to Head')



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
    fig.add_trace(go.Bar(x=drivers2,y=wetpos, name='wet', marker_color=COLORS['cyan']))
    fig.add_trace(go.Bar(x=drivers2,y=drypos,name='dry',marker_color=COLORS['red']))

    fig.update_xaxes(title_text='Driver')
    fig.update_yaxes(autorange= 'reversed',title_text='Average Position', dtick=1)
    return applytheme(fig, 'Wet vs Dry Performance')





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
            colors.append(COLORS['cyan'])
        else:
            colors.append(COLORS['yellow'])

    fig=go.Figure()
    fig.add_trace(go.Bar(x=circuits,y=gaps, name='Qualifying Gap', marker_color=colors))
    fig.update_xaxes(title_text='Race')
    fig.update_yaxes(title_text='Gap (s)')
    return applytheme(fig, f'{d1} (Cyan) vs {d2} (Yellow) Qualifying Gap')






def championshipbattle_chart(year,races,session):
    from analyzedata import championship_battle
    data = championship_battle(year,races)

    drivers = list(data[0]['scores'].keys())
    fig=go.Figure()

    for driver in drivers:
        points=[]
        for entry in data:
            points.append(entry['scores'][driver])

        color=getcolor(session,driver)
        fig.add_trace(go.Scatter(

            x=races,
            y=points,
            mode='lines+markers',
            name=driver,
            marker=dict(size=6,color=color),
            line=dict(width=2, color=color)))
        
    fig.update_xaxes(title_text='Race')
    fig.update_yaxes(title_text='Points')
    return applytheme(fig, f'{year} Championship Battle')


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
        line=dict(color=COLORS['cyan'], width=2)))
    fig.add_hline(y=0, line_dash='dash', line_color='white')


    fig.update_xaxes(title_text='Lap %')
    fig.update_yaxes(title_text=f'Delta (s), negative = {d1} ahead')
    return applytheme(fig, f'{d1} vs {d2} Delta')





def perfectlap_chart(session,driver):
    from analyzedata import perfectlap
    data=perfectlap(session,driver)


    sectors =['S1','S2','S3']
    best=[data['s1']['best'],   data['s2']['best'],  data['s3']['best']]
    actual=[data['s1']['actual'], data['s2']['actual'], data['s3']['actual']]

    fig=go.Figure()
    fig.add_trace(go.Bar(x=sectors, y=best, name='Best Possible',marker_color=COLORS['green']))
    fig.add_trace(go.Bar(x=sectors,y=actual, name='Actual Fastest',marker_color=getcolor(session,driver)))
    fig.update_xaxes(title_text='Sector')
    fig.update_yaxes(title_text='Time')
    fig.update_layout(barmode='group')

    return applytheme(fig, f'{driver} Perfect Lap Breakdown')







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
            colors.append(COLORS['green'])
        else:
            colors.append(COLORS['red'])

    fig=go.Figure()
    fig.add_trace(go.Bar(x=drivers, y=changes, marker_color=colors))
    fig.update_xaxes(title_text='Driver')
    fig.update_yaxes(title_text='Positions Gained/Lost')
    return applytheme(fig, 'Lap 1 Position Changes')



def fueleffect_chart(session, driver):

    from analyzedata import fuel_effect
    data = fuel_effect(session,driver)

    stints=[]
    rates=[]

    for stint in data:
        stints.append(stint)
        rates.append(data[stint]['fuel_effect'])

   
    tyre_colors= {
        'SOFT': COLORS['soft'],
        'MEDIUM': COLORS['medium'],
        'HARD': COLORS['hard'],
        'INTERMEDIATE': COLORS['inter'],
        'WET': COLORS['wet']} 

    colors=[]
    laps = session.laps[session.laps['Driver']==driver]
    for stint in stints:
        stintlaps=laps[laps['Stint'] == stint]
        if not stintlaps.empty:
            compound=stintlaps.iloc[0]['Compound']
            colors.append(tyre_colors.get(compound, COLORS['text_secondary']))
        else:
            colors.append(COLORS['text_secondary'])
    
    fig = px.bar(x=stints, y=rates)
    fig.update_traces(marker_color=colors)
    fig.update_xaxes( title_text='Stint', dtick=1)
    fig.update_yaxes(title_text='Time Gain Per Lap')
    fig.update_layout(template='plotly_dark')
    return applytheme(fig, f'{driver} Fuel Impact per Stint')





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

    c1 = getcolor(session,d1)
    c2=getcolor(session,d2)
    opacity2 = 0.5 if c1==c2 else 1.0

    fig=go.Figure()
    fig.add_trace(go.Bar(x=checkpoints, y=d1_positions, name=d1,marker_color=c1))
    fig.add_trace(go.Bar(x=checkpoints, y=d2_positions, name=d2,marker_color=c2, opacity=opacity2))
    success = 'Success' if box['success'] else 'Fail'

    fig.update_xaxes(title_text='Checkpoint')
    fig.update_yaxes(autorange='reversed', title_text='Position',dtick=1)
    fig.update_layout(barmode='group')

    return applytheme(fig, f'{d1} Undercut vs {d2}, ({success})')

    



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

    
    c1 = getcolor(session,d1)
    c2=getcolor(session,d2)
    opacity2 = 0.5 if c1==c2 else 1.0

    fig = go.Figure()
    fig.add_trace(go.Bar(x=checkpoints, y=d1_pos, name=d1, marker_color=c1))
    fig.add_trace(go.Bar(x=checkpoints, y=d2_pos, name=d2,marker_color=c2, opacity=opacity2))

    success= 'Success' if box['success'] else 'Fail'
    fig.update_xaxes(title_text='Checkpoint')
    fig.update_yaxes(autorange='reversed', title_text='Position', dtick=1)

    fig.update_layout(barmode='group')
    return applytheme(fig, f'{d1} Overcut vs {d2} ({success})')






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
    fig.add_trace(go.Bar(x=drivers, y=wins, name='Wins',marker_color=COLORS['yellow']))
    fig.add_trace(go.Bar(x=drivers,y=podiums,name='Podiums',marker_color=COLORS['cyan']))
    fig.add_trace(go.Bar(x=drivers,y=poles,name='Poles',marker_color=COLORS['red']))
    fig.update_xaxes(title_text='Driver')
    fig.update_yaxes(title_text='Count')
    fig.update_layout(barmode='group')
    return applytheme(fig, 'Career Stats')




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
        marker_color=[COLORS['green'], COLORS['red'], 'white']))

    fig.update_xaxes(title_text='Stat')
    fig.update_yaxes(title_text='Position', dtick=1)
    return applytheme(fig, f'{driver} Results at {circuit}')



def positionsgained_chart(session):

    from analyzedata import positionsgained
    data=positionsgained(session)
    sorteddata = sorted(data, key=lambda x:x['gain'], reverse=True)

    drivers=[]
    gains=[]
    colors=[]

    for entry in sorteddata:
        drivers.append(entry['driver'])
        gains.append(entry['gain'])
        if entry['gain'] >=0:
            colors.append(COLORS['green'])
        else:
            colors.append(COLORS['red'])


    fig=go.Figure()
    fig.add_trace(go.Bar(x=drivers, y=gains, marker_color=colors))
    fig.update_xaxes(title_text='Driver')
    fig.update_yaxes(title_text='Positions Gained')
    return applytheme(fig, 'Positions Gained/Lost')



def stintsum_chart(session, driver):
    from analyzedata import stintsum
    data = stintsum(session, driver)

    stints = []
    for lap in data:
        if lap['stint'] not in stints:
            stints.append(lap['stint'])

    tyre_colors = {
        'SOFT': COLORS['soft'],
        'MEDIUM': COLORS['medium'],
        'HARD': COLORS['hard'],
        'INTERMEDIATE': COLORS['inter'],
        'WET': COLORS['wet']}

    fig = go.Figure()
    for stint in stints:
        laps = []
        times = []
        compound = ""
        for lap in data:
            if lap['stint'] == stint:
                laps.append(lap['lap'])
                times.append(lap['lap_time'])
                compound = lap['compound']

        color = tyre_colors.get(compound, COLORS['text_secondary'])
        fig.add_trace(go.Scatter(
            x=laps,
            y=times,
            mode='lines+markers',
            name=f'Stint {stint} ({compound})',
            line=dict(color=color, width=2),
            marker=dict(color=color)))

    fig.update_xaxes(title_text='Lap Number')
    fig.update_yaxes(title_text='Lap Time')
    return applytheme(fig, f'{driver} Lap Times by Stint')



def compoundusage_chart(session,driver):

    from analyzedata import compound_usage
    data =compound_usage(session,driver)
    fig=go.Figure()

    tyre_colors={
        'SOFT': COLORS['soft'],
        'MEDIUM':COLORS['medium'],
        'HARD':COLORS['hard'],
        'INTERMEDIATE': COLORS['inter'],
        'WET':COLORS['wet']}

    for stint in data:
        fig.add_trace(go.Bar(
            y=[f"stint {stint['stint']}"],
            x=[stint['laps']],
            base=[stint['start_lap']],
            orientation='h',
            name=stint['compound'],
            marker_color=tyre_colors.get(stint['compound'], COLORS['text_secondary']),
            text=f"{stint['compound']} ({stint['laps']} laps)",
            textposition='inside'))
    fig.update_xaxes(title_text='Lap Number')
    fig.update_yaxes(autorange='reversed', title_text='Stint')
    return applytheme(fig, f'{driver} Tyre Strategy')







def compoundpace_chart(session,driver):
    from analyzedata import compound_pace
    data=compound_pace(session,driver)

    compounds=[]
    averages=[]
    fastests=[]
    slowests=[]

    for entry in data:
        compounds.append(entry['compound'])
        averages.append(entry['average'])
        fastests.append(entry['fastest'])
        slowests.append(entry['slowest'])


    tyre_colors = {
        'SOFT': COLORS['soft'],
        'MEDIUM': COLORS['medium'],
        'HARD': COLORS['hard'],
        'INTERMEDIATE': COLORS['inter'],
        'WET': COLORS['wet']}

    colors = [tyre_colors.get(c,COLORS['text_secondary']) for c in compounds]
    fig = go.Figure()
    

    fig.add_trace(go.Bar(x=compounds,y=averages,name='Average',marker_color=colors))
    fig.add_trace(go.Bar(x=compounds,y=fastests,name='Fastest',marker_color=colors, opacity=0.7))
    fig.add_trace(go.Bar(x=compounds,y=slowests,name='Slowest',marker_color=colors,opacity=0.4))

    fig.update_xaxes(title_text='Compound')
    fig.update_yaxes(title_text='Lap Time')
    fig.update_layout(barmode='group')
    return applytheme(fig, f'{driver} Pace by Compound')





def positionprogress_chart(session,driver):

    from analyzedata import position_progress
    data =position_progress(session,driver)

    laps=[]
    positions=[]

    for entry in data:
        laps.append(entry['lap'])
        positions.append(entry['position'])

    fig= go.Figure()
    fig.add_trace(go.Scatter(
        x=laps,
        y=positions, 
        mode='lines+markers',
        name=driver,
        marker=dict(size=6),
        line=dict(width=2, color=getcolor(session,driver))))

    fig.update_xaxes(title_text='Lap')
    fig.update_yaxes(autorange='reversed', title_text='Position',dtick=1)
    return applytheme(fig, f'{driver} Position Progress')