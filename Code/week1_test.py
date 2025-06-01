from skyfield.api import EarthSatellite, load
from datetime import datetime
import numpy as np

# TLE (for the ISS)
tle_iss = [
    "ISS (ZARYA)",
    "1 25544U 98067A   24140.51005787  .00004250  00000+0  85977-4 0  9991",
    "2 25544  51.6421 160.9324 0004693 293.4370 181.2067 15.50367430441329"
]

# Load a satellite
sat_iss = EarthSatellite(tle_iss[1], tle_iss[2], tle_iss[0])
ts = load.timescale()
t = ts.utc(2025, 5, 20, 12, 0, 0)  # a UTC time
geo_iss = sat_iss.at(t)

# Get position and velocity
position_km = geo_iss.position.km
velocity_kmps = geo_iss.velocity.km_per_s

print("Position (km):", position_km)
print("Velocity (km/s):", velocity_kmps)

# Load another satellite
tle_noaa15 = [
    "NOAA 15",
    "1 25338U 98030A   24140.39692130  .00000083  00000+0  68134-4 0  9991",
    "2 25338  98.7390 136.7234 0011536 170.2362 189.8990 14.25766605840442"
]

sat_noaa15 = EarthSatellite(tle_noaa15[1], tle_noaa15[2], tle_noaa15[0])
geo_noaa15 = sat_noaa15.at(t)

v1 = np.array(geo_iss.velocity.km_per_s)
v2 = np.array(geo_noaa15.velocity.km_per_s)

relative_velocity = v1 - v2
approach_speed = np.linalg.norm(relative_velocity)

print("Relative position vector (km):", geo_iss.position.km - geo_noaa15.position.km)
print("Relative velocity vector (km/s):", relative_velocity)
print("Approach speed (km/s):", approach_speed)