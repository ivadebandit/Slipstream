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

