# Queries houses queries as consts

CREATE_AUDIT_TABLE = """ -- create audit table
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

TABLE_EXISTS = "SELECT name FROM sqlite_master WHERE name='audits';"

INSERT_AUDIT = """ -- insert one
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