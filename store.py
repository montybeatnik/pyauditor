from dataclasses import dataclass
import sqlite3
import datetime
from getpass import getuser

import models

@dataclass
class Auditor:
    db: str

    def create_table(self):
        query = """ -- create audit table
CREATE TABLE IF NOT EXISTS audits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT,
    cmd TEXT,
    created_at DATETIME,
    hostname TEXT,
    output BLOB,
    was_successful BOOLEAN,
    failure_reason TEXT
);        
"""
        with sqlite3.connect(self.db) as conn:
            try:
                conn.execute(query)
            except Exception as e:
                print(f"failed to create table {e}")

    def update(self, audit: models.Audit):
        with sqlite3.connect(self.db) as conn:
            query = f""" -- insert one
INSERT INTO audits (
    created_at,
    user,
    cmd,
    hostname,
    output,
    was_successful,
    failure_reason
) VALUES (
    ?, ?, ?, ?, ?, ?, ?
);
"""
            try:
                params = (
                    datetime.datetime.now(), 
                    audit.user,
                    audit.cmd, 
                    audit.device.hostname, 
                    audit.output,
                    audit.was_successful,
                    audit.failure_reason,
                )
                conn.execute(query, params)
            except Exception as e:
                print(f"couldn't update {self.db} DB; {e}")

    def table_exists(self, table_name: str) -> bool:
        # query = "SELECT name FROM sqlite_master WHERE name=?;"
        query = "SELECT name FROM sqlite_master WHERE name='audits';"
        try: 
            with sqlite3.connect(self.db) as conn:
                # cur = conn.execute(query, table_name)
                cur = conn.execute(query)
                row = cur.fetchone()
                print(f"{row=}")
                if row[0] == "audits":
                    return True
        except Exception as e:
            print(f"couldn't very if table {table_name} exists: {str(e)}")
            return False
        return False

if __name__ == "__main__":
    # TODO: this is wrong; fix it when you have time!
    user = getuser()
    auditor = Auditor(db="audits.db")
    auditor.create_table()