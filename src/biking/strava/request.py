from requests_cache import CachedSession


class RequestBase:
    def __init__(self, params, auth):
        self.params = params
        self.auth = auth

        name = params.http_cache.file
        expire_sec = params.http_cache.expire_sec
        self.session = CachedSession(name, expire_after=expire_sec)

    def fetch(self, url, params=None, level=0):
        access_token = self.auth.credentials.access_token
        headers = {
            "Authorization": f"Bearer {access_token}",
        }

        args = dict()
        if params:
            args["params"] = params

        response = self.session.get(url, headers=headers, **args)

        # if response.from_cache:
        #     print("@@@ Response was served from cache.")
        # else:
        #     print("@@@ Fetched a fresh response.")

        data = response.json()

        token_expired = (
            response.status_code == 401
            and data["message"] == "Authorization Error"
            and data["errors"][0]["field"] == "access_token"
            and data["errors"][0]["code"] == "invalid"
        )

        if response.status_code == 200:
            # print(json.dumps(data, indent=4))
            return data
        elif not token_expired or level > 1:
            print(f"**** Error: {response.status_code}")
            print("**** Response:", response.text)
            return None

        self.auth.refresh_tokens()
        return self.fetch(url, params, level + 1)


class Request(RequestBase):
    def get_athlete(self):
        data = self.fetch(self.params.url.athlete)

        return data

    def get_activities(self):
        params = dict(
            per_page=100,
            page=1,
        )
        data = []

        while True:
            page_data = self.fetch(self.params.url.activities, params)
            if not page_data:
                break
            data.extend(item for item in page_data if item["sport_type"] == "Ride")
            params["page"] += 1

        return data

    def get_new_activities(self, app_cache):
        """
        Get activities that are not already in the application cache.
        Even if an activity is in the app cache, we still look to see if it has changed since it was cached.
        We do not try to load all Strava activities to compare with the cache.  Instead, we look back until
        a certain number of activities (say 3) are the same in cache as loaded from Strava.  When that is
        true, we stop loading older activities from Strava.
        """
        params = dict(
            per_page=3,
            page=1,
        )
        data = []

        same_counter = 0
        num_lookback = self.params.db_cache.num_activities_lookback_for_change

        while same_counter < num_lookback:
            # print(f"@@@ get_activities, page {params["page"]}")
            page_data = self.fetch(self.params.url.activities, params)
            if not page_data:
                break

            items = [item for item in page_data if item["sport_type"] == "Ride"]
            for item in items:
                date = item["start_date_local"]
                if item == app_cache.get(date):
                    same_counter += 1
                    # print(f"@@@ same item {item["start_date_local"]}, counter = {same_counter}")
                    if same_counter == num_lookback:
                        break
                else:
                    data.append(item)
                    same_counter = 0
                    # print(f"@@@ new item {item["start_date_local"]}, counter = {same_counter}")

            params["page"] += 1

        return data
