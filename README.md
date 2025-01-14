# Auditor
Run audits against the network infrastructure. 

## Overview
There are times when we'll want to run audits against our fleet of devices. This is the begining of a framework to do just that. 

### Env Variables
We could get these from a vault - see [hashicorp](https://www.vaultproject.io/). 
- `SSH_USER`
- `SSH_PASSWORD`

## Manage the project
- using [uv](https://github.com/astral-sh/uv)

### Add a dependency
```bash
uv add xmltodict
```

### Run some code 
```bash
uv run auditor.py
# or if you're feeling frisky, run a concurrent audit using threads. 
uv run auditor-conc.py
```

## Create the DB
```bash
python store.py
# or 
uv run store.py
```

### Learn how to interact with the DB
- [db-docs](./docs/db.md)


## TODO
- [x] Add failure column to audit table 
    - [x] ensure the reason is added
- [ ] Add user column (could be some background daemon and not a real person)
- [ ] Make the audits configurable
- [ ] Improve the exception handling 
- [ ] Pull queries out into their own file

