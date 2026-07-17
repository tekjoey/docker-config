#!/usr/bin/python3

# Purpose: Create a backup for Vikunja
# Author & Copywright: Josiah McKay / 2026

def run():
    import backup_utils as bu

    file_root = "/docker/vikunja/"
    backup_root = "vikunja/"
    ct = "Vikunja"

    ## Backup Database
    cmd = ["docker", "exec", "vikunja-db", "pg_dump", "-U", "vikunja", "vikunja"]

    bu.db_backup(cmd, ct)

    # Delete old files
    bu.delete_older(ct)


    # Encrypt .env file
    env_file = f"{file_root}.env"
    enc_file = f"{file_root}encrypted.env"

    bu.encrypt_file(env_file, enc_file, ct=ct)


if __name__ == "__main__":
    run()
