# PhotoFindr

A full-stack web application that lets users search photos by natural language descriptions using AI-powered image captioning and semantic search. Connect your Google Drive folder, let BLIP generate captions, and search using everyday language like "person in front of a church" or "beach sunset".

## Features

- **Google Drive Integration**: Connect public Drive folders without downloading images
- **AI Image Captioning**: BLIP model generates natural language descriptions
- **Semantic Search**: Find photos using everyday descriptions
- **Modern UI**: Clean, responsive design with light/dark mode
- **Free & Self-Hostable**: Uses open-source models and free-tier hosting

## Tech Stack

### Frontend
- React 18 + TypeScript
- Vite for build tooling
- TailwindCSS for styling
- Supabase client for database queries
- Lucide React for icons

### Backend (Python)
- Flask REST API
- BLIP (Salesforce/blip-image-captioning-base)
- Sentence Transformers (all-MiniLM-L6-v2)
- Google Drive API integration

### Database
- Supabase (PostgreSQL)
- pgvector extension for vector similarity search
- 384-dimensional embeddings

## Project Structure

```
photofindr/
├── src/                      # React frontend
│   ├── components/          # UI components
│   │   ├── Navbar.tsx
│   │   ├── SearchBar.tsx
│   │   ├── PhotoCard.tsx
│   │   ├── PhotoGrid.tsx
│   │   └── Toast.tsx
│   ├── pages/               # Page components
│   │   ├── Home.tsx
│   │   └── Search.tsx
│   ├── contexts/            # React contexts
│   │   └── ThemeContext.tsx
│   ├── lib/                 # Utilities
│   │   └── supabase.ts
│   └── App.tsx
│
└── python-backend/          # Python Flask API
    ├── services/
    │   ├── drive_service.py      # Google Drive integration
    │   ├── caption_service.py    # BLIP captioning
    │   ├── embedding_service.py  # Sentence embeddings
    │   └── database_service.py   # Supabase queries
    ├── app.py
    └── requirements.txt
```

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.9+
- Supabase account (free tier)
- Google Cloud API key (for Drive API)

### 1. Frontend Setup

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will run on `http://localhost:5173`

### 2. Backend Setup

See detailed instructions in `python-backend/README.md`

```bash
cd python-backend

# Install Python dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env with your Supabase credentials
# Add Google API key to services/drive_service.py

# Run backend
python app.py
```

The backend will run on `http://localhost:5000`

### 3. Database Setup

The database is already configured with:
- `photos` table with pgvector support
- HNSW index for fast similarity search
- `match_photos()` function for semantic queries

No additional setup needed!

## Usage

### 1. Connect Google Drive

1. Make a folder public in Google Drive (Anyone with link can view)
2. Copy the folder link
3. Paste it on the PhotoFindr home page
4. Click "Process Photos"

### 2. Wait for Processing

The backend will:
1. List all images in the folder
2. Generate captions using BLIP
3. Create embeddings using sentence-transformers
4. Store everything in Supabase

### 3. Search Your Photos

Navigate to the Search page and type natural language queries:
- "person in front of a church"
- "beach at sunset"
- "group of people smiling"
- "dog playing in the park"

Results show similarity scores and let you copy Drive links or open images directly.

## Deployment

### Frontend (Vercel)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Set environment variables in Vercel dashboard:
# - VITE_SUPABASE_URL
# - VITE_SUPABASE_ANON_KEY
# - VITE_BACKEND_URL (your deployed backend URL)
```

### Backend (Render)

1. Push `python-backend/` to GitHub
2. Create a Web Service on [Render](https://render.com)
3. Set Root Directory to `python-backend`
4. Add build command: `pip install -r requirements.txt`
5. Add start command: `gunicorn app:app`
6. Add environment variables
7. Deploy!

See `python-backend/README.md` for Railway and Fly.io options.

## Environment Variables

### Frontend (.env)
```
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_anon_key
VITE_BACKEND_URL=http://localhost:5000
```

### Backend (python-backend/.env)
```
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
PORT=5000
```

## How It Works

1. **Drive Listing**: Uses Google Drive API to list image URLs from public folders
2. **Caption Generation**: BLIP model analyzes each image and generates descriptions
3. **Embedding Creation**: Sentence-transformers converts captions to 384-dim vectors
4. **Storage**: Photos, captions, and embeddings stored in PostgreSQL with pgvector
5. **Search**: User queries are embedded and compared via cosine similarity
6. **Results**: Top matches returned with similarity scores

## Performance

- Initial model load: ~10-20 seconds
- Captioning: ~2-3 seconds per image
- Embedding: <1 second per text
- Search: <100ms for 1000s of photos

## Models

- **BLIP**: Image → Text captioning (~990MB)
- **MiniLM**: Text → Embedding vector (~80MB)

Both are cached after first download.

## Limitations

- Public Google Drive folders only (no private folders)
- Images must be .jpg, .jpeg, or .png
- Backend requires ~2GB RAM for BLIP
- First request is slow (model loading)

## Future Enhancements

- [ ] Batch upload optimization
- [ ] Multi-folder support
- [ ] Image similarity search (CLIP embeddings)
- [ ] User authentication
- [ ] Private folder support (OAuth2)
- [ ] GPU acceleration
- [ ] Progressive loading for large galleries

## License

MIT

## Contributing

Contributions welcome! Please open an issue or submit a PR.

## Support

For issues or questions, please open a GitHub issue.
