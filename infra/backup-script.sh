#!/bin/bash

ntfy_topic="https://ntfy.mckay.one/docker-backup-script"
backup_root="/docker/infra/ct_backups"


#curl -d "Beginning Docker backup" https://ntfy.mckay.one/docker-backup-script
SECONDS=0

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

logfile=`cat $backup_root/backups.log`
if [[ $logfile == *ERROR* ]]; then
  curl -H "Title: Error in backup" -H "Tags: rotating_light" -d "Docker backup has completed, but an error was found. Check the log file for more details. Backup took $SECONDS seconds." $ntfy_topic
else
  curl -H "Title: Backup Successfull" -H "Tags: tada" -d "Docker backup complete. Backup took $SECONDS seconds" $ntfy_topic
  # If no errors are found we can archive the current logfile.
  echo "" >> $backup_root/backup-archive.log && echo "-----$(date)-----" >> $backup_root/backup-archive.log
  cat $backup_root/backups.log >> $backup_root/backup-archive.log
  echo "" > $backup_root/backups.log
fi
