# PhotoFindr Deployment Guide

Complete guide to deploying PhotoFindr to production using free hosting tiers.

## Architecture Overview

- **Frontend**: Vercel (free tier)
- **Backend**: Render (free tier)
- **Database**: Supabase (already configured)

Total cost: **$0/month**

## 1. Deploy Backend (Render)

### A. Prepare Backend for Deployment

Add `gunicorn` to `python-backend/requirements.txt`:

```txt
flask==3.0.0
flask-cors==4.0.0
google-api-python-client==2.108.0
google-auth==2.25.2
transformers==4.36.0
torch==2.1.0
pillow==10.1.0
sentence-transformers==2.2.2
python-dotenv==1.0.0
psycopg2-binary==2.9.9
requests==2.31.0
gunicorn==21.2.0
```

### B. Push to GitHub

```bash
# Initialize git (if not already)
git init
git add .
git commit -m "Initial commit"

# Create GitHub repo and push
git remote add origin https://github.com/yourusername/photofindr.git
git branch -M main
git push -u origin main
```

### C. Deploy on Render

1. Go to [Render.com](https://render.com) and sign up
2. Click **New +** → **Web Service**
3. Connect your GitHub repository
4. Configure:

**Settings:**
- **Name**: `photofindr-backend`
- **Root Directory**: `python-backend`
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`
- **Instance Type**: `Free`

**Environment Variables:**
```
SUPABASE_URL=https://wlmfymvantcrtomxjhqh.supabase.co
SUPABASE_SERVICE_ROLE_KEY=<your-service-role-key>
PORT=10000
```

5. Click **Create Web Service**
6. Wait for deployment (~5-10 minutes for first deploy)
7. Copy your backend URL: `https://photofindr-backend.onrender.com`

**Important Notes:**
- Free tier spins down after 15 minutes of inactivity
- First request after spin-down takes ~30 seconds
- Disk space is ephemeral (models re-download on spin-up)

## 2. Deploy Frontend (Vercel)

### A. Update Environment Variables

Edit `.env`:

```env
VITE_SUPABASE_URL=https://wlmfymvantcrtomxjhqh.supabase.co
VITE_SUPABASE_ANON_KEY=<your-anon-key>
VITE_BACKEND_URL=https://photofindr-backend.onrender.com
```

**Important:** Update `VITE_BACKEND_URL` to your Render backend URL!

### B. Deploy on Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
vercel
```

Follow the prompts:
- Set up and deploy? `Y`
- Which scope? (select your account)
- Link to existing project? `N`
- Project name? `photofindr`
- Directory? `./`
- Override settings? `N`

### C. Add Environment Variables in Vercel

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Select your project
3. Settings → Environment Variables
4. Add these variables:

```
VITE_SUPABASE_URL=https://wlmfymvantcrtomxjhqh.supabase.co
VITE_SUPABASE_ANON_KEY=<your-anon-key>
VITE_BACKEND_URL=https://photofindr-backend.onrender.com
```

5. Redeploy: `vercel --prod`

Your app is now live at `https://photofindr.vercel.app` (or your custom domain)!

## 3. Alternative: Deploy Backend to Railway

Railway offers a better free tier with persistent storage for models.

### A. Install Railway CLI

```bash
npm i -g @railway/cli
```

### B. Deploy

```bash
cd python-backend

# Login
railway login

# Initialize project
railway init

# Deploy
railway up

# Add environment variables
railway variables set SUPABASE_URL=https://...
railway variables set SUPABASE_SERVICE_ROLE_KEY=...
```

Your backend URL will be: `https://photofindr-backend.up.railway.app`

Update `VITE_BACKEND_URL` in Vercel accordingly.

## 4. Alternative: Deploy Backend to Fly.io

Fly.io offers good performance and persistent volumes.

### A. Install Fly CLI

```bash
curl -L https://fly.io/install.sh | sh
```

### B. Create Fly.toml

Create `python-backend/fly.toml`:

```toml
app = "photofindr-backend"
primary_region = "iad"

[build]

[http_service]
  internal_port = 5000
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0

[[vm]]
  cpu_kind = "shared"
  cpus = 1
  memory_mb = 512
```

### C. Deploy

```bash
cd python-backend

# Login
fly auth signup  # or fly auth login

# Launch app
fly launch

# Set secrets
fly secrets set SUPABASE_URL=https://...
fly secrets set SUPABASE_SERVICE_ROLE_KEY=...

# Deploy
fly deploy
```

Your backend: `https://photofindr-backend.fly.dev`

## 5. Production Optimizations

### Backend Performance

**Cache Models (Recommended for Railway/Fly.io):**

Create `python-backend/download_models.py`:

```python
from transformers import BlipProcessor, BlipForConditionalGeneration
from sentence_transformers import SentenceTransformer

print("Downloading BLIP model...")
BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

print("Downloading sentence-transformers model...")
SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

print("Models downloaded!")
```

Update build command:
```bash
pip install -r requirements.txt && python download_models.py
```

### Frontend Performance

**Enable Vercel Analytics:**

```bash
npm install @vercel/analytics
```

Update `src/main.tsx`:

```tsx
import { Analytics } from '@vercel/analytics/react';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
    <Analytics />
  </React.StrictMode>,
);
```

## 6. Custom Domain (Optional)

### Vercel
1. Go to Project Settings → Domains
2. Add your domain
3. Update DNS records as instructed

### Render
1. Go to Dashboard → Settings → Custom Domains
2. Add your domain
3. Update DNS with CNAME record

## 7. Monitoring

### Backend Health Check

Add to Render/Railway/Fly.io:
- Health check path: `/health`
- Expected response: `200 OK`

### Uptime Monitoring

Use [UptimeRobot](https://uptimerobot.com/) (free) to:
- Monitor backend availability
- Send alerts if down
- Keep Render from spinning down (ping every 5 min)

## 8. Cost Breakdown

| Service | Free Tier | Limits |
|---------|-----------|--------|
| Vercel | Free | 100GB bandwidth, unlimited deploys |
| Render | Free | Spins down after 15min inactivity, 750hrs/month |
| Railway | Free | $5 credit/month (~550 hours) |
| Fly.io | Free | 3 shared-cpu VMs, 160GB transfer |
| Supabase | Free | 500MB database, 2GB file storage |

**Total: $0/month** for moderate usage

## 9. Troubleshooting Production

### Backend taking too long to respond

- Render free tier spins down after 15min
- First request takes ~30 seconds to wake up
- Use UptimeRobot to ping every 5 minutes to keep warm

### Models downloading every deploy

- Use Railway or Fly.io with persistent storage
- Or use Docker with model caching

### CORS errors

Make sure `flask-cors` is installed and configured:

```python
from flask_cors import CORS
CORS(app)
```

### Environment variables not working

- Double-check all variables are set in Render/Railway/Fly.io dashboard
- Redeploy after changing variables
- Check logs: `render logs` or `railway logs` or `fly logs`

## Support

For deployment issues, check:
- [Render Docs](https://render.com/docs)
- [Vercel Docs](https://vercel.com/docs)
- [Railway Docs](https://docs.railway.app/)
- [Fly.io Docs](https://fly.io/docs/)

Good luck with your deployment! 🚀
