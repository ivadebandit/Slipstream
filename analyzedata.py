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





def teamstandings(year, races):

    results = {}

    for race in races:
        session= get_session(year, race, 'R')

        raceresults = session.results
        for _, row in raceresults.iterrows():
            team = row['TeamName']

            points = row['Points']
            results[team] = results.get(team, 0) +points

    return results

def teamsprints(year, races):
    results = {}
    for race in races:
        try:
            session = get_session(year, race, 'S')
        except:
            continue
        sprintres = session.results
        for _, row in sprintres.iterrows():

            team = row['TeamName']
            points = row['Points']
            results[team] = results.get(team, 0) + points

    return results



def totalteams(year,races):
    racepts = teamstandings(year,races)
    sprintpts = teamsprints(year,races)

    combined= {}
    for teams, points in racepts.items():
        combined[teams] = points
    for teams, points in sprintpts.items():
        combined[teams]= combined.get(teams, 0) + points


    return combined
    


def boxbox(session):

    results =[]
    laps = session.laps

    drivers =session.laps['Driver'].unique()


    for driver in drivers:
        driver_laps = laps[laps['Driver']==driver]
        pit_in  = driver_laps[driver_laps['PitInTime'].notna()]


        if not pit_in.empty:
            for _, row in pit_in.iterrows():
                goin = row['LapNumber']
                pitin = row['PitInTime']
                goout = driver_laps[driver_laps['LapNumber'] == goin+1]
                if not goout.empty:
                    pitout = goout.iloc[0]['PitOutTime']


                    duration = (pitout-pitin).total_seconds()
                    if duration < 100:
                        results.append({'driver':driver, 'lap':goin, 'duration': duration})
    return results





def racepace(session, driver):
    laps = session.laps
    driverlaps = laps[laps['Driver'] == driver]
    filtered = driverlaps[driverlaps['TrackStatus'] =='1']
    filtered = filtered[filtered['IsAccurate'] == True]
    filtered = filtered[filtered['PitInTime'].isna()]
    filtered = filtered[filtered['PitOutTime'].isna()]

    filtered = filtered[filtered['LapTime'].notna()]

    filtered['seconds']=filtered['LapTime'].dt.total_seconds()


    results = {}
    stints = filtered['Stint'].unique()

    for stint in stints:

        stintlaps = filtered[filtered['Stint']==stint]
        avg = stintlaps['seconds'].mean()

        results[int(stint)] = round(float(avg),3)
    return results




def tiredeg(session,driver):

    laps = session.laps

    driverlaps = laps[laps['Driver']==driver]
    driverlaps = driverlaps[driverlaps['LapTime'].notna()]
    driverlaps= driverlaps[driverlaps['TyreLife'].notna()]
    results = []



    for stint in driverlaps['Stint'].unique():
        stint_laps = driverlaps[driverlaps['Stint']== stint]


        if len(stint_laps) < 5:
            continue
        laptimes = []

        for _, row in stint_laps.iterrows():
            seconds=row['LapTime'].total_seconds()
            laptimes.append(seconds)

        first5 = laptimes[:5]
        last5 = laptimes[-5:]
        firstavg = sum(first5) / 5
        lastavg = sum(last5) /5

        lapsbetween = len(stint_laps) -5
        deg = (lastavg - firstavg) / lapsbetween

        results.append({
                'stint': int(stint),
                'compound': stint_laps.iloc[0]['Compound'],
                'deg': round(deg,3)})


    return results



def teammategap_pace(session, d1,d2):

    laps = session.laps
    laps1 = clean_laps(session,d1)
    laps2 = clean_laps(session,d2)
    pace1 = float(laps1.mean())
    pace2 =float(laps2.mean())

    if (pace1 < pace2):
        faster = d1
        gap = pace2 - pace1
    else:
        faster = d2
        gap = pace1 - pace2
    return {
        'faster': faster,
        'gap': round(gap, 3),
        'pace1': round(pace1,3),
        'pace2': round(pace2,3) }



def filtered_laps(session):
    laps = session.laps
    filtered = laps[laps['IsAccurate'] == True]
    filtered= filtered[filtered['TrackStatus'] == '1']
    filtered = filtered[filtered['Deleted'] == False]
    filtered = filtered[filtered['LapTime'].notna()]
    return filtered


def trackevo(session):
    laps = filtered_laps(session)

    laps = laps.sort_values('LapStartTime')

    results = []
    best = 1000

    for _, row in laps.iterrows():
        seconds = row['LapTime'].total_seconds()
        if seconds < best:
            best = seconds


        results.append({
            'driver': row['Driver'],
            'lap': row['LapNumber'],
            'time': round(seconds, 3),
            'best': round(best,3) })


    return results


def drs_zones(session,driver):
    laps = session.laps
    driverlaps = laps[laps['Driver'] == driver]

    fastest = driverlaps.pick_fastest()
    telemetry = fastest.get_telemetry()
    zones = []

    inzone = False
    distance_start = None

    for _, row in telemetry.iterrows():
        drs = row['DRS']
        open = drs in [10,12,14]
        if open and not inzone:
            inzone = True
            distance_start = row['Distance']

        if not open and inzone:
            inzone = False
            end_distance = row['Distance']
            zones.append({
                'start': round(distance_start, 1),
                'end': round(end_distance,1) })
    return zones



def h2h(driver1, driver2, races, years):
    results = {}
    for race in races:

        d1_wins = 0
        d2_wins = 0
        for year in years:
            session = get_session(year,race, 'Q')

            qualires = session.results
            d1_res = qualires[qualires['Abbreviation'] == driver1]
            d2_res = qualires[qualires['Abbreviation'] == driver2]


            if d1_res.empty or d2_res.empty:
                continue
            d1pos = d1_res.iloc[0]['Position']
            d2pos = d2_res.iloc[0]['Position']
            if d1pos < d2pos:
                d1_wins = d1_wins + 1
            elif d2pos < d1pos:
                d2_wins = d2_wins +1



        results[race] = {
            'd1_wins': d1_wins,
            'd2_wins': d2_wins }
    return results




def wet_session(session):
    laps = session.laps
    compounds = laps['Compound'].unique()
    for compound in compounds:
        if compound == 'INTERMEDIATE' or compound == 'WET':
            return True
    else:
        return False



def wetdrycomp(sessions, drivers):
    results = {}
    

    for driver in drivers:
        wet_positions = []
        dry_positions = []


        for session in sessions:
            session_results = session.results
            driver_res = session_results[session_results['Abbreviation'] == driver]
            if driver_res.empty:
                continue
            
            position = driver_res.iloc[0]['Position']

            if wet_session(session) == True:
                wet_positions.append(position)
            else:
                dry_positions.append(position)

        if len(wet_positions) >0:
            wetavg = sum(wet_positions) / len(wet_positions)
        else:
            wetavg = None
        if len(dry_positions)>0:
            dryavg = sum(dry_positions) / len(dry_positions)
        else:
            dryavg = None

        if wetavg is not None and dryavg is not None:
            advantage = wetavg - dryavg
        else:
            advantage = None

        results[driver] = {
                'advantage': round(float(advantage),3)if advantage is not None else None,
                'dry': round(float(dryavg), 3) if dryavg is not None else None,
                'wet': round(float(wetavg), 3) if wetavg is not None else None }

    return results
