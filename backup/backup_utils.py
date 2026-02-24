import subprocess, os, sys
from datetime import date, timedelta, datetime

now = datetime.now()
date_format = now.strftime('%Y-%m-%d_%H-%M')

def db_backup(cmd, output_dir):
    outputfile = f"{output_dir}{date_format}.sql"

    with open(outputfile, "w") as file:
        db_result = subprocess.run(cmd, stdout=file)

    if db_result.returncode == 0:
        print("DB Backup Successfull!")
    else:
        print("Error in backup. Try again")

def delete_older(backup_root, days=30):
    cutoff_time = (now - timedelta(days=days)).timestamp()
    file_list = os.listdir(path=backup_root)
    removed_any = False
    for backup in file_list:
        path = backup_root + backup
        if os.path.getctime(path) < cutoff_time:
            os.remove(path)
            removed_any = True
            print(f"Removed {path}")
    if not removed_any:
        print("No files deleted")

def encrypt_file(plain_path, encrypted_path):
# plain_path is the absolute path of the file to be encrypted.
# encrypted_path is the absolute path of the file after it has been encrypted.

    enc_cmd = ["sops", "-e", "--age", "age1u2dqqhqrhpj0m8g3d36vrp6tpdyjnzqj0kt5cvuc0fa3qt8daqusrpnfp7", f"{plain_path}"]

    with open(encrypted_path, "w") as file:
        enc_result = subprocess.run(enc_cmd, stdout=file)

    if enc_result.returncode == 0:
        print(f"{plain_path} Encryption Successfull!")
    else:
        print("Error in .env Encryption. Try again")

def write_dated_file(content, filepath, extention, mode='w', prefix=''):
    with open(f'{filepath}{prefix}{date_format}.{extention}', mode) as dated_file:
        dated_file.write(content)
        print("write finished")
