# Deploying this Django project on Vercel

## What’s included

- **`vercel.json`** – Build command, install command, Python 3.12 runtime, and rewrites so all traffic is handled by the Django app.
- **`api/wsgi.py`** – Vercel serverless entry point that exposes the Django WSGI app as `app`.
- **WhiteNoise** – Serves static files in production (no separate static hosting).
- **`.vercelignore`** – Keeps `venv`, `.env`, and other unneeded files out of the deployment.

## Deploy steps

1. **Install Vercel CLI (optional):**  
   `npm i -g vercel`

2. **Link and deploy:**  
   From the project root run `vercel` (or connect the repo in the Vercel dashboard and deploy from Git).

3. **Set environment variables** in the Vercel project (Dashboard → Project → Settings → Environment Variables). Use the same names as in your local `.env`, for example:
   - `SECRET_KEY`
   - `DEBUG` (e.g. `False` for production)
   - `DATABASE_NAME`, `DATABASE_USER`, `DATABASE_PASSWORD`, `DATABASE_HOST`, `DATABASE_PORT` (or use `USE_SQLITE=true` only for very minimal testing; SQLite on Vercel is not recommended for real use)
   - `UNIVERSAL_AIR_API_*`, `TRAVEL_BOUTIQUE_*`, `RAZORPAY_*`, `EMAIL_*`, and any other variables your app reads from `os.getenv(...)`.

4. **Database:** Use an external PostgreSQL (e.g. Vercel Postgres, Neon, Supabase, Railway). Do not rely on SQLite for production on Vercel.

5. **Redeploy** after changing environment variables so the new values are applied.

## Build and runtime

- **Install:** `pip install -r requirements.txt`
- **Build:** `python manage.py collectstatic --noinput --clear`
- **Runtime:** All requests are rewritten to `/api/wsgi`, which runs your Django app (including admin, static files via WhiteNoise, and media if you configure external storage).

## Optional: custom domain

In Vercel, add your domain (e.g. ticketclue.com). Then add that origin to `CSRF_TRUSTED_ORIGINS` in `flightApp/settings.py` if it’s not already there.
