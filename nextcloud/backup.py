#!/usr/bin/python3

# Purpose: Create a backup for Nextcloud
# Author & Copywright: Josiah McKay / 2026

# This script curently will only backup the database.
# The `data` and `config` volumes need to be handled as well.

import sys
sys.path.append('/docker/infra')
import backup_utils as bu

file_root = "/docker/nextcloud/"
backup_root = "nextcloud/"


## Backup Database
cmd = ["docker", "exec", "nextcloud-db-1", "pg_dump", "-U", "nextcloud", "nextcloud"]

bu.db_backup(cmd, backup_root)

# Delete old files
bu.delete_older(backup_root)


# Encrypt .env file
env_file = f"{file_root}.env"
enc_file = f"{file_root}encrypted.env"

bu.encrypt_file(env_file, enc_file)
