from dataclasses import dataclass

@dataclass
class Device:
    hostname: str
    mgmt_addr: str
    username: str
    password: str
