import subprocess, os, sys, logging, requests
from datetime import date, timedelta, datetime

logger = logging.getLogger(__name__)
file_h = logging.FileHandler("/docker/infra/docker-backup.log")
console_h = logging.StreamHandler()
format_str = "%(asctime)s - %(levelname)s: %(message)s"
logging.basicConfig(
    handlers = [file_h, console_h],
    encoding='utf-8', 
    level=logging.INFO,
    format=format_str,
    datefmt='%m/%d/%Y %H:%M:%S'
)

now = datetime.now()
date_format = now.strftime('%Y-%m-%d_%H-%M')
backup_root = "/docker/infra/ct_backups/"

def log(level, ct, msg):
  message = f"{ct} - {msg}"
  match level:
      case "DEBUG":
          logger.debug(message)
      case "INFO":
          logger.info(message)
      case "WARNING":
          logger.warning(message)
          notify(level, message)
      case "ERROR":
          logger.error(message)
          notify(level, message)
      case "CRITICAL":
          logger.critical(message)
          notify(level, message)
      case "_":
          logger.warning("Unknown level message")
          notify(level, message)

def notify(level, message, headers={"Tags": "loudspeaker"}):
    ntfy_topic = "https://ntfy.mckay.one/docker-backup-script"
    requests.post(
        ntfy_topic,
        data=f"{level}: {message}",
        headers=headers
        )


def db_backup(cmd, ct, root=backup_root):
    outputfile = f"{root}{ct.lower()}/{date_format}.sql"

    with open(outputfile, "w") as file:
        db_result = subprocess.run(cmd, stdout=file)
        
    log("DEBUG", ct, f"Return code from DB backup is {db_result.returncode}")
    
    if db_result.returncode == 0:
        log("INFO", ct, f"DB was backup up successfully")
    else:
        log("WARNING", ct, f"DB failed to backup")

def delete_older(ct, days=30, root=backup_root):
    backup_path = f"{root}{ct}/"
    cutoff_time = (now - timedelta(days=days)).timestamp()
    file_list = os.listdir(path=backup_path)
    log("DEBUG", ct, f"Found {len(file_list)} files in {backup_path} older than {days} days")
    removed_any = False
    for backup in file_list:
        path = backup_path + backup
        log("DEBUG",ct, f"Checking if {path} is older than {cutoff_time}")
        if os.path.getctime(path) < cutoff_time:
            os.remove(path)
            removed_any = True
            log("INFO", ct, f"Removed {path}")
    if not removed_any:
        log("INFO", ct, f"No files deleted")

def encrypt_file(plain_path, encrypted_path, ct="Temp"):
# plain_path is the absolute path of the file to be encrypted.
# encrypted_path is the absolute path of the file after it has been encrypted.

    enc_cmd = ["sops", "-e", "--age", "age1u2dqqhqrhpj0m8g3d36vrp6tpdyjnzqj0kt5cvuc0fa3qt8daqusrpnfp7", f"{plain_path}"]

    with open(encrypted_path, "w") as file:
        enc_result = subprocess.run(enc_cmd, stdout=file)
        
    log("DEBUG", ct, f"Return code from {plain_path} encryption is {enc_result.returncode}")
    
    if enc_result.returncode == 0:
        log("INFO", ct, f"Encrypted {plain_path}")
    else:
        log("WARNING", ct, f"Unable to encrypt {plain_path}")

def write_dated_file(content, output_path, extention, mode='w', prefix='', root=backup_root):
    with open(f'{root}{output_path}{prefix}{date_format}.{extention}', mode) as dated_file:
        dated_file.write(content)
        log("INFO", None, f"Finished writing {dated_file.name}")
        
        
