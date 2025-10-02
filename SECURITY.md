# Security & Secrets Policy

- **Secrets only in `.env` on VPS** (or container secrets). Never commit real `.env`.
- **Data/DB/logs** only in `data/` (gitignored).
- Weekly secret scans with **Gitleaks** (see GitHub Action).
- If a token leaks, rotate immediately and purge commit history (GitHub UI + force push to remove leaks from mirror).
- Auto-clean old events via future cron/APScheduler task.
