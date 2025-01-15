from dataclasses import dataclass

@dataclass
class Device:
    hostname: str
    mgmt_addr: str
    username: str
    password: str

@dataclass
class Audit:
    user: str # TODO: this should be a PK pointing to user's table. 
    device: Device
    cmd: str
    output: str
    was_successful: bool
    failure_reason: str    