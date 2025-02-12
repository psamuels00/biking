#!/usr/bin/env python

import sqlite3

from biking.params import Parameters


def main():
    params = Parameters()
    file = params.strava.db_cache.file
    print(f"Create activities database in {file}")

    conn = sqlite3.connect(file)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activities (
            date TEXT PRIMARY KEY,
            activities TEXT
        )
    """)

    conn.commit()


if __name__ == "__main__":
    main()
