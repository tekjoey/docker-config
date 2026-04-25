#!/usr/bin/python3
import sys, importlib, requests
from pathlib import Path
sys.path.append('/docker/infra')
import backup_utils as bu

fail = False

def run_backup(path):
    spec = importlib.util.spec_from_file_location("backup_module", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    try:
        bu.log("DEBUG", "MAIN", f"Beginning {path}")
        module.run()
        bu.log("INFO", "MAIN", f"{path} succeeded")
    except Exception as e:
        bu.log("ERROR", "MAIN", f"{path} failed: {e}")
        fail = True

bu.log("INFO", "MAIN", "Beginning backup")

for script in Path("/docker").rglob("backup.py"):
    run_backup(script)


data = f"Backup complete. {'No errors found.' if not fail else 'Errors found.'}"
bu.log("INFO", "MAIN", data, ntfy=True)

