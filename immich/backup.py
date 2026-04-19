#!/usr/bin/python3

# Purpose: Create a backup for Homebox
# Author & Copywright: Josiah McKay / 2026

def run():
    import backup_utils as bu

    file_root = "/docker/immich/"
    ct = "Immich"


    ## Backup Database
    cmd = ["docker", "exec", "immich_postgres", "pg_dump", "-U", "postgres", "immich"]

    bu.db_backup(cmd, ct)

    # Delete old files
    bu.delete_older(ct)

    # Encrypt .env file
    env_file = f"{file_root}.env"
    enc_file = f"{file_root}encrypted.env"

    bu.encrypt_file(env_file, enc_file, ct=ct)


run()
