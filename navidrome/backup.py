#!/usr/bin/python3

# Purpose: Create a backup for Navidrome
# Author & Copywright: Josiah McKay / 2026
def run():
    import sys, subprocess
    sys.path.append('/docker/infra')
    import backup_utils as bu

    file_root = "/docker/navidrome/"
    backup_path = "/docker/infra/ct_backups/navidrome/"


    ## Backup Database
    cmd_backup = ["docker", "compose", "-f", f"{file_root}docker-compose.yml", "run" , "-d", "-q", "--remove-orphans", "navidrome", "backup", "create"]
    cmd_prune = ["docker", "compose", "-f", f"{file_root}docker-compose.yml", "run", "-d", "-q", "--remove-orphans", "navidrome", "backup", "prune"]
    cmd_dk_cp = ["docker", "cp", "navidrome-navidrome-1:/data/backups/", f"{backup_path}"]

    subprocess.run(cmd_backup)
    subprocess.run(cmd_prune)
    subprocess.run(cmd_dk_cp)

    # Encrypt .env file
    env_file = f"{file_root}.env"
    enc_file = f"{file_root}encrypted.env"

    conf_file = f"{file_root}navidrome.yml"
    enc_conf_file = f"{file_root}encrypted-navidrome.yml"

    bu.encrypt_file(env_file, enc_file)
    bu.encrypt_file(conf_file, enc_conf_file)


run()