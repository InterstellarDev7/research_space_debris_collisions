import requests

# Function to fetch TLE data from space-track.org
def fetch_tle(norad_id, username, password):
    """
    Fetch the latest TLE data for a given NORAD Catalog ID from space-track.org.
    Returns a list of TLE lines.clea
    """
    LOGIN_URL = 'https://www.space-track.org/ajaxauth/login'
    TLE_URL = f'https://www.space-track.org/basicspacedata/query/class/tle_latest/NORAD_CAT_ID/{norad_id}/format/tle'

    session = requests.Session()
    login_data = {'identity': username, 'password': password}
    response = session.post(LOGIN_URL, data=login_data)

    if response.ok:
        tle_response = session.get(TLE_URL)
        if tle_response.ok:
            return tle_response.text.strip().split('\n')
        else:
            raise Exception(f"Failed to fetch TLE: {tle_response.status_code}")
    else:
        raise Exception(f"Login failed: {response.status_code}")

# Function to fetch TLE and create an EarthSatellite object
def fetch_and_create_satellite(norad_id, name, username, password):
    tle_lines = fetch_tle(norad_id, username, password)
    tle = [name] + tle_lines
    return EarthSatellite(tle[1], tle[2], tle[0])