#!/bin/bash

ntfy_topic="https://ntfy.mckay.one/docker-backup-script"
backup_root="/docker/infra/ct_backups"
logfile_path=$backup_root/backups.log

SECONDS=0


# First parameter is log level (info, success, warn, error)
# Second parameter is message
logmessage () {
	echo "$(date +%Y-%m-%d_%H-%M-%S) - $1: $2" >> $logfile_path}

logmessage "INFO" "Begining backup"


# Run backup script for each container.
/docker/authentik/backup.py
/docker/calibre-web/backup.py
/docker/collabora-code/backup.py
/docker/dozzel/backup.py
/docker/homebox/backup.py
/docker/homepage/backup.py
/docker/immich/backup.py
/docker/lube-logger/backup.py
/docker/mealie/backup.py
/docker/miniflux/backup.py
/docker/nextcloud/backup.py
/docker/ntfy/backup.py
/docker/omada/backup.py
/docker/paperless-ngx/backup.py
/docker/traefik/backup.py
/docker/uptime-kuma/backup.py
/docker/vikunja/backup.py

logmessage "INFO" "Finished Backup. Backup took $SECONDS seconds"

logfile=`cat $logfile_path`
if [[ $logfile == *ERROR* ]]; then
  curl -H "Title: Error in backup" -H "Tags: rotating_light" -d "Docker backup has completed, but an error was found. Check the log file for more details. Backup took $SECONDS seconds." $ntfy_topic
else
  curl -H "Title: Backup Successfull" -H "Tags: tada" -d "Docker backup complete. Backup took $SECONDS seconds" $ntfy_topic
  # If no errors are found we can archive the current logfile.
  echo "" >> $backup_root/backup-archive.log && echo "-----$(date)-----" >> $backup_root/backup-archive.log
  cat $logfile_path >> $backup_root/backup-archive.log
  echo "" > $logfile_path
fi
