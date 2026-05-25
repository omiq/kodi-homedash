#!/usr/bin/env bash
# Deploy script.homedash straight into the LibreELEC box over SSH.
#
# Why not "Install from zip"? Kodi reads a zip over HTTP using byte-range
# requests; Python's http.server ignores Range, so local-served zips fail with
# "Error getting zip://". rsync over SSH sidesteps zips entirely.
#
# Usage:
#   ./deploy.sh                 # sync code; relaunch the add-on in Kodi to see it
#   ./deploy.sh --restart       # sync + restart Kodi (needed when addon.xml,
#                               # the service, or other extension points change)
#   KODI_HOST=root@1.2.3.4 ./deploy.sh
set -euo pipefail

HOST="${KODI_HOST:-root@192.168.0.106}"
REMOTE_RSYNC="/storage/.kodi/addons/virtual.network-tools/bin/rsync"
ADDON_DIR="/storage/.kodi/addons/script.homedash"

rsync -a --delete \
  --rsync-path="$REMOTE_RSYNC" \
  --exclude='__pycache__' --exclude='*.pyc' --exclude='.DS_Store' \
  script.homedash/ "$HOST:$ADDON_DIR/"
echo "Synced to $HOST:$ADDON_DIR"

if [ "${1:-}" = "--restart" ]; then
  echo "Restarting Kodi (screen will blank ~30s)..."
  ssh "$HOST" 'systemctl restart kodi'
  echo "Done."
else
  echo "Code synced. Relaunch the add-on in Kodi to pick it up."
  echo "(addon.xml / service changes need: ./deploy.sh --restart)"
fi
