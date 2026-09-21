# Deployment

```
browser ──https──> Vercel (frontend/, static build)
   │
   └──https──> Tailscale Funnel  https://<vm>.<tailnet>.ts.net
                  │  (TLS terminated here, forwards with X-Forwarded-Proto)
                  └──http──> gunicorn 127.0.0.1:8000 on the LAN VM ──> PostgreSQL (same VM)
```

The backend runs on a VM on the local network with no domain and no port
forwarding. Tailscale Funnel gives it a stable public HTTPS hostname with a
real certificate; HTTPS is required because the Vercel site is HTTPS and
browsers block `http://` API calls and images from it (mixed content).

## 1. Prepare the VM

Ubuntu 22.04+/Debian 12+, 1 vCPU / 1 GB RAM is plenty. It needs outbound
internet only.

## 2. Install the API

```
curl -fsSLO https://raw.githubusercontent.com/The-Home-Hive/property-search-prototype/main/deploy/vm/bootstrap.sh
sudo CORS_ORIGINS=https://<project>.vercel.app bash bootstrap.sh
```

The script only adds packages (`--no-upgrade`), binds to loopback, and aborts
if port 8000 is taken, so it is safe alongside other services on the host.

This installs Postgres, clones the repo to `/opt/property-search`, generates
`/opt/property-search/.env` (random secret key and DB password), runs
migrations and every seed command in the required order, and starts the
`property-search` systemd service on `127.0.0.1:8000`.

## 3. Expose it with Tailscale Funnel

```
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up --accept-dns=false     # log in via the printed URL; leave the host's DNS alone
sudo tailscale funnel --bg 8000          # first run prints a link to enable Funnel for the tailnet
tailscale funnel status                  # shows https://<vm>.<tailnet>.ts.net
```

Then put that hostname into `/opt/property-search/.env`:

```
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,<vm>.<tailnet>.ts.net
DJANGO_CSRF_TRUSTED_ORIGINS=https://<vm>.<tailnet>.ts.net
```

`sudo systemctl restart property-search`, and check from any machine:
`curl https://<vm>.<tailnet>.ts.net/countries`.

## 4. Deploy the frontend on Vercel

Import the GitHub repo in Vercel → **Root Directory: `frontend`** (framework
preset Vite is detected; build `npm run build`, output `dist`). Add one
environment variable (Production and Preview):

```
VITE_API_BASE_URL=https://<vm>.<tailnet>.ts.net
```

It is baked in at build time, so changing it needs a redeploy.

## 5. Allow the Vercel origin

Back on the VM, in `/opt/property-search/.env`:

```
DJANGO_CORS_ALLOWED_ORIGINS=https://<project>.vercel.app
DJANGO_CORS_ALLOWED_ORIGIN_REGEXES=^https://<project>-.*\.vercel\.app$
```

The regex is optional; it admits Vercel preview deployments. Restart the
service and load the Vercel URL. See `vm/env.production.example` for the full
file.

## Updating

Pushes to `main` redeploy the frontend automatically. For the backend:

```
sudo bash /opt/property-search/deploy/vm/update.sh
```

It pulls `main`, installs dependencies, migrates, collects static files and
restarts. Re-run the seed commands (backend/README.md) if a change touches
seed data.

## Operating

| Task | Command |
|---|---|
| Logs | `journalctl -u property-search -f` |
| Restart | `sudo systemctl restart property-search` |
| Funnel off / on | `sudo tailscale funnel --bg 8000 off` / `sudo tailscale funnel --bg 8000` |
| DB shell | `sudo -u postgres psql property_search` |
