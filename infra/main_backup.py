import sys, importlib
from pathlib import Path
sys.path.append('/docker/infra')
import backup_utils as bu

def run_backup(path):
    spec = importlib.util.spec_from_file_location("backup_module", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    try:
        module.run()
        print(f"{path} succeeded")
    except Exception as e:
        print(f"{path} failed: {e}")

for script in Path("/docker").rglob("backup.py"):
    print(script)
    run_backup(script)

# import backup_utils as bu


# def test_error(num):
#     if num > 3:
#         raise bu.BackupError("Not less than 3", severity="ERROR", container="test")
# try:
#     bu.db_backup(["docker", "exec", "authentik-postgresql-1", "pg_dump", "-U", "authentik", "authentik"], "testers/", ct="Test")
# except bu.BackupError as e:
#    e.log_error(ntfy=True)


# print("\n\n\n----------\nthis runs after the error\n----------\n\n")
