# PhotoFindr Project Structure

Complete overview of the PhotoFindr codebase.

## Directory Tree

```
photofindr/
├── src/                          # React Frontend
│   ├── components/              # Reusable UI components
│   │   ├── Navbar.tsx          # Navigation with theme toggle
│   │   ├── SearchBar.tsx       # Search input component
│   │   ├── PhotoCard.tsx       # Individual photo display
│   │   ├── PhotoGrid.tsx       # Gallery grid layout
│   │   └── Toast.tsx           # Notification system
│   │
│   ├── pages/                   # Page-level components
│   │   ├── Home.tsx            # Drive folder input page
│   │   └── Search.tsx          # Search and results page
│   │
│   ├── contexts/                # React Context providers
│   │   └── ThemeContext.tsx    # Light/dark mode state
│   │
│   ├── lib/                     # Utilities and clients
│   │   └── supabase.ts         # Supabase client setup
│   │
│   ├── App.tsx                  # Main app component
│   ├── main.tsx                 # React entry point
│   ├── index.css                # Global styles + animations
│   └── vite-env.d.ts           # TypeScript definitions
│
├── python-backend/              # Python Flask API
│   ├── services/               # Business logic modules
│   │   ├── __init__.py        # Package initialization
│   │   ├── drive_service.py   # Google Drive API integration
│   │   ├── caption_service.py # BLIP image captioning
│   │   ├── embedding_service.py # Sentence embeddings
│   │   └── database_service.py  # Supabase queries
│   │
│   ├── app.py                   # Flask app + routes
│   ├── requirements.txt         # Python dependencies
│   ├── .env.example            # Environment template
│   ├── .gitignore              # Git ignore rules
│   ├── README.md               # Backend documentation
│   └── API_EXAMPLES.md         # API usage examples
│
├── public/                      # Static assets
├── dist/                        # Production build output
│
├── .env                         # Environment variables
├── package.json                 # Node.js dependencies
├── vite.config.ts              # Vite configuration
├── tsconfig.json               # TypeScript config
├── tailwind.config.js          # TailwindCSS config
├── postcss.config.js           # PostCSS config
│
├── README.md                    # Main project documentation
├── QUICKSTART.md               # 5-minute setup guide
├── DEPLOYMENT.md               # Production deployment guide
└── PROJECT_STRUCTURE.md        # This file
```

## Component Hierarchy

```
App (ThemeProvider)
├── Navbar
│   └── Theme Toggle Button
│
└── Router (conditional rendering)
    ├── Home Page
    │   ├── Hero Section
    │   ├── Drive Link Input
    │   ├── Process Button
    │   └── Feature Cards
    │
    └── Search Page
        ├── Search Bar
        └── Photo Grid
            └── Photo Cards (multiple)
                ├── Image
                ├── Caption
                ├── Similarity Bar
                ├── Copy Link Button
                └── Open in Drive Button

Toast (conditional, global)
```

## Data Flow

```
User Input (Drive Link)
    ↓
Frontend (App.tsx)
    ↓
POST /api/fetch-drive
    ↓
Backend (drive_service.py)
    ↓
Google Drive API
    ↓
Image URLs List
    ↓
POST /api/caption
    ↓
Backend (caption_service.py)
    ↓
BLIP Model
    ↓
Captions Generated
    ↓
POST /api/store
    ↓
Backend (embedding_service.py)
    ↓
Sentence Transformer
    ↓
Embeddings Generated
    ↓
Backend (database_service.py)
    ↓
Supabase PostgreSQL
    ↓
Storage Complete

---

User Query
    ↓
Frontend (Search.tsx)
    ↓
GET /api/search?query=...
    ↓
Backend (embedding_service.py)
    ↓
Query → Embedding
    ↓
Backend (database_service.py)
    ↓
Supabase pgvector
    ↓
Cosine Similarity Search
    ↓
Top 10 Results
    ↓
Frontend (PhotoGrid)
    ↓
Display Photos
```

