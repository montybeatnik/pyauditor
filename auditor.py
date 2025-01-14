import os
from netmiko.juniper import JuniperSSH
import threading
import xmltodict
from typing import List

from store import AuditUpdate
import models

def update_store(dev: models.Device, cmd: str, output: str) -> None:
    """
    update_store takes in 
        - a device of type models.Device
        - a cmd of type str
        - output of type str
    It constructs an AuditUpdate and then calls the update method, 
    which updates the store (sqlite DB). 
    """
    audit_update = AuditUpdate(
        device=dev,
        cmd=cmd,
        output=output,
        db="audits.db",
        was_successful=True,
        failure_reason=None,
    )
    audit_update.update()

def update_store_failure(dev: models.Device, cmd: str, failure_reason: str) -> None:
    """
    update_store takes in 
        - a device of type models.Device
        - a cmd of type str
        - output of type str
    It constructs an AuditUpdate and then calls the update method, 
    which updates the store (sqlite DB). 
    """
    audit_update = AuditUpdate(
        device=dev,
        cmd=cmd,
        output=None,
        was_successful=False,
        failure_reason=failure_reason,
        db="audits.db",
    )
    audit_update.update()    

def run_command_and_store_results(dev: models.Device, cmd: str) -> None:
    """
    run_command_and_store_results takes in
        - a dev of type models.Device
        - and a cmd of type string 
    It attempts to log into the device and run the command. 
    If the cmd asks for xml, it will then attempt to parse that output
    into a native python dict. 
    Finally, it will update the store with the results. 
    """
    try:
        jnpr_dev = JuniperSSH(ip=dev.mgmt_addr, username=dev.username, password=dev.password)
        output = jnpr_dev.send_command(cmd)
        if "xml" in cmd:
            output = xmltodict.parse(output)
        update_store(dev, cmd, output)
    # TODO: 
    # Could probably have an array of more specific exceptions
    # to print more meaningful errors.
    except Exception as e:
        # For when we run it concurrently in a separate thread
        update_store_failure(dev, cmd, str(e))


def run_audit(devices: List[models.Device], cmd: str):
    """
    run_audit takes in a list of devices and a command. 
    It loops through the devices, running the command. 
    Then it updates the DB via the store. 
    """
    print(f"running an audit against {len(devices)}")
    for dev in devices:
        print(f"logging into {dev.hostname}...")
        err = run_command_and_store_results(dev, cmd)
        if err != None:
            print(err)

def run_audit_concurrently(devices: List[models.Device], cmd: str):
    """
    run_audit_concurrently takes in a list of devices and a command. 
    It loops through the devices, firing off a thread for each, where each thread
    runs the command against the device. 
    Then it updates the DB via the store. 
    """
    print(f"running an audit against {len(devices)}")
    threads = list()
    for dev in devices:
        thread = threading.Thread(target=run_command_and_store_results, args=(dev, cmd))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

def get_devices(un: str, pw: str) -> List:
    """
    get_devices is a helper function that produces a list of 
    lab devices for testing.
    TODO: this should be a call to netbox or some other DB housing
    network elements.
    """
    devices = [
        models.Device(mgmt_addr="10.0.0.86", username=un, password=pw, hostname="lab-r1"),
        models.Device(mgmt_addr="10.0.0.23", username=un, password=pw, hostname="lab-r2"),
        models.Device(mgmt_addr="10.0.0.212", username=un, password=pw, hostname="lab-r3"),
        models.Device(mgmt_addr="10.0.0.150", username=un, password=pw, hostname="lab-r4"),
        models.Device(mgmt_addr="10.0.0.87", username=un, password=pw, hostname="lab-r5"),
        models.Device(mgmt_addr="10.0.0.24", username=un, password=pw, hostname="lab-r6"),
        models.Device(mgmt_addr="10.0.0.213", username=un, password=pw, hostname="lab-r7"),
        models.Device(mgmt_addr="10.0.0.149", username=un, password=pw, hostname="lab-r8"),
    ]
    return devices


def main():
    # setup the creds
    un = os.getenv("SSH_USER")
    pw = os.getenv("SSH_PASSWORD")
    # currently using the lab devices in my proxmox instance of eve-ng. 
    devices = get_devices(un, pw)  
    cmd = "show system alarms"
    run_audit(devices, cmd)


if __name__ == "__main__":
    main()
