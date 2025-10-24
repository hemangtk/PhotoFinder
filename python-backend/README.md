# PhotoFindr Python Backend

This is the Python backend for PhotoFindr that handles AI captioning and semantic search.

## Features

- Google Drive folder image listing
- BLIP image captioning (Salesforce/blip-image-captioning-base)
- Sentence embeddings (all-MiniLM-L6-v2)
- PostgreSQL/Supabase integration with pgvector
- Semantic search with cosine similarity

## Setup

### 1. Install Dependencies

```bash
cd python-backend
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env` with your values:

```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
PORT=5000
```

### 3. Google Drive API Setup

To fetch images from public Google Drive folders, you need a Google API key:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the **Google Drive API**
4. Go to **Credentials** → **Create Credentials** → **API Key**
5. Copy the API key
6. Edit `services/drive_service.py` and replace `YOUR_GOOGLE_API_KEY` with your key

**Note:** For public folders, you don't need OAuth2. A simple API key works.

### 4. Run the Server

```bash
python app.py
```

The server will start on `http://localhost:5000`

## API Endpoints

### POST `/api/fetch-drive`

Fetch all images from a Google Drive folder.

**Request:**
```json
{
  "driveLink": "https://drive.google.com/drive/folders/FOLDER_ID"
}
```

**Response:**
```json
{
  "images": [
    {
      "fileName": "photo.jpg",
      "fileId": "...",
      "driveLink": "https://drive.google.com/file/d/.../view",
      "directLink": "https://drive.google.com/uc?export=view&id=..."
    }
  ],
  "count": 1
}
```

### POST `/api/caption`

Generate captions for images using BLIP.

**Request:**
```json
{
  "images": [
    {
      "fileName": "photo.jpg",
      "driveLink": "...",
      "directLink": "..."
    }
  ]
}
```

**Response:**
```json
{
  "captions": [
    {
      "fileName": "photo.jpg",
      "driveLink": "...",
      "caption": "a person standing in front of a church"
    }
  ],
  "count": 1
}
```

### POST `/api/store`

Store photos with embeddings in Supabase.

**Request:**
```json
{
  "photos": [
    {
      "fileName": "photo.jpg",
      "driveLink": "...",
      "caption": "a person standing in front of a church"
    }
  ]
}
```

**Response:**
```json
{
  "message": "Photos stored successfully",
  "count": 1
}
```

### GET `/api/search?query=...`

Semantic search for photos.

**Request:**
```
GET /api/search?query=person in front of church
```

**Response:**
```json
{
  "results": [
    {
      "id": "...",
      "file_name": "photo.jpg",
      "drive_link": "...",
      "caption": "a person standing in front of a church",
      "similarity": 0.87
    }
  ],
  "count": 1
}
```

## Deployment

### Option 1: Render (Free Tier)

1. Push this `python-backend` folder to GitHub
2. Create a new **Web Service** on [Render](https://render.com)
3. Connect your repository
4. Set **Root Directory** to `python-backend`
5. Set **Build Command**: `pip install -r requirements.txt`
6. Set **Start Command**: `gunicorn app:app`
7. Add environment variables in Render dashboard
8. Deploy!

Add `gunicorn` to `requirements.txt`:
```
gunicorn==21.2.0
```

### Option 2: Railway

1. Install Railway CLI: `npm i -g @railway/cli`
2. Run `railway login`
3. Run `railway init`
4. Run `railway up`
5. Add environment variables via Railway dashboard

### Option 3: Fly.io

1. Install Fly CLI: `curl -L https://fly.io/install.sh | sh`
2. Run `fly auth signup` or `fly auth login`
3. Run `fly launch` in the python-backend directory
4. Set environment variables: `fly secrets set SUPABASE_URL=... SUPABASE_SERVICE_ROLE_KEY=...`
5. Deploy: `fly deploy`

## Performance Tips

- The first request will be slow as models are loaded into memory
- After initial load, captioning takes ~2-3 seconds per image
- Use batch processing for multiple images
- Consider using GPU for faster inference (CUDA-enabled hosting)

## Models Used

- **BLIP**: Salesforce/blip-image-captioning-base (~990MB)
- **Embeddings**: sentence-transformers/all-MiniLM-L6-v2 (~80MB)

Both models are cached after first download.

## Troubleshooting

### "No module named 'torch'"
```bash
pip install torch
```

### "Connection refused" to Supabase
Check your `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` are correct.

### "Invalid Drive folder link"
Make sure the folder is set to "Anyone with the link can view" in Google Drive.

### Out of memory
BLIP requires ~2GB RAM. Consider using a smaller model or upgrading your hosting tier.
