# CLMS Cloud Deployment Guide

This document provides step-by-step instructions to deploy CLMS to Render.com.

## Prerequisites

1. A GitHub account with access to the CLMS repository
2. A Render.com account (free tier available)
3. Git installed locally

## Step 1: Push Code to GitHub

The application has been prepared for cloud deployment. Push the changes to GitHub:

```bash
cd /c:/Users/HP/Documents/CLMS/06_Prototype
git push origin master
```

This will push:
- Updated `web_app.py` with environment variable support
- Updated `requirements.txt` with `gunicorn`
- New `Procfile` for Render
- New `render.yaml` for deployment configuration
- `.env.example` showing required environment variables
- `database/clms.db` (the application database with existing data)

## Step 2: Create Render.com Service

1. Log in to [Render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Select "Build and deploy from a Git repository"
4. Connect your GitHub account and select the CLMS repository
5. Fill in the service details:
   - **Name**: `clms` (or any name you prefer)
   - **Region**: Choose the closest region to your users
   - **Branch**: `master`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn -b 0.0.0.0:$PORT -w 2 -t 120 web_app:app`

6. **Environment Variables**: Add these in the "Environment" section
   - `FLASK_ENV`: `production`
   - `FLASK_SECRET_KEY`: Generate a secure random key (Render can generate this automatically with the "Generate" button)

7. **Plan**: Select "Free" tier (0.5 CPU, 512 MB RAM, 100 GB bandwidth/month)

8. Click "Create Web Service" and wait for deployment (typically 2-3 minutes)

## Step 3: Verify Deployment

Once deployed, Render will provide you with a URL like:
```
https://clms-xxxxx.onrender.com
```

Access this URL and verify:
1. Login page loads with HTTPS
2. Sign in with credentials:
   - Username: `admin`
   - Password: `Admin123` (change after first login!)
3. Dashboard loads
4. All navigation links work

## Step 4: Test All Features

See the testing checklist below.

## Database Persistence

The `clms.db` SQLite database is committed to the repository and deployed with the application.

**Important Notes:**
- The database is stored on Render's ephemeral filesystem
- Each redeploy will have the same database snapshot as committed to GitHub
- If you need permanent data storage, you can:
  - Commit database changes to GitHub
  - Or use Render's Disk service (paid feature)

## Rolling Back

If something goes wrong:
1. Go to Render dashboard for your service
2. Click "Deployments"
3. Find a previous successful deployment
4. Click "Redeploy"

## Environment Configuration

Key environment variables used by CLMS:

| Variable | Default | Purpose |
|----------|---------|---------|
| `FLASK_ENV` | development | Set to `production` in cloud |
| `FLASK_SECRET_KEY` | random | Session encryption key |
| `PORT` | 5000 | Listen port (Render sets this) |
| `FLASK_HOST` | 127.0.0.1 | Bind address (0.0.0.0 in production) |

## Troubleshooting

### "502 Bad Gateway" Error
- Check Render logs: Deployments → View Logs
- Usually means the app crashed during startup
- Verify `FLASK_SECRET_KEY` is set in Environment

### Database Not Persisting
- Changes to the database during a session are stored in Render's ephemeral filesystem
- After redeploy, you get the committed version of `clms.db`
- To save data permanently, commit to Git or use Render Disk

### App Won't Start
- Check Render logs for errors
- Verify all dependencies in `requirements.txt` are correct
- Ensure `web_app.py` is the Flask app entry point

## Scaling Considerations

For higher traffic:
- Upgrade from Free to Starter/Pro tier on Render
- Increase gunicorn workers: `gunicorn -b 0.0.0.0:$PORT -w 4 web_app:app`
- Consider PostgreSQL for data (currently using SQLite)

## Security Checklist

Before sharing the URL publicly:
- [ ] Change default admin password
- [ ] Review user accounts
- [ ] Verify login is required for private pages
- [ ] Check that database backups are available (via Git)
- [ ] Ensure no sensitive data in logs

## URLs to Share

Once deployed:
- **Admin/Team**: `https://clms-xxxxx.onrender.com` (share the full URL)
- **For Adil**: Same URL
- **For Ilham**: Same URL

All users access the same application and share data through the SQLite database.

## Support

For Render.com specific issues: https://render.com/docs
For CLMS specific issues: Check `database/database.py` and Flask logs on Render

---

**Deployment prepared**: August 14, 2026
**Application version**: 1.0.0
**Database included**: Yes (clms.db with demo data)
