"""drivers = ['ALO', 'HAM', 'BEA', 'HAD', 'LIN', 'NOR', 'VER']
drivers.sort()
print(drivers)
first, second, third = drivers[:3]
print(first, second, third)
if 'VER' in drivers:
    print(True)
laptimes = [103.33, 101.23, 102.99, 103.44]
penalty = [x + 5 for x in laptimes]
print(penalty)

drivers = ['VER', 'HAM', 'LEC']
result = drivers.sort()
print(result)
print(drivers)



drivers_teams = {
    'VER': 'Red Bull',
    'HAM':  'Ferrari',
    'LEC': 'Ferrari',
    'NOR':'McLaren',
     'ALO': 'Aston Martin' }
print(drivers_teams['VER'])
if 'HAM' in drivers_teams:
    print("true")
for driver in drivers_teams:
    print(driver)
for driver, team in drivers_teams.items():
    print(driver, team)
    print("hello")

drivers = {
    'VER': {'team': 'Red Bull', 'wins': 63},
    'HAM': {'team': 'Ferrari', 'wins': 105},
    'LEC': {'team':'Ferrari', 'wins':8},
    'NOR': {'team':'McLaren', 'wins': 5},
    'RUS': {'team': 'Mercedes', 'wins': 3} }
for driver, info in drivers.items():
    print(driver, info['team'], info['wins'])
    print
"""""""

import pandas as pd
data = {
    'driver': ['VER', 'HAM', 'LEC'],
    'team': ['Red Bull', 'Ferrari', 'Ferrari'],
    'wins': [63, 105, 8] }
df = pd.DataFrame(data)
print(df)
print(df.shape)
print(df['driver'])
print(df[['driver', 'wins']])
ferraridrivers = df[df['team'] == 'Ferrari']
print(ferraridrivers)
sortby_wins = df.sort_values('wins', ascending =False)
print(sortby_wins)
"""

"""
from getdata import get_session
import pandas as pd
session = get_session(2026, 'Netherlands', 'R')
df = session.results
print(df.head())
print(df[['Abbreviation', 'TeamName']])
ferraridriv = df[df['TeamName'] == 'Ferrari']
print(ferraridriv)

sort = df.sort_values('Points', ascending=False)
print(sort[['Abbreviation', 'TeamName', 'Points']])
"""

"""
from getdata import get_session
import pandas as pd
session = get_session(2026, 'Zandvoort', 'R')
df = session.results
ver = df[df['Abbreviation'] == 'VER']
print(ver)
print(len(df))
print(df['TeamName'].unique()) # shows all values in a column
print(df['TeamName'].value_counts()) # counts the amount of times it appears
print(df.groupby('TeamName')['Points'].mean()) # group data by something
"""
"""
from getdata import get_session
import pandas as pd
session = get_session(2026, 'Red Bull Ring', 'R')
laps = session.laps
print(laps.shape)
print(laps.head(3))
print(laps.columns)
ver_laps=laps[laps['Driver']=='VER']
print(ver_laps.head(3))

print(laps['Driver'].value_counts().head(5))
print(laps['Compound'].unique())
print(laps['LapTime'].head(5))
print(laps['IsAccurate'].value.counts())
"""
"""
from getdata import get_session
from analyzedata import clean_laps
session = get_session(2026, 'Austria', 'R')

laps = clean_laps(session, 'VER')


print(laps.head())
print(len(laps))"""



from getdata import get_session
"""
from analyzedata import raceresult

session=get_session(2026, 'Netherlands' , 'R')
res = raceresult(session)
print(res)"""


"""
from analyzedata import fastest_lap, fastestoverall
session = get_session(2026, 'Monaco', 'Q')
ver_fastest = fastest_lap(session, 'VER')
print({ver_fastest})


overall = fastestoverall(session)
print({overall})



from analyzedata import get_consistency
session = get_session(2022, 'Mexico', 'R')
ver = get_consistency(session,'VER')
print(ver)



session = get_session(2026, 'Austria', 'R')
laps = session.laps

pit_laps=laps[laps['PitInTime'].notna()]
print(pit_laps[['Driver', 'LapNumber', 'PitInTime', 'PitOutTime']])
pitout = laps[laps['PitOutTime'].notna()]
print(pitout[['Driver','LapNumber','PitInTime', 'PitOutTime']])

"""


"""
session = get_session(2026, 'Monza', 'Q')
from analyzedata import quali_progress

ver = quali_progress(session, 'VER')
print(ver)"""



