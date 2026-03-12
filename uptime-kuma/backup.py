#!/usr/bin/python3

# Purpose: Create a backup for Uptime Kuma
# Author & Copywright: Josiah McKay / 2026

# This container has all content stored in volumes. No database to backup.
# No .env file to back up

import sys
sys.path.append('/docker/infra')
import backup_utils as bu

file_root = "/docker/uptime-kuma/"
