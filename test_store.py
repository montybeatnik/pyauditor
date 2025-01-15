from getpass import getuser
from store import Auditor
import models 

def test_create_db():
    auditor = Auditor("audits.db")
    auditor.create_table()
    assert auditor.table_exists("audits") == True


def test_add_audit():
    auditor = Auditor("audits.db")
    user = getuser()
    audit = models.Audit(
        user=user,
        device=models.Device(
            hostname="test", 
            mgmt_addr="1.1.1.1", 
            username="user", 
            password="pass"
        ),        
        cmd="test command",
        output="{'msg':'some msg'}",
        was_successful=True,
        failure_reason=None,
    )
    auditor.insert_audit(audit)
