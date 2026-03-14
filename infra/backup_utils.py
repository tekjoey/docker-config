import subprocess, os, sys
from datetime import date, timedelta, datetime

now = datetime.now()
date_format = now.strftime('%Y-%m-%d_%H-%M')
backup_root = "/docker/infra/ct_backups/"

def log(level, message):
  print(f"{date_format} - {level}: {message}\n")
  with open(f"{backup_root}backups.log", "a") as logfile:
    logfile.write(f"{date_format} - {level}: {message}\n")


#log("INFO", "This is a test of the logging system")

def db_backup(cmd, output_dir, root=backup_root):
    outputfile = f"{root}{output_dir}{date_format}.sql"

    with open(outputfile, "w") as file:
        db_result = subprocess.run(cmd, stdout=file)

    if db_result.returncode == 0:
        log("SUCCESS", f"{output_dir} DB was backup up successfully")
    else:
        log("FAILURE", f"{output_dir} DB failed to backup")

def delete_older(backup_dir, days=30, root=backup_root):
    backup_path = root + backup_dir
    cutoff_time = (now - timedelta(days=days)).timestamp()
    file_list = os.listdir(path=backup_path)
    removed_any = False
    for backup in file_list:
        path = backup_path + backup
        if os.path.getctime(path) < cutoff_time:
            os.remove(path)
            removed_any = True
            log("INFO", f"{backup_dir}: Removed {path}")
    if not removed_any:
        log("INFO", f"{backup_dir}: No files deleted")

def encrypt_file(plain_path, encrypted_path):
# plain_path is the absolute path of the file to be encrypted.
# encrypted_path is the absolute path of the file after it has been encrypted.

    enc_cmd = ["sops", "-e", "--age", "age1u2dqqhqrhpj0m8g3d36vrp6tpdyjnzqj0kt5cvuc0fa3qt8daqusrpnfp7", f"{plain_path}"]

    with open(encrypted_path, "w") as file:
        enc_result = subprocess.run(enc_cmd, stdout=file)

    if enc_result.returncode == 0:
        log("SUCCESS", f"Encrypted {plain_path}")
    else:
        log("FAILURE" f"Unable to encrypt {plain_path}")

def write_dated_file(content, output_path, extention, mode='w', prefix='', root=backup_root):
    with open(f'{root}{output_path}{prefix}{date_format}.{extention}', mode) as dated_file:
        dated_file.write(content)
        log("INFO", f"Finished writing {dated_file.name}")

#write_dated_file("This is a test", "test", "txt")
