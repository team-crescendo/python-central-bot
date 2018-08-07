import psycopg2
from threading import get_ident


class PostgreSQL:
    def __init__(self, **kwargs):
        self.host = kwargs.get("host", "localhost")
        self.user = kwargs.get("user", "postgres")
        self.pw = kwargs.get("pw", "")
        self.dbname = kwargs.get("dbname", "postgres")

        self.cursor_dict = {}
        self.conn_dict = {}

    def _make_connection(self, tid=get_ident()):
        if not tid in self.conn_dict:
            self.conn_dict[tid] = psycopg2.connect(
                f"host={self.host} user={self.user} {'password=' if self.pw else ''}{self.pw} dbname={self.dbname}"
            )
            self.conn_dict[tid].autocommit = True
        elif self.conn_dict[tid].closed:
            self.conn_dict[tid] = psycopg2.connect(
                f"host={self.host} user={self.user} {'password=' if self.pw else ''}{self.pw} dbname={self.dbname}"
            )
            self.conn_dict[tid].autocommit = True
        return self.conn_dict[tid]

    def get_cursor(self, tid=get_ident()):
        if not tid in self.cursor_dict:
            self.cursor_dict[tid] = self._make_connection(tid).cursor()

        elif self.cursor_dict[tid].closed:
            self.cursor_dict[tid] = self._make_connection(tid).cursor()

        return self.cursor_dict[tid]

    # Run
    def run(self, query: str):
        cur = self.get_cursor()
        cur.execute(query)

        return cur

    # Run N Fetch
    def rnf(self, query: str):
        cur = self.get_cursor()
        cur.execute(query)
        
        return cur, cur.fetchall()

