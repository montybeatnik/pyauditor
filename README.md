# Auditor
Run audits against the network infrastructure. 

## Manage the project
- using [uv](https://github.com/astral-sh/uv)

### Add a dependency
```bash
uv add xmltodict
```

## Create the DB
```bash
python store.py
```

### run an audit and look at the tables
```sql
.mode table
sqlite> select * from audits; 
+----+--------------+----------------------------+----------+----------------------------------------+
| id |     cmd      |         created_at         | hostname |                 output                 |
+----+--------------+----------------------------+----------+----------------------------------------+
| 9  | show version | 2025-01-13 14:06:49.226962 | lab-r1   | JUNOS Software Release [12.1X46-D20.5] |
| 10 | show version | 2025-01-13 14:06:51.120142 | lab-r2   | JUNOS Software Release [12.1X46-D20.5] |
| 11 | show version | 2025-01-13 14:06:52.969728 | lab-r3   | JUNOS Software Release [12.1X46-D20.5] |
| 12 | show version | 2025-01-13 14:06:54.552075 | lab-r4   | JUNOS Software Release [12.1X46-D20.5] |
| 13 | show version | 2025-01-13 14:06:56.441286 | lab-r5   | JUNOS Software Release [12.1X46-D20.5] |
| 14 | show version | 2025-01-13 14:06:57.298813 | lab-r6   | JUNOS Software Release [12.1X46-D20.5] |
| 15 | show version | 2025-01-13 14:06:58.972081 | lab-r7   | JUNOS Software Release [12.1X46-D20.5] |
| 16 | show version | 2025-01-13 14:07:00.070654 | lab-r8   | JUNOS Software Release [12.1X46-D20.5] |
+----+--------------+----------------------------+----------+----------------------------------------+
```

## TODO
- [ ] Add failure column to audit table 
    - ensure the reason is added
- [ ] improve the exception handling 
