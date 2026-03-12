#!/usr/bin/python3

# Purpose: Create a backup for Lube Logger
# Author & Copywright: Josiah McKay / 2026

# This container has all content stored in volumes. No database to backup.
# provides an api to backup /api/makebackup


import sys, requests
sys.path.append('/docker/infra')
import backup_utils as bu

file_root = "/docker/lube-logger/"
backup_root = "lube-logger/"

# Encrypt .env file
env_file = f"{file_root}.env"
enc_file = f"{file_root}encrypted.env"

bu.encrypt_file(env_file, enc_file)

# Download backup
site_root = "https://cars.mckay.one/"
api_path = "/api/makebackup"

tmp = requests.get(site_root + api_path)
zip_path = tmp.text.strip('"')
backup = requests.get(site_root + zip_path)
bu.write_dated_file(backup.content, backup_root, 'zip', mode='wb', prefix='backup')



