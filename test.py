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
from analyzedata import raceresult

session=get_session(2026, 'Netherlands' , 'R')
res = raceresult(session)
print(res)