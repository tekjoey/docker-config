#!/usr/bin/python3

# Purpose: Create a backup for Vikunja
# Author & Copywright: Josiah McKay / 2026

# This script curently will only backup the database.

import sys
sys.path.append('/docker/infra')
import backup_utils as bu

file_root = "/docker/vikunja/"
backup_root = "vikunja/"


## Backup Database
cmd = ["docker", "exec", "vikunja_db", "pg_dump", "-U", "vikunja", "vikunja"]

bu.db_backup(cmd, backup_root)

# Delete old files
bu.delete_older(backup_root)


# Encrypt .env file
env_file = f"{file_root}.env"
enc_file = f"{file_root}encrypted.env"

bu.encrypt_file(env_file, enc_file)