"""
from analyzedata import qualipositions

ver = qualipositions('VER', 'Austria', [2022, 2023, 2024, 2025, 2026])
print(ver)
"""

"""
from analyzedata import racepositions
ver = racepositions('VER', 'Zandvoort', [2020,2021,2022,2023,2024,2025,2026])
print(ver)"""


"""
from analyzedata import bestlaps_quali
ver = bestlaps_quali('VER', 'Zandvoort', [2020, 2021,2023,2025, 2026])
print(ver)
"""


"""
from analyzedata import clean_laps
session = get_session(2023, 'Zandvoort', 'Q')
laps = clean_laps(session, 'VER')
print(len(laps))
print(laps)
"""

"""
from analyzedata import fastest_lap
session = get_session(2023, 'Zandvoort', 'Q')
fastest = fastest_lap(session, 'VER')
print(fastest)"""
"""
from analyzedata import fastest_all_time

res = fastest_all_time('Monza', [2021, 2024, 2025, 2026])
print(res)"""





"""from analyzedata import driverstandings, standingssprint, totalpoints

races = ['Zandvoort', 'Monza']
racepts = driverstandings(2026, races)

print("pts", racepts)

sprintpts= standingssprint(2026, races)
print("sprint points", sprintpts)

total = totalpoints(2026, races)
print("total", total)
"""


"""from analyzedata import  teamstandings, teamsprints, totalteams
races = ['Miami']
racepts = teamstandings(2026,races)
sprintpts= teamsprints(2026,races)
total=totalteams(2026, races)

print("points", racepts)
print("sprint points", sprintpts)


print("total", total)
"""


"""
from analyzedata import boxbox
session= get_session(2026, 'Italian Grand Prix', 'R')
pitstops = boxbox(session)
print(pitstops)"""



"""

from analyzedata import racepace

session=get_session(2026, 'Zandvoort', 'R')
pace = racepace(session,'VER')
print(pace)"""






"""from analyzedata import tiredeg
session = get_session(2026, 'Austria', 'R')
res = tiredeg(session, 'VER')
print(res)
"""

"""
from analyzedata import teammategap_pace
session = get_session(2026, 'Monza', 'R')
gap = teammategap_pace(session, 'ANT', 'RUS')
print(gap)"""

"""
from analyzedata import trackevo

session = get_session(2026, 'Madrid', 'Q')
evo = trackevo(session)
print(evo[:4])
print(evo[-4])
"""

"""
session = get_session(2025, 'Austria', 'Q')
laps = session.laps
ver = laps[laps['Driver'] == 'VER']
fastest = ver.pick_fastest()
telemetry = fastest.get_telemetry()
print(telemetry['DRS'].unique())
"""
"""
from analyzedata import drs_zones
session = get_session(2025, 'Austria', 'Q')
zones = drs_zones(session, 'VER')
print(zones)"""

"""
from getdata import get_session
from analyzedata import h2h
results = h2h('VER', 'HAM', ['Monza', 'Monaco', 'Silverstone'], [2021, 2022, 2023, 2024])
print(results)"""



"""
from analyzedata import wetdrycomp
sessions = [
    get_session(2024, 'Canada', 'R'),
    get_session(2024, 'Brazil', 'R'),
    get_session(2024, 'Brazil', 'Q'),
    get_session(2025, 'Jeddah', 'R'),
    get_session(2026, 'Austria', 'R'),
    get_session(2025, 'Monza', 'Q') ]
results = wetdrycomp(sessions, ['VER', 'HAM', 'HAD'])
print(results)"""


"""from getdata import get_session
session = get_session(2026,'Monaco', 'R')
print(session.results['Status'].unique())"""


"""
from analyzedata import reliability
races = ['Madrid']
years = 2026
res = reliability(years, races)
print(res)"""

"""
from analyzedata import championship_battle
races = ['Dutch Grand Prix', 'Monaco']
res = championship_battle(2026, races)
print(res)
"""

"""
from analyzedata import teammategap_quali
rb = teammategap_quali('HAM', 'VER', ['Monza', 'Silverstone'], [2023,2024])
print(rb)
print(" ")
print("help")
laps = session.laps
ver = laps[laps"""
"""
from analyzedata import fastest_lap, clean_laps
session = get_session(2021, 'Monza', 'Q')
print("drivers")
print(session.results['Abbreviation'].unique())
print("lap count")
laps = session.laps
ver = laps[laps['Driver'] == 'PER']
print(len(ver))
print("laptimes")
print(ver['LapTime'].head(2))
clean = clean_laps(session, 'PER')
print(len(clean))
print("fastest")
print(clean.min())
print()
print("fastest 2")
print(fastest_lap(session, 'PER'))"""





