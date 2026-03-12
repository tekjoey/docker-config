#!/usr/bin/python3

# Purpose: Create a backup for Calibre-Web
# Author & Copywright: Josiah McKay / 2026

# This container has all content stored in volumes. No database to backup.

import sys
sys.path.append('/docker/infra')
import backup_utils as bu

file_root = "/docker/homepage/"

# Encrypt .env & settings file
env_file = f"{file_root}.env"
enc_file = f"{file_root}encrypted.env"

settings_file = f"{file_root}config/settings.yaml"
enc_settings_file = f"{file_root}config/encrypted_settings.yaml"


bu.encrypt_file(env_file, enc_file)
bu.encrypt_file(settings_file, enc_settings_file)
