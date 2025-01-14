# DB 

## Overview
We're using sqlite3 at the moment. We could have chosen a fancy DB like postgres (I fancy the relational model) or even mongo (if you're into noSQL), but sqlite is already running on our machines. That is pretty much the primary reason for that decision. 

since we're not doing anything complicated, it works just fine. 

## Queries 
```sql
-- to drop into the sqlite interface 
sqlite3 audits.db
-- to log out
sqlite> .exit
-- to see the tables
sqlite> .tables
audits
-- to see the current schema of the audits table
sqlite> .schema audits
CREATE TABLE audits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cmd TEXT,
    created_at DATETIME,
    hostname TEXT,
    output BLOB,
    was_successful BOOLEAN,
    failure_reason TEXT
);
-- how many rows are there?
sqlite> SELECT count(*) FROM audits;
31
-- how many failed
sqlite> SELECT count(*) FROM audits WHERE was_successful = false;
3
-- why did they fail
sqlite> .mode table -- to make the format easier to digest
sqlite> SELECT hostname, failure_reason FROM audits WHERE was_successful = false;
+----------+-------------------------------------------+
| hostname |              failure_reason               |
+----------+-------------------------------------------+
| lab-r7   | TCP connection to device failed.          |
|          |                                           |
|          | Common causes of this problem are:        |
|          | 1. Incorrect hostname or IP address.      |
|          | 2. Wrong TCP port.                        |
|          | 3. Intermediate firewall blocking access. |
|          |                                           |
|          | Device settings:  10.0.0.213:22           |
|          |                                           |
+----------+-------------------------------------------+
| lab-r7   | TCP connection to device failed.          |
|          |                                           |
|          | Common causes of this problem are:        |
|          | 1. Incorrect hostname or IP address.      |
|          | 2. Wrong TCP port.                        |
|          | 3. Intermediate firewall blocking access. |
|          |                                           |
|          | Device settings:  10.0.0.213:22           |
|          |                                           |
+----------+-------------------------------------------+
| lab-r7   | TCP connection to device failed.          |
|          |                                           |
|          | Common causes of this problem are:        |
|          | 1. Incorrect hostname or IP address.      |
|          | 2. Wrong TCP port.                        |
|          | 3. Intermediate firewall blocking access. |
|          |                                           |
|          | Device settings:  10.0.0.213:22           |
|          |                                           |
+----------+-------------------------------------------+
-- show the rows, but limit the output to 8
SELECT
    id,
    cmd,
    created_at,
    hostname,
    output
FROM audits
WHERE was_successful = true
limit 8;
-- show the types of audits run
sqlite> SELECT DISTINCT(cmd) as audit_types FROM audits;
+---------------------------+
|        audit_types        |
+---------------------------+
| show mpls lsp             |
| show system alarms        |
| show interfaces terse ge* |
+---------------------------+
-- show all audits for a specific device
SELECT
    id,
    cmd,
    created_at,
    hostname,
    output
FROM audits
WHERE hostname = 'lab-r1';
+----+---------------------------+----------------------------+----------+--------------------------------------------------------------+
| id |            cmd            |         created_at         | hostname |                            output                            |
+----+---------------------------+----------------------------+----------+--------------------------------------------------------------+
| 1  | show mpls lsp             | 2025-01-14 12:58:28.978858 | lab-r1   | Ingress LSP: 7 sessions                                      |
|    |                           |                            |          | To              From            State Rt P     ActivePath    |
|    |                           |                            |          |     LSPname                                                  |
|    |                           |                            |          | 10.1.0.2        10.1.0.1        Up     0 *                   |
|    |                           |                            |          |     R1_TO_R2                                                 |
|    |                           |                            |          | 10.1.0.3        10.1.0.1        Up     0 *                   |
|    |                           |                            |          |     R1_TO_R3                                                 |
|    |                           |                            |          | 10.1.0.4        10.1.0.1        Up     0 *                   |
|    |                           |                            |          |     R1_TO_R4                                                 |
|    |                           |                            |          | 10.1.0.5        10.1.0.1        Up     0 *                   |
|    |                           |                            |          |     R1_TO_R5                                                 |
|    |                           |                            |          | 10.1.0.6        10.1.0.1        Up     0 *                   |
|    |                           |                            |          |     R1_TO_R6                                                 |
|    |                           |                            |          | 10.1.0.7        10.1.0.1        Up     0 *                   |
|    |                           |                            |          |     R1_TO_R7                                                 |
|    |                           |                            |          | 10.1.0.8        10.1.0.1        Up     0 *                   |
|    |                           |                            |          |     R1_TO_R8                                                 |
|    |                           |                            |          | Total 7 displayed, Up 7, Down 0                              |
|    |                           |                            |          |                                                              |
|    |                           |                            |          | Egress LSP: 7 sessions                                       |
|    |                           |                            |          | To              From            State   Rt Style Labelin Lab |
|    |                           |                            |          | elout LSPname                                                |
|    |                           |                            |          | 10.1.0.1        10.1.0.5        Up       0  1 FF       3     |
|    |                           |                            |          |     - R5_TO_R1                                               |
|    |                           |                            |          | 10.1.0.1        10.1.0.2        Up       0  1 FF       3     |
|    |                           |                            |          |     - R2_TO_R1                                               |
|    |                           |                            |          | 10.1.0.1        10.0.0.3        Up       0  1 FF       3     |
|    |                           |                            |          |     - R3_TO_R1                                               |
|    |                           |                            |          | 10.1.0.1        10.1.0.6        Up       0  1 FF       3     |
|    |                           |                            |          |     - R6_TO_R1                                               |
|    |                           |                            |          | 10.1.0.1        10.1.0.8        Up       0  1 FF       3     |
|    |                           |                            |          |     - R8_TO_R1                                               |
|    |                           |                            |          | 10.1.0.1        10.1.0.4        Up       0  1 FF       3     |
|    |                           |                            |          |     - R4_TO_R1                                               |
|    |                           |                            |          | 10.1.0.1        10.1.0.7        Up       0  1 FF       3     |
|    |                           |                            |          |     - R7_TO_R1                                               |
|    |                           |                            |          | Total 7 displayed, Up 7, Down 0                              |
|    |                           |                            |          |                                                              |
|    |                           |                            |          | Transit LSP: 15 sessions                                     |
|    |                           |                            |          | To              From            State   Rt Style Labelin Lab |
|    |                           |                            |          | elout LSPname                                                |
|    |                           |                            |          | 10.1.0.2        10.1.0.5        Up       0  1 FF  300224     |
|    |                           |                            |          |     3 R5_TO_R2                                               |
|    |                           |                            |          | 10.1.0.2        10.1.0.6        Up       0  1 FF  300080     |
|    |                           |                            |          |     3 R6_TO_R2                                               |
|    |                           |                            |          | 10.1.0.2        10.1.0.8        Up       0  1 FF  300112     |
|    |                           |                            |          |     3 R8_TO_R2                                               |
|    |                           |                            |          | 10.1.0.2        10.1.0.7        Up       0  1 FF  300096     |
|    |                           |                            |          |     3 R7_TO_R2                                               |
|    |                           |                            |          | 10.1.0.3        10.1.0.5        Up       0  1 FF  300144   2 |
|    |                           |                            |          | 99792 R5_TO_R3                                               |
|    |                           |                            |          | 10.1.0.3        10.1.0.6        Up       0  1 FF  300304   2 |
|    |                           |                            |          | 99904 R6_TO_R3                                               |
|    |                           |                            |          | 10.1.0.3        10.1.0.8        Up       0  1 FF  300128   2 |
|    |                           |                            |          | 99776 R8_TO_R3                                               |
|    |                           |                            |          | 10.1.0.3        10.1.0.7        Up       0  1 FF  300192   2 |
|    |                           |                            |          | 99840 R7_TO_R3                                               |
|    |                           |                            |          | 10.1.0.5        10.1.0.2        Up       0  1 FF  300288   3 |
|    |                           |                            |          | 00576 R2_TO_R5                                               |
|    |                           |                            |          | 10.1.0.6        10.1.0.2        Up       0  1 FF  300240     |
|    |                           |                            |          |     3 R2_TO_R6                                               |
|    |                           |                            |          | 10.1.0.6        10.1.0.3        Up       0  1 FF  300208     |
|    |                           |                            |          |     3 R3_TO_R6                                               |
|    |                           |                            |          | 10.1.0.7        10.1.0.2        Up       0  1 FF  300272   3 |
|    |                           |                            |          | 00560 R2_TO_R7                                               |
|    |                           |                            |          | 10.1.0.7        10.1.0.3        Up       0  1 FF  300176   3 |
|    |                           |                            |          | 00496 R3_TO_R7                                               |
|    |                           |                            |          | 10.1.0.8        10.1.0.2        Up       0  1 FF  300256   3 |
|    |                           |                            |          | 00544 R2_TO_R8                                               |
|    |                           |                            |          | 10.1.0.8        10.1.0.3        Up       0  1 FF  300160   3 |
|    |                           |                            |          | 00480 R3_TO_R8                                               |
|    |                           |                            |          | Total 15 displayed, Up 15, Down 0                            |
+----+---------------------------+----------------------------+----------+--------------------------------------------------------------+
| 8  | show mpls lsp             | 2025-01-14 13:02:18.930331 | lab-r1   | Ingress LSP: 7 sessions                                      |
|    |                           |                            |          | To              From            State Rt P     ActivePath    |
|    |                           |                            |          |     LSPname                                                  |
|    |                           |                            |          | 10.1.0.2        10.1.0.1        Up     0 *                   |
|    |                           |                            |          |     R1_TO_R2                                                 |
|    |                           |                            |          | 10.1.0.3        10.1.0.1        Up     0 *                   |
|    |                           |                            |          |     R1_TO_R3                                                 |
|    |                           |                            |          | 10.1.0.4        10.1.0.1        Up     0 *                   |
|    |                           |                            |          |     R1_TO_R4                                                 |
|    |                           |                            |          | 10.1.0.5        10.1.0.1        Up     0 *                   |
|    |                           |                            |          |     R1_TO_R5                                                 |
|    |                           |                            |          | 10.1.0.6        10.1.0.1        Up     0 *                   |
|    |                           |                            |          |     R1_TO_R6                                                 |
|    |                           |                            |          | 10.1.0.7        10.1.0.1        Up     0 *                   |
|    |                           |                            |          |     R1_TO_R7                                                 |
|    |                           |                            |          | 10.1.0.8        10.1.0.1        Up     0 *                   |
|    |                           |                            |          |     R1_TO_R8                                                 |
|    |                           |                            |          | Total 7 displayed, Up 7, Down 0                              |
|    |                           |                            |          |                                                              |
|    |                           |                            |          | Egress LSP: 7 sessions                                       |
|    |                           |                            |          | To              From            State   Rt Style Labelin Lab |
|    |                           |                            |          | elout LSPname                                                |
|    |                           |                            |          | 10.1.0.1        10.1.0.5        Up       0  1 FF       3     |
|    |                           |                            |          |     - R5_TO_R1                                               |
|    |                           |                            |          | 10.1.0.1        10.1.0.2        Up       0  1 FF       3     |
|    |                           |                            |          |     - R2_TO_R1                                               |
|    |                           |                            |          | 10.1.0.1        10.0.0.3        Up       0  1 FF       3     |
|    |                           |                            |          |     - R3_TO_R1                                               |
|    |                           |                            |          | 10.1.0.1        10.1.0.6        Up       0  1 FF       3     |
|    |                           |                            |          |     - R6_TO_R1                                               |
|    |                           |                            |          | 10.1.0.1        10.1.0.8        Up       0  1 FF       3     |
|    |                           |                            |          |     - R8_TO_R1                                               |
|    |                           |                            |          | 10.1.0.1        10.1.0.4        Up       0  1 FF       3     |
|    |                           |                            |          |     - R4_TO_R1                                               |
|    |                           |                            |          | 10.1.0.1        10.1.0.7        Up       0  1 FF       3     |
|    |                           |                            |          |     - R7_TO_R1                                               |
|    |                           |                            |          | Total 7 displayed, Up 7, Down 0                              |
|    |                           |                            |          |                                                              |
|    |                           |                            |          | Transit LSP: 15 sessions                                     |
|    |                           |                            |          | To              From            State   Rt Style Labelin Lab |
|    |                           |                            |          | elout LSPname                                                |
|    |                           |                            |          | 10.1.0.2        10.1.0.5        Up       0  1 FF  300224     |
|    |                           |                            |          |     3 R5_TO_R2                                               |
|    |                           |                            |          | 10.1.0.2        10.1.0.6        Up       0  1 FF  300080     |
|    |                           |                            |          |     3 R6_TO_R2                                               |
|    |                           |                            |          | 10.1.0.2        10.1.0.8        Up       0  1 FF  300112     |
|    |                           |                            |          |     3 R8_TO_R2                                               |
|    |                           |                            |          | 10.1.0.2        10.1.0.7        Up       0  1 FF  300096     |
|    |                           |                            |          |     3 R7_TO_R2                                               |
|    |                           |                            |          | 10.1.0.3        10.1.0.5        Up       0  1 FF  300144   2 |
|    |                           |                            |          | 99792 R5_TO_R3                                               |
|    |                           |                            |          | 10.1.0.3        10.1.0.6        Up       0  1 FF  300304   2 |
|    |                           |                            |          | 99904 R6_TO_R3                                               |
|    |                           |                            |          | 10.1.0.3        10.1.0.8        Up       0  1 FF  300128   2 |
|    |                           |                            |          | 99776 R8_TO_R3                                               |
|    |                           |                            |          | 10.1.0.3        10.1.0.7        Up       0  1 FF  300192   2 |
|    |                           |                            |          | 99840 R7_TO_R3                                               |
|    |                           |                            |          | 10.1.0.5        10.1.0.2        Up       0  1 FF  300288   3 |
|    |                           |                            |          | 00576 R2_TO_R5                                               |
|    |                           |                            |          | 10.1.0.6        10.1.0.2        Up       0  1 FF  300240     |
|    |                           |                            |          |     3 R2_TO_R6                                               |
|    |                           |                            |          | 10.1.0.6        10.1.0.3        Up       0  1 FF  300208     |
|    |                           |                            |          |     3 R3_TO_R6                                               |
|    |                           |                            |          | 10.1.0.7        10.1.0.2        Up       0  1 FF  300272   3 |
|    |                           |                            |          | 00560 R2_TO_R7                                               |
|    |                           |                            |          | 10.1.0.7        10.1.0.3        Up       0  1 FF  300176   3 |
|    |                           |                            |          | 00496 R3_TO_R7                                               |
|    |                           |                            |          | 10.1.0.8        10.1.0.2        Up       0  1 FF  300256   3 |
|    |                           |                            |          | 00544 R2_TO_R8                                               |
|    |                           |                            |          | 10.1.0.8        10.1.0.3        Up       0  1 FF  300160   3 |
|    |                           |                            |          | 00480 R3_TO_R8                                               |
|    |                           |                            |          | Total 15 displayed, Up 15, Down 0                            |
+----+---------------------------+----------------------------+----------+--------------------------------------------------------------+
| 16 | show system alarms        | 2025-01-14 16:45:03.734937 | lab-r1   | 1 alarms currently active                                    |
|    |                           |                            |          | Alarm time               Class  Description                  |
|    |                           |                            |          | 2025-01-12 22:14:58 UTC  Minor  Rescue configuration is not  |
|    |                           |                            |          | set                                                          |
+----+---------------------------+----------------------------+----------+--------------------------------------------------------------+
| 27 | show interfaces terse ge* | 2025-01-14 16:48:10.596516 | lab-r1   | Interface               Admin Link Proto    Local            |
|    |                           |                            |          |       Remote                                                 |
|    |                           |                            |          | ge-0/0/0                up    up                             |
|    |                           |                            |          | ge-0/0/0.12             up    up   inet     172.16.12.1/24   |
|    |                           |                            |          |                                    mpls                      |
|    |                           |                            |          | ge-0/0/0.32767          up    up                             |
|    |                           |                            |          | ge-0/0/1                up    up                             |
|    |                           |                            |          | ge-0/0/1.16             up    up   inet     172.16.16.1/24   |
|    |                           |                            |          |                                    mpls                      |
|    |                           |                            |          | ge-0/0/1.32767          up    up                             |
|    |                           |                            |          | ge-0/0/2                up    up                             |
|    |                           |                            |          | ge-0/0/3                up    up                             |
|    |                           |                            |          | ge-0/0/4                up    up                             |
|    |                           |                            |          | ge-0/0/5                up    up                             |
|    |                           |                            |          | ge-0/0/6                up    up                             |
|    |                           |                            |          | ge-0/0/7                up    up                             |
|    |                           |                            |          | ge-0/0/7.0              up    up   inet     10.0.0.86/24     |
+----+---------------------------+----------------------------+----------+--------------------------------------------------------------+
```