from requests_cache import CachedSession


def get_elevation(cache_name, lat, lng):
    session = CachedSession(cache_name)

    url = f"https://api.open-elevation.com/api/v1/lookup?locations={lat},{lng}"
    response = session.get(url)

    elevation = None

    if response.status_code == 200:
        data = response.json()
        elevation = data["results"][0]["elevation"]

    return elevation
