#!/usr/bin/python3

# Purpose: Create a backup for Authentik
# Author & Copywright: Josiah McKay / 2026

# The database is the only thing that needs to be backed up at this time.
# If the extra media/certificat folders are ever used, they will also have to be backed up.
def run():
  import backup_utils as bu

  file_root = "/docker/authentik/"
  ct = "Authentik"

  ## Backup Database
  cmd = ["docker", "exec", "authentik-postgresql-1", "pg_dump", "-U", "authentik", "authentik"]

  bu.db_backup(cmd, ct)


  # Delete old files
  bu.delete_older(ct)

  # Encrypt .env file
  env_file = f"{file_root}.env"
  enc_file = f"{file_root}encrypted.env"

  bu.encrypt_file(env_file, enc_file, ct=ct)

run()
