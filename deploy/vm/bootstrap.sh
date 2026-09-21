#!/usr/bin/env bash
# First-time setup of the property search API on a fresh Ubuntu/Debian VM.
# Run as a sudo-capable user:  sudo bash bootstrap.sh
# Safe to re-run: existing user, database, .env and checkout are left in place.
set -euo pipefail

REPO_URL=https://github.com/The-Home-Hive/property-search-prototype.git
BRANCH=${BRANCH:-main}
APP_DIR=/opt/property-search
APP_USER=propsearch
DB_NAME=property_search
DB_USER=property_search

echo "==> Installing system packages"
apt-get update -qq
apt-get install -y -qq git python3 python3-venv postgresql curl openssl

echo "==> Creating service user and checkout"
id -u "$APP_USER" >/dev/null 2>&1 || useradd --system --home "$APP_DIR" --shell /usr/sbin/nologin "$APP_USER"
if [ ! -d "$APP_DIR/.git" ]; then
    git clone --branch "$BRANCH" "$REPO_URL" "$APP_DIR"
fi
chown -R "$APP_USER:$APP_USER" "$APP_DIR"

echo "==> Creating database"
if [ ! -f "$APP_DIR/.env" ]; then
    DB_PASSWORD=$(openssl rand -hex 24)
    SECRET_KEY=$(openssl rand -base64 48 | tr -d '\n')
    sudo -u postgres psql -v ON_ERROR_STOP=1 -q <<SQL
DO \$\$ BEGIN
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = '$DB_USER') THEN
    CREATE ROLE $DB_USER LOGIN PASSWORD '$DB_PASSWORD';
  ELSE
    ALTER ROLE $DB_USER PASSWORD '$DB_PASSWORD';
  END IF;
END \$\$;
SQL
    sudo -u postgres psql -tAc "SELECT 1 FROM pg_database WHERE datname='$DB_NAME'" | grep -q 1 \
        || sudo -u postgres createdb -O "$DB_USER" "$DB_NAME"

    cat > "$APP_DIR/.env" <<ENV
DJANGO_SECRET_KEY=$SECRET_KEY
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_CSRF_TRUSTED_ORIGINS=
DJANGO_BEHIND_HTTPS_PROXY=True
DJANGO_CORS_ALLOWED_ORIGINS=
DJANGO_CORS_ALLOWED_ORIGIN_REGEXES=
DATABASE_URL=postgresql://$DB_USER:$DB_PASSWORD@localhost:5432/$DB_NAME
ENV
    chown "$APP_USER:$APP_USER" "$APP_DIR/.env"
    chmod 600 "$APP_DIR/.env"
else
    echo "    .env exists, leaving database credentials alone"
fi

echo "==> Installing Python dependencies"
sudo -u "$APP_USER" python3 -m venv "$APP_DIR/backend/.venv"
sudo -u "$APP_USER" "$APP_DIR/backend/.venv/bin/pip" install -q -r "$APP_DIR/backend/requirements.txt"

echo "==> Migrating and seeding (order matters, see backend/README.md)"
manage() { sudo -u "$APP_USER" bash -c "cd $APP_DIR/backend && .venv/bin/python manage.py $*"; }
manage migrate --noinput
manage seed_locations
manage seed_prices
manage loaddata properties_seed
manage seed_property_images
manage seed_property_descriptions
manage collectstatic --noinput -v0

echo "==> Installing systemd service"
cp "$APP_DIR/deploy/vm/property-search.service" /etc/systemd/system/
systemctl daemon-reload
systemctl enable --now property-search
systemctl restart property-search
sleep 2
curl -fsS -o /dev/null -w "    local health check: /countries -> %{http_code}\n" http://127.0.0.1:8000/countries

cat <<MSG

Done. Next: expose it with Tailscale Funnel and fill in the hostnames in
$APP_DIR/.env — see deploy/README.md, step 3.
MSG
