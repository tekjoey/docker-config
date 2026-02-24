#!/usr/bin/python3

# Purpose: Create a backup for Dozzel
# Author & Copywright: Josiah McKay / 2026

# This container has all content stored in volumes. No database to backup.

import sys
sys.path.append('/docker/backup')
import backup_utils as bu

file_root = "/docker/dozzel/"
