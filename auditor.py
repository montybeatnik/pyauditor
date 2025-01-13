import os
from netmiko.juniper import JuniperSSH
import xmltodict

from store import AuditUpdate
import models


def get_software(dev:models.Device) -> str:
    """
    get_software takes in a device, which is of type models.Device, 
    it logs into the device, runs the command, converst the xml string 
    to a dict, and finally returns it. 
    """
    jnpr_dev = JuniperSSH(ip=dev.mgmt_addr, username=dev.username, password=dev.password)
    cmd = "show version | display xml"
    ver = ""
    try:
        output = jnpr_dev.send_command(cmd)
        ver = xmltodict.parse(output)
    # TODO: 
    # Could probably have an array of more specific exceptions
    # to print more meaningful errors.
    except Exception as e:
        print(f"something went wrong {e}")
    return ver

def main():
    # setup the creds
    un = os.getenv("SSH_USER")
    pw = os.getenv("SSH_PASSWORD")
    # currently using the lab devices in my proxmox instance of eve-ng. 
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
    # loop through the devices, and run the get_software func, grabbing the JunOS version.  
    for dev in devices:
        output = get_software(dev)
        ver = output["rpc-reply"]["software-information"]["package-information"]["comment"]
        # prepare the data so we can add it to the DB at the store layer. 
        audit_update = AuditUpdate(
            device=dev,
            cmd="show version",
            output=ver,
            db="audits.db",
        )
        audit_update.update()




if __name__ == "__main__":
    main()
