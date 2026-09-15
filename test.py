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
print(res)"""


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







from analyzedata import teammategap_quali
res = teammategap_quali('VER', 'PER', ['Monza'], [2021])
print(res)