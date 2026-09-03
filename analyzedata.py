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