"""

from analyzedata import teammategap_quali
res = teammategap_quali('VER', 'PER', ['Monza'], [2021])
print(res)"""



"""
session = get_session(2025, 'Monza', 'Q')
laps=session.laps

ver = laps[laps['Driver'] == 'VER'].pick_fastest()
ham = laps[laps['Driver'] == 'HAM'].pick_fastest()
tel1 = ver.get_telemetry()
tel2 = ham.get_telemetry()

print("ver", len(tel1))

print("ham", len(tel2))
print(tel1[['Distance', 'Time']].head())"""


"""

from analyzedata import delta
session = get_session(2026, 'Madrid', 'Q')
delta('VER', 'ANT', session)
print(delta)

"""
"""

from getdata import get_session
from analyzedata import delta
session = get_session(2026, 'Madrid', 'Q')
res = delta('VER', 'ANT', session)
print(res[:5])
print(res[-5:])
"""

"""
from analyzedata import perfectlap
session = get_session(2026, 'Madrid', 'Q')
ver = perfectlap(session, 'VER')
print(ver)"""


"""
from analyzedata import lap1start

session = get_session(2026, '  Australia', 'R')
a = lap1start(session)
print(a)"""


"""
from analyzedata import circuit_type
print(circuit_type('Suzuka'))
print(circuit_type('Monza'))
"""


"""
from analyzedata import fuel_effect
session = get_session(2026, 'Zandvoort', 'R')
result = fuel_effect(session, 'LEC')
print(result)"""


"""
from analyzedata import undercuteffect
session = get_session(2024, 'Hungary', 'R')
res = undercuteffect(session, 'VER', 'HAM')
print(res)"""


"""
from analyzedata import overcuteffect
session = get_session(2023, 'Bahrain', 'R')
result = overcuteffect(session, 'STR', 'RUS')
print(result)"""


"""
from analyzedata import safetycar_impact
session = get_session(2026, 'Netherlands', 'R')
res = safetycar_impact(session)
print(res) """

"""
session = get_session(2026, 'Madrid', 'R')
print(session.laps['TrackStatus'].unique())"""
"""
session = get_session(2026, 'Zandvoort', 'R')
print(session.laps['TrackStatus'].unique())""" 



"""session = get_session(2024, 'Spa', 'Q')
res = session.results
print(res[res['Abbreviation'] == 'VER'][['Abbreviation', 'Position']])
race = get_session(2024, 'Spa', 'R')
raceres = race.results
print(raceres[raceres['Abbreviation'] == 'VER'][['Abbreviation', 'GridPosition']])
"""

"""
from analyzedata import wins_count, podium_count, pole_count

races = ['Bahrain', 'Jeddah', 'Melbourne', 'Suzuka', 'Imola']
print(wins_count([2024], races, 'VER'))
print(podium_count([2024], races, 'VER'))
print(pole_count([2024], races, 'VER'))"""


"""
from analyzedata import bestfinish
print(bestfinish('VER', 'Monza', [2022,2023]))"""

"""
from analyzedata import worstfinish
print(worstfinish('VER', 'Monza', [2021, 2023]))"""

"""
from analyzedata import avgfinish
print(avgfinish('VER', 'Monza', [2021,2022,2023,2024]))"""


"""
from analyzedata import fastestoverall
session = get_session(2026, 'Madrid', 'Q')
res = fastestoverall(session)
print(res)"""



"""from analyzedata import positionsgained
session = get_session(2024, 'Brazil', 'R')
res = positionsgained(session)[0]
print(res)"""


"""
from analyzedata import stintsum
session = get_session(2026, 'Madrid', 'R')
res = stintsum(session, 'HAM')
print(res[:5])
print(res[-5:])
print(len(res))"""


"""
from analyzedata import compound_usage
session = get_session(2025, 'Spain', 'R')
res = compound_usage(session, 'VER')
print(res)"""

"""

from analyzedata import compound_pace
session = get_session(2026, 'Madrid', 'R')
ver = compound_pace(session, 'VER')
print(ver)"""

"""

from analyzedata import position_progress
session =get_session(2024, 'Brazil','R')
ver = position_progress(session, 'VER')
print(ver)"""









