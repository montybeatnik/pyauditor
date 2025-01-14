import os
import auditor

if __name__ == "__main__":
    threads = list()
    cmd = "show interfaces terse ge*"
    un = os.getenv("SSH_USER")
    pw = os.getenv("SSH_PASSWORD")
    devices = auditor.get_devices(un=un, pw=pw)
    auditor.run_audit_concurrently(devices, cmd)
    