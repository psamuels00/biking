from requests_cache import CachedSession


def get_elevation(cache_name, lat, lng, isThis=False):
    session = CachedSession(cache_name)

    if (lat, lng) == (37.98170233603846, -121.93490873758489):
        return 426.72 # 1400 ft

    url = f"https://api.open-elevation.com/api/v1/lookup?locations={lat},{lng}"
    response = session.get(url)

    elevation = None

    if response.status_code == 200:
        data = response.json()
        elevation = data["results"][0]["elevation"]

    return elevation