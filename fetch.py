import requests
import folium

BASE = "https://opendata.adsb.fi/api/v2/lat/{lat}/lon/{lon}/dist/{dist}"

def fetch_aircraft(lat, lon, dist_km):
    url = BASE.format(lat=lat, lon=lon, dist=dist_km)
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.json().get("aircraft", [])

if __name__ == "__main__":
    lat, lon, dist = 39.95, -75.20, 5
    aircraft = fetch_aircraft(lat, lon, dist)

    # Initialize map centered at your location
    m = folium.Map(location=[lat, lon], zoom_start=9)
    folium.Marker([lat, lon], popup="You (center)", icon=folium.Icon(color="blue")).add_to(m)

    # Add aircraft markers
    for ac in aircraft:
        ac_lat = ac.get("lat")
        ac_lon = ac.get("lon")
        callsign = ac.get("flight") or "N/A"
        popup = f"{callsign} @ {ac.get('alt_baro')} ft"
        folium.Marker(
            [ac_lat, ac_lon],
            popup=popup,
            icon=folium.Icon(color="red", icon="plane", prefix="fa")
        ).add_to(m)

    # Save map
    m.save("aircraft_map.html")
    print(f"Saved map with {len(aircraft)} aircraft.")
