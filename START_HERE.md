# 🚀 PhotoFindr - Start Here!

Welcome to PhotoFindr, an AI-powered photo search application that lets you find photos using natural language!

## 📋 What You Have

A complete full-stack application with:

- ✅ **Modern React frontend** with light/dark mode
- ✅ **Python Flask backend** with BLIP AI captioning
- ✅ **Supabase PostgreSQL** database with vector search
- ✅ **Google Drive integration** for easy photo management
- ✅ **Semantic search** using sentence transformers
- ✅ **Production-ready** code with deployment guides

## 🎯 Quick Navigation

### First Time Setup
👉 **[QUICKSTART.md](QUICKSTART.md)** - Get running in 5 minutes

### Complete Setup
👉 **[SETUP_CHECKLIST.md](SETUP_CHECKLIST.md)** - Step-by-step checklist

### Understanding the Project
👉 **[README.md](README.md)** - Full project overview
👉 **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - Codebase structure

### Deployment
👉 **[DEPLOYMENT.md](DEPLOYMENT.md)** - Production deployment guide

### Backend Documentation
👉 **[python-backend/README.md](python-backend/README.md)** - Backend details
👉 **[python-backend/API_EXAMPLES.md](python-backend/API_EXAMPLES.md)** - API usage

## ⚡ Super Quick Start

```bash
# 1. Install frontend dependencies
npm install

# 2. Start frontend (terminal 1)
npm run dev

# 3. Setup backend (terminal 2)
cd python-backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your Supabase credentials

# 4. Edit services/drive_service.py
# Replace YOUR_GOOGLE_API_KEY with actual Google API key

# 5. Start backend
python app.py

# 6. Open http://localhost:5173 and start using PhotoFindr!
```

## 🔑 What You Need

Before you start, get these ready:

1. **Supabase Credentials** (already configured)
   - URL: Check `.env` file
   - Service Role Key: Get from Supabase dashboard

2. **Google Drive API Key**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create project → Enable Drive API → Get API key
   - Takes 2 minutes!

3. **A Google Drive Folder**
   - Add some photos
   - Make it public ("Anyone with link can view")
   - Copy the folder link

## 🎨 How It Works

```
1. Paste Drive Link → 2. AI Generates Captions → 3. Search Naturally
     ↓                        ↓                          ↓
  "drive.google.com/..."  "person in church"      "Find: sunset beach"
                                                         ↓
                                                   📸 Results!
```

## 📦 What's Included

### Frontend (`src/`)
- Home page with Drive link input
- Search page with results grid
- Photo cards with captions and similarity scores
- Light/dark theme toggle
- Responsive design

### Backend (`python-backend/`)
- Flask REST API
- BLIP image captioning
- Sentence-transformers embeddings
- Supabase database integration
- Google Drive file listing

### Database (Supabase)
- PostgreSQL with pgvector
- Vector similarity search
- Photos table with embeddings
- Automatic indexing

## 🛠️ Tech Stack

**Frontend:** React + TypeScript + TailwindCSS + Vite
**Backend:** Python + Flask + BLIP + Sentence Transformers
**Database:** Supabase (PostgreSQL + pgvector)
**AI Models:** BLIP (captioning) + MiniLM (embeddings)

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `START_HERE.md` | This file - your starting point |
| `QUICKSTART.md` | 5-minute setup guide |
| `README.md` | Main project documentation |
| `SETUP_CHECKLIST.md` | Complete setup checklist |
| `PROJECT_STRUCTURE.md` | Codebase overview |
| `DEPLOYMENT.md` | Production deployment guide |
| `python-backend/README.md` | Backend documentation |
| `python-backend/API_EXAMPLES.md` | API usage examples |
| `LICENSE` | MIT License |

## 🚦 Getting Started

### Option 1: I'm in a hurry (5 minutes)
Read **QUICKSTART.md** and follow the steps.

### Option 2: I want to understand everything (15 minutes)
1. Read this file (you're here!)
2. Read **README.md** for project overview
3. Follow **SETUP_CHECKLIST.md** step by step
4. Review **PROJECT_STRUCTURE.md** to understand the code

### Option 3: I want to deploy to production
1. Get it running locally first (QUICKSTART.md)
2. Follow **DEPLOYMENT.md** for Vercel + Render deployment
3. Test thoroughly before sharing

## ❓ Common Questions

**Q: Do I need to pay for anything?**
A: No! Everything uses free tiers (Supabase, Vercel, Render).

**Q: How long does processing take?**
A: ~2-3 seconds per image for captioning.

**Q: Can I use private Drive folders?**
A: Currently only public folders. OAuth2 support is a future enhancement.

**Q: How accurate is the search?**
A: Very good! The AI understands context and semantics.

**Q: Can I upload images directly?**
A: Not yet, but it's on the roadmap. Use Drive for now.

**Q: What image formats are supported?**
A: JPG, JPEG, and PNG files.

## 🐛 Troubleshooting

**Frontend won't start:**
```bash
rm -rf node_modules package-lock.json
npm install
npm run dev
```

**Backend errors:**
- Check `.env` file has correct Supabase credentials
- Verify Google API key is added to `services/drive_service.py`
- Ensure Python 3.9+ is installed

**Database connection fails:**
- Use service role key (not anon key) in backend `.env`
- Verify Supabase URL is correct

**For more help:** Check SETUP_CHECKLIST.md or open a GitHub issue

## 🎯 Next Steps

1. ✅ Complete setup (QUICKSTART.md or SETUP_CHECKLIST.md)
2. ✅ Test with a small Drive folder (2-3 images)
3. ✅ Try different search queries
4. ✅ Deploy to production (DEPLOYMENT.md)
5. ✅ Share with friends!

## 💡 Pro Tips

- Start with a small folder (5-10 images) to test
- Use descriptive search queries for best results
- The first backend request is slow (model loading)
- Keep your service role key secret (never commit to Git)
- Use UptimeRobot to keep free-tier backend warm

## 🎉 Ready?

Pick your path:
- **Fast Setup:** Jump to [QUICKSTART.md](QUICKSTART.md)
- **Detailed Setup:** Start with [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md)
- **Just Browsing:** Read [README.md](README.md)

Let's build something awesome! 🚀📸✨

---

**Need help?** All the answers are in the documentation files. Happy coding!