import matplotlib.pyplot as plt
"""
x = [1,2,3,4,5,6] #must have same amount elem in x and y
y=[5,4,4,3,2,2]
y2=[6,5,4,4,3,3]
# plt.figure(figsize=(2,2))
# plt.plot(x,y, marker='o', color='red', linewidth=1) # adda a dot at each point
plt.plot(x,y, marker='o', label='driver 1')
plt.plot(x,y2, marker='o',label='driver 2')

plt.title('test test')
plt.xlabel('laps')
plt.ylabel('position')
plt.grid(True) # add grid
plt.show()
"""

"""
drivers =['VER','HAM','LEC','NOR']
wins = [63,104,7,1]
plt.bar(drivers,wins)
plt.title('driver wins')
plt.xlabel('driver')
plt.ylabel('wins')
plt.show()
"""
"""
laps = [1,2,3,4,5,6]
laptimes = [92.4, 91.8, 92.1, 91.5, 91.2, 91.6]

plt.scatter(laps, laptimes)
plt.title('laptimes')
plt.show()"""


"""
compounds =['SOFT', 'MEDIUM','HARD']
laps =[25,35,15]
plt.pie(laps,labels=compounds, autopct='%1.1f%%')    #pie chart
plt.show()
"""


""" # histogram
laptimes=[91.4, 91.8, 92.1, 91.5, 91.2,91.6, 92.3, 91.9, 92.5, 91.4]
plt.hist(laptimes, bins= 12)
plt.show()"""

"""
#shows multiple charts at once
fig, axes = plt.subplots(2, 1, figsize=(8, 8) )
axes[0].plot([1,2,3,4,5], [92,91,90,92,91])
axes[0].set_title('laptimes')

axes[1].bar(['VER', 'HAM'],[63,105])
axes[1].set_title('wins')
plt.tight_layout()
plt.show()


"""



"""
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].plot([1,2,3,4,5], [92,91,90,92,91], marker='o', color='red', label='VER')
axes[0].plot([1,2,3,4,5],[93,92,92,91,90], marker='s',color='blue', label='HAM')
axes[0].set_title('laptimes ')
axes[0].set_xlabel('lap')
axes[0].set_ylabel('times')
axes[0].legend()
axes[0].grid(True)
axes[1].bar(['VER','HAM', 'LEC'], [63,105,8], color=['blue','red','red'])
axes[1].set_title('wins total')
axes[1].set_xlabel('driver')
axes[1].set_ylabel(' wins')
plt.tight_layout()
plt.show()
"""


"""
fig, ax =plt.subplots(figsize=(10,5))
laps=[1,2,3,4,5,6,7,8,9,10]
times= [92,91,90,95,98,96,92,91,90,89]
ax.plot(laps, times, marker='d',color='black')
ax.set_title('ver race pace')
ax.set_xlabel('lap')
ax.set_ylabel('time')

ax.axvspan(4,6, alpha=0.99,color='pink', label='sc111') # alpha is opacity

ax.annotate('fastest',xy=(10,89), xytext=(7,92),
            arrowprops=dict(arrowstyle='->'))
ax.legend()
ax.grid(True)
plt.show()
"""





# plotly
import plotly.express as px

"""
# line chart 
laps = [1,2,3,4,5,6]
times= [92.4,91.8,92.1,91.5, 91.2,91.6]
fig =px.line(x=laps, y=times, title='laptimes')
fig.show()
"""

"""

#bar chart
drivers=['VER', 'HAM', 'LEC','NOR']
wins= [ 63,105,8,5]
fig= px.bar(x=drivers, y=wins, title='wins')
fig.show()
"""



"""
#scatter plot

laps =[1,2,3,4,5,6]
laptimes= [92.4, 91.8, 90.3, 91.2, 92.1, 90.9]
fig = px.scatter(x=laps,y=laptimes, title='laptimes')
fig.show()"""




import pandas as pd

"""
# two lines
data ={
    'lap': [1,2,3,4,5,6],
    'ver': [91.3, 91.5, 91.4, 92.0, 92.1, 92.5],
    'ham': [91.1, 91.3, 91.7, 91.9, 92.9, 92.4]  }
df = pd.DataFrame(data)

fig = px.line(df, x='lap', y=['ver', 'ham'], title='data')
fig.show()"""



"""
laps = [1,2,3,4,5,6]
times=[71.4, 71.9, 71.2, 71.6, 72.1, 71.9]
"""

"""
fig = px.line(x=laps,y=times, title='laptimes', markers=True)
fig.update_traces(line_color='pink', line_width=2.3)
fig.show()"""


