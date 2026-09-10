from getdata import get_session

def clean_laps(session, driver):
    laps = session.laps
    driver_laps = laps[laps['Driver'] == driver]
    driver_laps = driver_laps[driver_laps['IsAccurate'] == True]
    driver_laps = driver_laps[driver_laps['TrackStatus'] == '1' ]
    driver_laps = driver_laps[driver_laps['Deleted'] ==False]



    driver_laps = driver_laps.dropna(subset=['LapTime'])

    driver_laps = driver_laps['LapTime'].dt.total_seconds()
    return driver_laps


def raceresult(session):
    results = session.results
    sort = results.sort_values('Points', ascending=False)

    return sort[['Abbreviation', 'TeamName', 'Position', 'Points', 'Status']]


def fastest_lap(session,driver): # for a specific driver

    laps = clean_laps(session, driver)
    fastest = laps.min()

    return fastest


def fastestoverall(session):
    laps = session.laps
    laps['LapTime'] = laps['LapTime'].dt.total_seconds()
    fastest = laps['LapTime'].min()
    return fastest

def get_consistency(session, driver):
    laps =clean_laps(session,driver)
    result = laps.std()
    return round(result, 3)
#boxbox gone should readd at some point later



import pandas as pd
def quali_progress(session, driver):


    results = session.results
    driverres = results[results['Abbreviation']== driver]

    q1 = driverres.iloc[0]['Q1']
    q2= driverres.iloc[0]['Q2']
    q3= driverres.iloc[0]['Q3']
    if pd.notna(q2) and pd.notna(q3):
        q1toq2 = (q1-q2).total_seconds()
        q2toq3= (q2-q3).total_seconds()
    elif pd.notna(q2):
        q1toq2 = (q1-q2).total_seconds()
        q2toq3= None
    else:
        q1toq2 = None
        q2toq3 = None

    results = {
        'q1toq2': q1toq2,
        'q2toq3': q2toq3,
        'q1': q1.total_seconds(),
        'q2': q2.total_seconds(),
        'q3':q3.total_seconds()}
    return results


def qualipositions(driver,circuit, years):

    results = {}
    for year in years:
        session = get_session(year, circuit, 'Q')
        qualiresults = session.results
        driver_result = qualiresults[qualiresults['Abbreviation']==driver]

        if not driver_result.empty:
            position= driver_result.iloc[0]['Position']
            results[year] = int(driver_result.iloc[0]['Position'])
        else:
            continue
    return results





def racepositions(driver, circuit, years):
    results = {}

    for year in years:
        session = get_session(year, circuit, 'R')
        raceres = session.results
        driverresults = raceres[raceres['Abbreviation'] == driver]
        if not driverresults.empty:

            position = driverresults.iloc[0]['Position']
            results[year]= int(driverresults.iloc[0]['Position'])

        else:
            continue
    return results





def bestlaps_quali(driver, circuit, years):
    results = {}
    for year in years:
        try:
            session = get_session(year, circuit, 'Q')
            fastest = fastest_lap(session, driver)
            if fastest is not None:
                results[year] = float(fastest)
        except: 
            continue
    return results

def fastest_all_time(location, years):
    results = {}
    for year in years:
        session= get_session(year, location, 'Q')
        laps = session.laps
        filtlaps = laps[laps['TrackStatus'] =='1']
        filtlaps =filtlaps[filtlaps['Deleted'] == False]
        filtlaps = filtlaps[filtlaps['IsAccurate'] == True]


        fastest = filtlaps.sort_values('LapTime').iloc[0]



        results[year] = {
            'time':fastest['LapTime'].total_seconds(),
            'driver': fastest['Driver'] }

    fastestfastest = min(results, key = lambda x: results[x]['time'])

    return {
        'time': results[fastestfastest]['time'],
        'year': fastestfastest,
        'driver': results[fastestfastest]['driver'] }






def driverstandings(year, races):
    results = {}
    for race in races:
        session = get_session(year, race, 'R')
        race_results = session.results

        for _, row in race_results.iterrows():
            driver=row['Abbreviation']

            points= row['Points']


            results[driver] = results.get(driver, 0) + points
    return results


def standingssprint(year,races):
    results={}


    for race in races:
        try:
            session = get_session(year, race, 'S')

        except:
            continue
        race_results = session.results
        for _, row in race_results.iterrows():
                driver = row['Abbreviation']
                points = row['Points']


                results[driver] = results.get(driver,0) +points
    return results



def totalpoints(year, races):

    racepoints = driverstandings(year, races)
    sprintpts = standingssprint(year, races)
    combined = {}
    for driver, points in racepoints.items():
        combined[driver] = points
    for driver, points in sprintpts.items():
        combined[driver]=combined.get(driver,0) + points
    return  combined
