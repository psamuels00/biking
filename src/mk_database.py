#!/usr/bin/env python

from biking.db import Db
from biking.params import Parameters


def main():
    params = Parameters()
    print(f"Create Activities table in {params.strava.db_cache.file}")
    Db(params).create_table()


if __name__ == "__main__":
    main()
