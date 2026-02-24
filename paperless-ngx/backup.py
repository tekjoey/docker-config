#!/usr/bin/python3

# Purpose: Create a backup for Paperless-NGX
# Author & Copywright: Josiah McKay / 2026

# This script curently will only backup the database.
# All the other volumes still need to be backed up

import sys
sys.path.append('/docker/backup')
import backup_utils as bu

file_root = "/docker/paperless-ngx/"
backup_root = "/docker/backup/paperless-ngx/"

## Backup Database
cmd = ["docker", "exec", "paperless_db", "pg_dump", "-U", "paperless", "paperless"]

bu.db_backup(cmd, backup_root)

# Delete old files
bu.delete_older(backup_root)

# Encrypt .env file
env_file = f"{file_root}.env"
enc_file = f"{file_root}encrypted.env"

bu.encrypt_file(env_file, enc_file)
