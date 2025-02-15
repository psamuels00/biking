import json
import sqlite3


class DbBase:
    def __init__(self, params):
        self.params = params

    def connect(self):
        conn = sqlite3.connect(self.params.strava.db_cache.file)
        cursor = conn.cursor()

        return conn, cursor

    def command(self, sql, args=tuple()):
        conn, cursor = self.connect()

        cursor.execute(sql, args)
        conn.commit()

    def query(self, sql, args=tuple()):
        conn, cursor = self.connect()

        cursor.execute(sql, args)
        rows = cursor.fetchall()
        cursor.close()

        return rows


class Db(DbBase):
    def create_table(self):
        self.command(
            """
            create table if not exists activities (
                date text primary key,
                activities text
            )
        """
        )

    def select_activities(self):
        rows = self.query(
            """
            select  date, activities
              from  activities
          order by  date
        """
        )

        rows = [(row[0], json.loads(row[1])) for row in rows]

        return rows

    def insert_activity(self, date, activity):
        activity_str = json.dumps(activity)
        self.command("insert into activities (date, activities) values (?, ?)", (date, activity_str))

    def update_activity(self, date, activity):
        activity_str = json.dumps(activity)
        self.command("update activities set activities = ? where date = ?", (activity_str, date))
