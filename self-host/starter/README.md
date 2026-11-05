# Fresh Synapse starter — reference configuration

Generic examples only. No accounts, tokens, private hostnames, signing keys or database snapshots included. Uses official upstream Synapse, PostgreSQL and Caddy containers; this is NOT a preconfigured Syndicate server image.

Follow https://synmessenger.com/self-host/ for OS installation, initialization, DNS/TLS, users, backups, updates, and UpCloud VM/Kubernetes guidance. Current image versions at publication: Synapse1.164.2 / PostgreSQL16 / Caddy2.11.9. Review upstream security releases and pin exact image digests for reproducible production deployment.

1. Work in Bash (WSL2 Ubuntu on Windows). Docker Desktop must be running on Windows/macOS. On Linux use Docker Engine plus Compose plugin.
2. Set your permanent SERVER_NAME in a private `.env`; generate a unique POSTGRES_PASSWORD. Never publish `.env`.
3. Generate fresh Synapse config in its named volume, then run configure.py as documented. Do not run configure.py against an existing database or treat this as a database migration.
4. Validate with `docker compose config --quiet`, start `docker compose up -d`, check logs and public HTTPS discovery, create an admin locally, then connect Syndicate.
5. This is a single-instance reference, not HA, a managed service, a TURN/SFU deployment or a promise of production capacity. PostgreSQL/data volumes and server signing keys need off-host backups. Server backups do not replace clients' encrypted-room recovery keys.

The compose file binds 8008 to host loopback and does not publish PostgreSQL. The proxy blocks public Synapse Admin API access; use local container tools. Ports80/443 require real DNS/public reachability for automatic trusted HTTPS. No firewall changes are made by these files. Docker-published ports can bypass some host firewall tools: use provider firewall rules and verify externally.

Stop using `docker compose down` without `-v` to preserve named volumes. Never delete volumes to repair an established homeserver. `admin.py` performs destructive account deactivation only after interactive confirmation; it is not room membership management. Keep a second admin and validate backups before administrative changes.