"""
#titles for both axes, rest is same
fig = px.line(x=laps, y=times, title='laptimes')
fig.update_xaxes(title_text='lap number')
fig.update_yaxes(title_text='laptime')
fig.show()
"""


"""
data = {
    'lap': [1,2,3,4,5,6, 1,2,3,4,5,6],
    'time': [92.4, 91.8, 92.1, 91.5, 91.2, 91.6,  93.1, 92.5, 92.3, 92.0, 91.8, 91.5],
    'driver': ['VER','HAM','VER','VER','VER','VER', 'HAM','HAM','HAM','HAM','HAM','HAM'] }
df = pd.DataFrame(data)

# fig = px.line(df, x='lap', y='time', color='driver',title= 'laptimes')

# fig = px.line(df, x='lap', y='time', color='driver',
 #             color_discrete_map= {'VER': 'blue', 'HAM':'yellow'} )

# fig = px.line(df, x='lap', y='time', color='driver', template='ggplot2')

fig = px.scatter(df, x='lap',y='time', color='driver',  template='plotly_dark',
                 hover_data=['driver', 'time'])
fig.show()

"""




# plotly graph objects 

import plotly.graph_objects as go


"""

fig = go.Figure()
fig.add_trace(go.Scatter(x=[1,2,3], y=[92,91,90], mode='lines+markers', name='VER'))
fig.add_trace(go.Scatter(x=[1,2,3],y=[90,92,92], mode='lines+markers', name='ham'))
fig.update_layout(title='laptimes', xaxis_title='laps', yaxis_title='seconds')
fig.show()"""

"""
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=[1,2,3,4,5],
    y=[92,91,90,92,91],
    mode='lines+markers',
    name='ver',
    line=dict(color='blue',width=3) ))
fig.add_trace(go.Scatter(
    x=[1,2,3,4,5],
    y=[92,93,91,92,91],
    mode='lines+markers',
    name='ham',
    line=dict(color='red', width=2.5)))
fig.update_layout(
    title='lap times',
    xaxis_title='lap',
    yaxis_title='time',
    template='plotly_dark')
fig.show()
#  is more precise for detailed stuff and such
"""






"""fig = go.Figure()
fig.add_trace(go.Scatter(
    x=[1,2,3,4,5],
    y=[92,91,91,92,90],
    mode='lines+markers',
    name='lap time',
    line=dict(color='blue')))
fig.add_trace(go.Bar(
    x=[1,2,3,4,5],
    y=[3,2,5,14,8],
    name='position',
    marker_color='orange',
    yaxis='y2' ))
fig.update_layout(
    title='laptime and position',
    xaxis_title='lap',
    yaxis=dict(title='time', side='left'),
    yaxis2=dict(title='position',  overlaying='y', side='right'),
    template='plotly_dark')
fig.show()

"""


import plotly.graph_objects as go



"""
fig =go.Figure()
fig.add_trace(go.Scatter(
    x=[1,2,3,4,5,6,7,8,9,10],
    y=[92,91,90,95,96,97,91,92,92,91,92],
    mode='lines+markers',
    name='lap times',
    line=dict(color='white')))
fig.add_vrect(
    x0=4, x1=6,
    fillcolor='red', opacity=0.2,
    layer='below', line_width=0,
    annotation_text='sc', annotation_position='bottom left')
fig.update_layout(
    title='race pace ver',
    xaxis_title='lap',
    yaxis_title='time',
    template='plotly_dark')
fig.show()"""







from plotly.subplots import make_subplots


"""
fig = make_subplots(rows=2,cols=1)
fig.add_trace(go.Scatter(x=[1,2,3], y=[88,87,89], name='time'),row=1, col=1)
fig.add_trace(go.Bar(x=['ver','ham'], y=[63,105], name='wins'), row=2, col=1)
fig.show() # again two charts together"""



"""
fig = make_subplots(rows=2, cols=2, subplot_titles=('lap times', 'wins'))
fig.add_trace(
    go.Scatter(x=[1,2,33,4,5, 0.5], y=[90,91,99,92,91], mode='lines+markers', name='ver'),
    row=1,col=1 )
fig.add_trace(
    go.Bar(x=['ver', 'alo', 'lin'], y=[63,32,1], name='wins'),
    row=2, col=1 )
fig.update_layout(template='plotly_dark', height = 610)
fig.show()
"""



from charts import fastestlap_chart


"""
session = get_session(2026, 'Bahrain', 'Q')
drivers = ['VER', 'HAM', 'ALO', 'BOR']
fig = fastestlap_chart(session, drivers)
fig.show()"""