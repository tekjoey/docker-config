#!/usr/bin/python3

# Purpose: Create a backup for Homebox
# Author & Copywright: Josiah McKay / 2026

# This container has all content stored in volumes. No database to backup.

import sys
sys.path.append('/docker/backup')
import backup_utils as bu

file_root = "/docker/homebox/"

# Encrypt .env file
env_file = f"{file_root}.env"
enc_file = f"{file_root}encrypted.env"

bu.encrypt_file(env_file, enc_file)
