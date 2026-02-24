#!/usr/bin/python3

# Purpose: Create a backup for Traefik
# Author & Copywright: Josiah McKay / 2026

# This container has all content stored in volumes. No database to backup.

import sys
sys.path.append('/docker/backup')
import backup_utils as bu

file_root = "/docker/traefik/"

# Encrypt .env file
env_file = f"{file_root}.env"
enc_file = f"{file_root}encrypted.env"

bu.encrypt_file(env_file, enc_file)

# Encrypt acme.json file
acme_file = f"{file_root}config/acme.json"
enc_acme_file = f"{file_root}config/encrypted-acme.json"

bu.encrypt_file(acme_file, enc_acme_file)
