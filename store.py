from dataclasses import dataclass
import sqlite3
import datetime
from getpass import getuser

import models
import queries

@dataclass
class Auditor:
    db: str

    def create_table(self):
        """
        create_table creates the audits table. In the future, this could be expanded 
        to take in a table name and it could be extensible and re-usable yadda yadda. 
        """
        with sqlite3.connect(self.db) as conn:
            try:
                conn.execute(queries.CREATE_AUDIT_TABLE)
            except Exception as e:
                print(f"failed to create table {e}")

    def insert_audit(self, audit: models.Audit):
        with sqlite3.connect(self.db) as conn:
            try:
                params = (
                    datetime.datetime.fromtimestamp(datetime.datetime.now()), 
                    audit.user,
                    audit.cmd, 
                    audit.device.hostname, 
                    audit.output,
                    audit.was_successful,
                    audit.failure_reason,
                )
                conn.execute(queries.INSERT_AUDIT, params)
            except Exception as e:
                print(f"couldn't update {self.db} DB; {e}")

    def table_exists(self, table_name: str) -> bool:
        # query = "SELECT name FROM sqlite_master WHERE name=?;"
        try: 
            with sqlite3.connect(self.db) as conn:
                # cur = conn.execute(query, table_name)
                cur = conn.execute(queries.TABLE_EXISTS)
                row = cur.fetchone()
                print(f"{row=}")
                if row[0] == "audits":
                    return True
        except Exception as e:
            print(f"couldn't verify table {table_name} exists: {str(e)}")
            return False
        return False

if __name__ == "__main__":
    # TODO: this is wrong; fix it when you have time!
    user = getuser()
    auditor = Auditor(db="audits.db")
    auditor.create_table()