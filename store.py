from dataclasses import dataclass
import sqlite3
import datetime

from models import Device

@dataclass
class AuditUpdate:
    device: Device
    cmd: str
    output: str
    db: str

    def create_table(self):
        query = """ -- create audit table
CREATE TABLE IF NOT EXISTS audits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cmd TEXT,
    created_at DATETIME,
    hostname TEXT,
    output BLOB
);        
"""
        with sqlite3.connect(self.db) as conn:
            try:
                conn.execute(query)
            except Exception as e:
                print(f"failed to create table {e}")

    def update(self):
        with sqlite3.connect(self.db) as conn:
            query = f""" -- insert one
INSERT INTO audits (
    created_at,
    cmd,
    hostname,
    output
) VALUES (
    ?, ?, ?, ?
);
"""
            try:
                params = (datetime.datetime.now(), self.cmd, self.device.hostname, self.output)
                conn.execute(query, params)
            except Exception as e:
                print(f"couldn't update {self.db} DB; {e}")

if __name__ == "__main__":
    audit_update = AuditUpdate(
        device=Device(hostname="test", mgmt_addr="1.1.1.1", username="user", password="pass"),        
        cmd="test command",
        output="{'msg':'some msg'}",
        db="audits.db",
    )
    audit_update.create_table()