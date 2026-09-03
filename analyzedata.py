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