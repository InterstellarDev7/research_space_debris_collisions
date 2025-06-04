import requests
import getpass
from skyfield.api import EarthSatellite, load
import numpy as np

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

# Credentials for space-track.org
username = input("Enter your Space-Track username: ")
password = getpass.getpass("Enter your Space-Track password: ")

# Define satellites
satellites_info = [
    (25544, "ISS (ZARYA)"),
    (25338, "NOAA 15"),
    (33591, "NOAA 19"),
    (22236, "COSMOS 2221")
]

# Fetch and create satellites
satellites = []
for norad_id, name in satellites_info:
    sat = fetch_and_create_satellite(norad_id, name, username, password)
    satellites.append(sat)

# Load timescale
ts = load.timescale()
start_time = ts.utc(2024, 2, 27, 12, 0, 0)
time_steps = ts.utc(start_time.utc.year, start_time.utc.month, start_time.utc.day, range(0, 48))

# Store results
times = []
relative_positions = {name: [] for _, name in satellites_info[1:]}
approach_speeds = {name: [] for _, name in satellites_info[1:]}

for t in time_steps:
    states = [sat.at(t) for sat in satellites]
    iss_state = states[0]
    for i, state in enumerate(states[1:], start=1):
        rel_pos = iss_state.position.km - state.position.km
        rel_vel = iss_state.velocity.km_per_s - state.velocity.km_per_s
        approach_speed = np.linalg.norm(rel_vel)
        relative_positions[satellites_info[i][1]].append(np.linalg.norm(rel_pos))
        approach_speeds[satellites_info[i][1]].append(approach_speed)
    times.append(t.utc_iso())