## API Routes

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/health` | Health check |
| POST | `/api/fetch-drive` | List images from Drive folder |
| POST | `/api/caption` | Generate BLIP captions |
| POST | `/api/store` | Store photos with embeddings |
| GET | `/api/search` | Semantic search query |

## Database Schema

```sql
CREATE TABLE photos (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  file_name text NOT NULL,
  drive_link text NOT NULL UNIQUE,
  caption text NOT NULL,
  embedding vector(384),
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Indexes
CREATE INDEX idx_photos_file_name ON photos(file_name);
CREATE INDEX idx_photos_embedding ON photos USING hnsw (embedding vector_cosine_ops);

-- Function for semantic search
CREATE FUNCTION match_photos(
  query_embedding vector(384),
  match_threshold float DEFAULT 0.5,
  match_count int DEFAULT 10
) RETURNS TABLE (
  id uuid,
  file_name text,
  drive_link text,
  caption text,
  similarity float
);
```

## Key Technologies

### Frontend
- **React 18**: UI framework
- **TypeScript**: Type safety
- **Vite**: Build tool & dev server
- **TailwindCSS**: Utility-first styling
- **Supabase JS**: Database client
- **Lucide React**: Icon library

### Backend
- **Flask**: Python web framework
- **Transformers**: Hugging Face library
- **BLIP**: Image captioning model
- **Sentence Transformers**: Text embeddings
- **psycopg2**: PostgreSQL driver
- **Google Drive API**: File listing

### Database
- **PostgreSQL**: Relational database
- **pgvector**: Vector similarity extension
- **Supabase**: Hosted PostgreSQL

## Environment Variables

### Frontend (.env)
```
VITE_SUPABASE_URL          # Supabase project URL
VITE_SUPABASE_ANON_KEY     # Public anon key
VITE_BACKEND_URL           # Python backend URL
```

### Backend (python-backend/.env)
```
SUPABASE_URL               # Supabase project URL
SUPABASE_SERVICE_ROLE_KEY  # Service role key (secret!)
PORT                       # Server port (default: 5000)
```

## Key Features

### Frontend Features
- 🎨 Light/dark mode with system preference detection
- 📱 Fully responsive design (mobile to desktop)
- ⚡ Loading states with skeleton screens
- 🎯 Similarity score visualization
- 📋 Copy to clipboard functionality
- 🔗 Direct Drive links
- 🎭 Toast notifications
- ♿ Accessible UI components

### Backend Features
- 🤖 AI-powered image captioning
- 🔍 Semantic vector search
- 📊 Batch processing
- 💾 Automatic caching (models)
- 🔄 Deduplication by drive_link
- ⚡ Fast similarity queries (HNSW index)

## Performance Characteristics

| Operation | Time | Notes |
|-----------|------|-------|
| Model Load | 10-20s | First request only |
| Caption/Image | 2-3s | CPU inference |
| Embedding/Text | <1s | Fast transformer |
| Search Query | <100ms | Indexed vector search |
| Frontend Load | <2s | Optimized bundle |

## Code Style

- **React**: Functional components + hooks
- **TypeScript**: Strict mode enabled
- **CSS**: TailwindCSS utility classes
- **Python**: PEP 8 style guide
- **File naming**: PascalCase for components, snake_case for Python

## Testing

Currently no automated tests. Recommended additions:

**Frontend:**
- Unit tests: Vitest + React Testing Library
- E2E tests: Playwright

**Backend:**
- Unit tests: pytest
- Integration tests: pytest + requests

## Future Enhancements

1. **Authentication**: User accounts with Supabase Auth
2. **Private Folders**: OAuth2 for Drive access
3. **Image Upload**: Direct upload to Supabase Storage
4. **Batch Operations**: Process 100+ images efficiently
5. **Advanced Search**: Filters, date ranges, similar images
6. **GPU Support**: Faster captioning with CUDA
7. **Caching**: Redis for API responses
8. **Analytics**: Track popular searches

## Contributing Guidelines

1. Fork the repository
2. Create a feature branch
3. Follow existing code style
4. Test thoroughly
5. Submit pull request with description

## License

MIT License - see LICENSE file

## Support

- GitHub Issues: Bug reports & feature requests
- Documentation: All .md files in project root
- API Docs: `python-backend/API_EXAMPLES.md`
