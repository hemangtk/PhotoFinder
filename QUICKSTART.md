# PhotoFindr Quick Start Guide

Get PhotoFindr running in 5 minutes!

## Step 1: Frontend Setup (2 minutes)

```bash
# Install dependencies
npm install

# Start the frontend
npm run dev
```

Frontend will be available at `http://localhost:5173`

## Step 2: Backend Setup (3 minutes)

### Install Python Dependencies

```bash
cd python-backend
pip install -r requirements.txt
```

### Configure Environment

```bash
cp .env.example .env
```

Edit `.env` file:
```
SUPABASE_URL=https://wlmfymvantcrtomxjhqh.supabase.co
SUPABASE_SERVICE_ROLE_KEY=<get from Supabase dashboard>
PORT=5000
```

**Get Service Role Key:**
1. Go to [Supabase Dashboard](https://supabase.com/dashboard)
2. Select your project
3. Go to Settings → API
4. Copy the `service_role` key (keep it secret!)

### Setup Google Drive API

Edit `python-backend/services/drive_service.py` line 30:

Replace:
```python
'key': 'YOUR_GOOGLE_API_KEY'
```

With your Google API key:
```python
'key': 'AIza...'
```

**Get Google API Key:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create project → Enable Google Drive API
3. Credentials → Create API Key
4. Copy the key

### Start Backend

```bash
python app.py
```

Backend will run on `http://localhost:5000`

## Step 3: Test It Out!

1. **Create a public Google Drive folder**
   - Add some photos (.jpg, .png)
   - Right-click → Share → Anyone with link can view
   - Copy the folder link

2. **Open PhotoFindr**
   - Go to `http://localhost:5173`
   - Paste your Drive folder link
   - Click "Process Photos"
   - Wait for captions to generate (~3 sec per image)

3. **Search your photos**
   - Go to Search page
   - Type: "person smiling" or "building" or "sunset"
   - See results with similarity scores!

## Troubleshooting

### Frontend won't start
```bash
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Backend errors

**"ModuleNotFoundError: No module named 'flask'"**
```bash
pip install -r requirements.txt
```

**"Connection to database failed"**
- Check your `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` in `.env`
- Make sure you're using the service role key, not the anon key

**"Invalid Drive folder link"**
- Make sure folder is public
- Share settings: "Anyone with the link can view"

### Models downloading slowly?

First request downloads BLIP (~990MB) and MiniLM (~80MB). This is normal.
Models are cached after first download.

## Next Steps

- Deploy to production (see README.md)
- Add more photos
- Experiment with search queries
- Check out the code structure

## Sample Search Queries

- "a person standing in front of a building"
- "group of people smiling"
- "sunset over water"
- "dog playing"
- "food on a table"
- "mountains in the background"

Enjoy! 🎉
