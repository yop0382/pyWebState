import psycopg2
import urllib.parse


class Pg:
    conn = None
    pg_connect_string_u = "postgresql://postgres:1234@pgha-postgresql-ha-pgpool:5432/test"
    pg_connect_string = None

    def __init__(self):
        self.pg_connect_string = urllib.parse.urlparse(self.pg_connect_string_u)

    def is_connected(self):
        try:
            sql = """ SELECT 1 """
            cur = self.conn.cursor()
            cur.execute(sql)
        except:
            self.connect_pg()

    def connect_pg(self):
        username = self.pg_connect_string.username
        password = self.pg_connect_string.password
        database = self.pg_connect_string.path[1:]
        hostname = self.pg_connect_string.hostname
        port = self.pg_connect_string.port

        self.conn = psycopg2.connect(
            database=database,
            user=username,
            password=password,
            host=hostname,
            port=port
        )

        self.conn.autocommit = True

    def get_command_progress(self, command_id):
        self.is_connected()

        sql = """ SELECT COUNT(*) AS events_number FROM events WHERE command_id = %s; """
        cur = self.conn.cursor()
        cur.execute(sql, (command_id,))
        events_number = cur.fetchone()[0]

        sql = """ SELECT COUNT(*) AS events_number FROM events WHERE command_id = %s AND status = %s; """
        cur = self.conn.cursor()
        cur.execute(sql, (command_id, "done"))
        events_done = cur.fetchone()[0]

        return {"events_number": events_number, "events_done": events_done}
