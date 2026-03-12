#!/bin/bash

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

curl -d "Backup Complete! Backup took $SECONDS seconds" https://ntfy.mckay.one/docker-backup-script

