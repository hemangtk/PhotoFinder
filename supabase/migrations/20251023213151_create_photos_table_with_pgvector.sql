/*
  # PhotoFindr Database Schema

  1. Extensions
    - Enable `pgvector` extension for semantic search with embeddings
  
  2. New Tables
    - `photos`
      - `id` (uuid, primary key) - Unique identifier for each photo
      - `file_name` (text) - Original filename from Google Drive
      - `drive_link` (text) - Direct link to image in Google Drive
      - `caption` (text) - BLIP-generated natural language caption
      - `embedding` (vector(384)) - MiniLM embedding vector for semantic search
      - `created_at` (timestamptz) - When the photo was indexed
      - `updated_at` (timestamptz) - Last update timestamp
  
  3. Indexes
    - HNSW index on embedding column for fast approximate nearest neighbor search
    - Index on file_name for quick lookups
  
  4. Security
    - Enable RLS on `photos` table
    - Public read access (anyone can search photos)
    - No write access from client (all writes go through backend)
  
  5. Functions
    - `match_photos` - Semantic search function using cosine similarity
      Takes a query embedding and returns top N most similar photos
*/

-- Enable pgvector extension for vector operations
CREATE EXTENSION IF NOT EXISTS vector;

-- Create photos table
CREATE TABLE IF NOT EXISTS photos (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  file_name text NOT NULL,
  drive_link text NOT NULL UNIQUE,
  caption text NOT NULL,
  embedding vector(384),
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Create index on file_name for quick lookups
CREATE INDEX IF NOT EXISTS idx_photos_file_name ON photos(file_name);

-- Create HNSW index for fast vector similarity search
CREATE INDEX IF NOT EXISTS idx_photos_embedding ON photos 
USING hnsw (embedding vector_cosine_ops);

-- Enable Row Level Security
ALTER TABLE photos ENABLE ROW LEVEL SECURITY;

-- Policy: Anyone can read photos (public search)
CREATE POLICY "Public read access"
  ON photos
  FOR SELECT
  TO anon, authenticated
  USING (true);

-- Policy: No direct inserts from client
-- (Backend will use service role key)

-- Create semantic search function
CREATE OR REPLACE FUNCTION match_photos(
  query_embedding vector(384),
  match_threshold float DEFAULT 0.5,
  match_count int DEFAULT 10
)
RETURNS TABLE (
  id uuid,
  file_name text,
  drive_link text,
  caption text,
  similarity float
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    photos.id,
    photos.file_name,
    photos.drive_link,
    photos.caption,
    1 - (photos.embedding <=> query_embedding) as similarity
  FROM photos
  WHERE photos.embedding IS NOT NULL
    AND 1 - (photos.embedding <=> query_embedding) > match_threshold
  ORDER BY photos.embedding <=> query_embedding
  LIMIT match_count;
END;
$$;