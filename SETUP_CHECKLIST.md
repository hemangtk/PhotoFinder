# PhotoFindr Setup Checklist

Complete this checklist to get PhotoFindr running locally and in production.

## ✅ Prerequisites

- [ ] Node.js 18+ installed (`node --version`)
- [ ] Python 3.9+ installed (`python --version`)
- [ ] Git installed (`git --version`)
- [ ] Code editor (VS Code recommended)
- [ ] Terminal/Command prompt

## ✅ Local Development Setup

### Frontend

- [ ] Clone or download project
- [ ] Navigate to project root
- [ ] Run `npm install`
- [ ] Verify `.env` file exists with correct values:
  - [ ] `VITE_SUPABASE_URL` is set
  - [ ] `VITE_SUPABASE_ANON_KEY` is set
  - [ ] `VITE_BACKEND_URL=http://localhost:5000`
- [ ] Run `npm run dev`
- [ ] Open `http://localhost:5173` in browser
- [ ] Verify home page loads correctly
- [ ] Test light/dark mode toggle

### Backend

- [ ] Navigate to `python-backend/` directory
- [ ] Create Python virtual environment (recommended):
  ```bash
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  ```
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Create `.env` file: `cp .env.example .env`
- [ ] Edit `.env` with your values:
  - [ ] `SUPABASE_URL` matches frontend
  - [ ] `SUPABASE_SERVICE_ROLE_KEY` from Supabase dashboard
  - [ ] `PORT=5000`
- [ ] Get Google Drive API key:
  - [ ] Go to Google Cloud Console
  - [ ] Create/select project
  - [ ] Enable Google Drive API
  - [ ] Create API key (Credentials)
  - [ ] Copy API key
- [ ] Edit `services/drive_service.py`:
  - [ ] Replace `YOUR_GOOGLE_API_KEY` with actual key (line 30)
- [ ] Run backend: `python app.py`
- [ ] Verify startup messages show models loading
- [ ] Test health endpoint: `curl http://localhost:5000/health`

### Database

- [ ] Database already configured (no action needed!)
- [ ] Verify by checking Supabase dashboard:
  - [ ] `photos` table exists
  - [ ] `pgvector` extension enabled
  - [ ] `match_photos` function exists

## ✅ Test Complete Workflow

- [ ] Create test Google Drive folder
- [ ] Add 2-3 test images (.jpg or .png)
- [ ] Make folder public ("Anyone with link can view")
- [ ] Copy folder link
- [ ] Open PhotoFindr frontend
- [ ] Paste Drive link on home page
- [ ] Click "Process Photos"
- [ ] Wait for success message
- [ ] Navigate to Search page
- [ ] Try search query (e.g., "person", "building", "nature")
- [ ] Verify results appear with similarity scores
- [ ] Test "Copy Link" button
- [ ] Test "Open in Drive" button
- [ ] Verify images load correctly

## ✅ Production Deployment

### Supabase (Already Done)

- [x] Database configured
- [x] pgvector extension enabled
- [x] Tables and functions created

### Backend Deployment (Choose One)

#### Option A: Render

- [ ] Push code to GitHub
- [ ] Create Render account
- [ ] Create new Web Service
- [ ] Connect GitHub repo
- [ ] Set root directory: `python-backend`
- [ ] Add environment variables
- [ ] Deploy
- [ ] Copy backend URL
- [ ] Test health endpoint

#### Option B: Railway

- [ ] Install Railway CLI
- [ ] Run `railway login`
- [ ] Navigate to `python-backend/`
- [ ] Run `railway init`
- [ ] Run `railway up`
- [ ] Add environment variables
- [ ] Copy backend URL

#### Option C: Fly.io

- [ ] Install Fly CLI
- [ ] Run `fly auth login`
- [ ] Navigate to `python-backend/`
- [ ] Run `fly launch`
- [ ] Set secrets
- [ ] Deploy
- [ ] Copy backend URL

### Frontend Deployment (Vercel)

- [ ] Update `.env` with production backend URL
- [ ] Install Vercel CLI: `npm i -g vercel`
- [ ] Run `vercel login`
- [ ] Run `vercel` in project root
- [ ] Add environment variables in Vercel dashboard:
  - [ ] `VITE_SUPABASE_URL`
  - [ ] `VITE_SUPABASE_ANON_KEY`
  - [ ] `VITE_BACKEND_URL` (production backend)
- [ ] Run `vercel --prod`
- [ ] Copy frontend URL
- [ ] Test production app

## ✅ Post-Deployment Verification

- [ ] Frontend loads on production URL
- [ ] Backend health check responds
- [ ] Can process Drive folder
- [ ] Captions generate successfully
- [ ] Photos stored in database
- [ ] Search returns results
- [ ] Images load from Drive
- [ ] All buttons work
- [ ] Theme toggle works
- [ ] Mobile responsive

## ✅ Optional Enhancements

- [ ] Add custom domain (Vercel + Render/Railway/Fly.io)
- [ ] Set up uptime monitoring (UptimeRobot)
- [ ] Enable Vercel Analytics
- [ ] Configure GitHub Actions for auto-deploy
- [ ] Add error tracking (Sentry)
- [ ] Set up backup strategy for database

## ✅ Documentation Review

- [ ] Read `README.md` for overview
- [ ] Read `QUICKSTART.md` for quick setup
- [ ] Read `DEPLOYMENT.md` for deployment details
- [ ] Read `python-backend/README.md` for backend specifics
- [ ] Read `python-backend/API_EXAMPLES.md` for API usage
- [ ] Read `PROJECT_STRUCTURE.md` for codebase overview

## 🎯 Troubleshooting Reference

If you encounter issues, check:

1. **Frontend won't start**
   - Delete `node_modules` and `package-lock.json`
   - Run `npm install` again

2. **Backend errors**
   - Check all environment variables are set
   - Verify Python version is 3.9+
   - Check Google API key is correct

3. **Database connection fails**
   - Verify Supabase credentials
   - Check service role key (not anon key)
   - Ensure database is accessible

4. **Models not loading**
   - First request takes 10-20 seconds (normal)
   - Requires ~2GB RAM
   - Models cache after first download

5. **Drive folder not found**
   - Ensure folder is public
   - Share setting: "Anyone with link can view"
   - Verify link format is correct

6. **Images not displaying**
   - Drive images must be public
   - Check browser console for errors
   - Verify CORS settings

## 📊 Success Criteria

You've successfully set up PhotoFindr when:

- ✅ Frontend loads without errors
- ✅ Backend responds to health check
- ✅ Can process at least one Drive folder
- ✅ Captions generate for images
- ✅ Search returns relevant results
- ✅ All UI interactions work smoothly

## 🎉 You're Done!

Congratulations on setting up PhotoFindr!

Next steps:
- Add more photos to your Drive folder
- Experiment with different search queries
- Share with friends and get feedback
- Consider contributing improvements

## 💡 Pro Tips

1. Use UptimeRobot to keep Render backend warm (free plan)
2. Batch process folders with many images during low-traffic times
3. Create multiple Drive folders for different photo collections
4. Use descriptive search queries for best results
5. Keep your service role key secret (never commit to Git)

## 📞 Need Help?

- Check documentation in project root
- Review `TROUBLESHOOTING.md` (if created)
- Open GitHub issue with details
- Include error messages and logs

Happy photo finding! 📸✨
