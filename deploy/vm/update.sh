#!/usr/bin/env bash
# Pull the latest main and restart the API.  sudo bash /opt/property-search/deploy/vm/update.sh
set -euo pipefail
APP_DIR=/opt/property-search
APP_USER=propsearch
BRANCH=${BRANCH:-main}

run() { sudo -u "$APP_USER" bash -c "cd $APP_DIR/backend && $*"; }
sudo -u "$APP_USER" git -C "$APP_DIR" pull --ff-only origin "$BRANCH"
run ".venv/bin/pip install -q -r requirements.txt"
run ".venv/bin/python manage.py migrate --noinput"
run ".venv/bin/python manage.py collectstatic --noinput -v0"
systemctl restart property-search
sleep 2
curl -fsS -o /dev/null -w "/countries -> %{http_code}\n" http://127.0.0.1:8000/countries
