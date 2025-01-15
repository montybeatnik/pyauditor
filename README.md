# Auditor
Run audits against the network infrastructure. 

## Overview
There are times when we'll want to run audits against our fleet of infrastructure devices. This is the begining of a framework to do just that. 

## Decisions
- dependency management with uv: I decided to use uv to manage the project. I've been using a VM as I wasn't able to install uv on my work mac. It's buit with Rust and is blazing fast! 
- type hinting: because...well, why not? In the absence of a strongly typed language, this is the best we've got. 
- netmiko: because it's been around a while and it's probably not going to change drastically out from underneath us. 
- sqlite: it doesn't require us to install anything. See above. 

## Contributing
There are 4 branches. 
- development
- staging
- production
- main

If you want to add a feature or fix a bug, branch off of development and submit a merge request. If the changes are approved, we'll merge them into development and test. 

I'd like to stricly enforce unit testing, but I don't think we're there yet (I know, that's a terrible excuse!)

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

