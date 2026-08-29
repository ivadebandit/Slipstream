import fastf1
fastf1.Cache.enable_cache('cache')

def get_session(year, gp, identifier):
    session = fastf1.get_session(year, gp, identifier)
    session.load()
    return session