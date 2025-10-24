# PhotoFindr API Examples

Real-world examples of API requests and responses.

## 1. Fetch Drive Images

**Endpoint:** `POST /api/fetch-drive`

**Request:**
```bash
curl -X POST http://localhost:5000/api/fetch-drive \
  -H "Content-Type: application/json" \
  -d '{
    "driveLink": "https://drive.google.com/drive/folders/1abc123xyz"
  }'
```

**Response:**
```json
{
  "images": [
    {
      "fileName": "beach-sunset.jpg",
      "fileId": "1abc123xyz789",
      "driveLink": "https://drive.google.com/file/d/1abc123xyz789/view",
      "directLink": "https://drive.google.com/uc?export=view&id=1abc123xyz789"
    },
    {
      "fileName": "church-photo.jpg",
      "fileId": "1def456uvw123",
      "driveLink": "https://drive.google.com/file/d/1def456uvw123/view",
      "directLink": "https://drive.google.com/uc?export=view&id=1def456uvw123"
    },
    {
      "fileName": "city-skyline.png",
      "fileId": "1ghi789rst456",
      "driveLink": "https://drive.google.com/file/d/1ghi789rst456/view",
      "directLink": "https://drive.google.com/uc?export=view&id=1ghi789rst456"
    }
  ],
  "count": 3
}
```

## 2. Generate Captions

**Endpoint:** `POST /api/caption`

**Request:**
```bash
curl -X POST http://localhost:5000/api/caption \
  -H "Content-Type: application/json" \
  -d '{
    "images": [
      {
        "fileName": "beach-sunset.jpg",
        "driveLink": "https://drive.google.com/file/d/1abc123xyz789/view",
        "directLink": "https://drive.google.com/uc?export=view&id=1abc123xyz789"
      },
      {
        "fileName": "church-photo.jpg",
        "driveLink": "https://drive.google.com/file/d/1def456uvw123/view",
        "directLink": "https://drive.google.com/uc?export=view&id=1def456uvw123"
      }
    ]
  }'
```

**Response:**
```json
{
  "captions": [
    {
      "fileName": "beach-sunset.jpg",
      "driveLink": "https://drive.google.com/file/d/1abc123xyz789/view",
      "caption": "a sunset over the ocean with waves"
    },
    {
      "fileName": "church-photo.jpg",
      "driveLink": "https://drive.google.com/file/d/1def456uvw123/view",
      "caption": "a person standing in front of a large white church building"
    }
  ],
  "count": 2
}
```

## 3. Store Photos

**Endpoint:** `POST /api/store`

**Request:**
```bash
curl -X POST http://localhost:5000/api/store \
  -H "Content-Type: application/json" \
  -d '{
    "photos": [
      {
        "fileName": "beach-sunset.jpg",
        "driveLink": "https://drive.google.com/file/d/1abc123xyz789/view",
        "caption": "a sunset over the ocean with waves"
      },
      {
        "fileName": "church-photo.jpg",
        "driveLink": "https://drive.google.com/file/d/1def456uvw123/view",
        "caption": "a person standing in front of a large white church building"
      }
    ]
  }'
```

**Response:**
```json
{
  "message": "Photos stored successfully",
  "count": 2
}
```

**What happens:**
1. Generates 384-dim embeddings for each caption
2. Stores in Supabase: `{fileName, driveLink, caption, embedding}`
3. Updates existing photos if drive_link already exists

## 4. Search Photos

**Endpoint:** `GET /api/search?query=...`

**Request:**
```bash
curl "http://localhost:5000/api/search?query=person%20in%20front%20of%20church"
```

**Response:**
```json
{
  "results": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "file_name": "church-photo.jpg",
      "drive_link": "https://drive.google.com/file/d/1def456uvw123/view",
      "caption": "a person standing in front of a large white church building",
      "similarity": 0.89,
      "created_at": ""
    },
    {
      "id": "660e8400-e29b-41d4-a716-446655440001",
      "file_name": "cathedral.jpg",
      "drive_link": "https://drive.google.com/file/d/1xyz789abc456/view",
      "caption": "a gothic cathedral with people walking in front",
      "similarity": 0.76,
      "created_at": ""
    }
  ],
  "count": 2
}
```

**How it works:**
1. Query "person in front of church" → embedding vector
2. Compare with all stored embeddings using cosine similarity
3. Return top 10 matches sorted by similarity score

## 5. Health Check

**Endpoint:** `GET /health`

**Request:**
```bash
curl http://localhost:5000/health
```

**Response:**
```json
{
  "status": "healthy"
}
```

## Full Workflow Example

### Step 1: Fetch Images from Drive

```bash
curl -X POST http://localhost:5000/api/fetch-drive \
  -H "Content-Type: application/json" \
  -d '{"driveLink": "https://drive.google.com/drive/folders/YOUR_FOLDER_ID"}' \
  > images.json
```

### Step 2: Generate Captions

```bash
curl -X POST http://localhost:5000/api/caption \
  -H "Content-Type: application/json" \
  -d @images.json \
  > captions.json
```

### Step 3: Store in Database

```bash
curl -X POST http://localhost:5000/api/store \
  -H "Content-Type: application/json" \
  -d "$(jq '{photos: .captions}' captions.json)" \
  > store_result.json
```

### Step 4: Search

```bash
curl "http://localhost:5000/api/search?query=sunset%20over%20water" \
  > search_results.json
```

## Error Responses

### 400 Bad Request

```json
{
  "error": "Drive link is required"
}
```

### 500 Internal Server Error

```json
{
  "error": "Failed to fetch from Google Drive API: 403 Forbidden"
}
```

## Performance Notes

- First request: ~10-20 seconds (model loading)
- Subsequent captions: ~2-3 seconds per image
- Search: <100ms
- Storage: ~1 second per batch

## Testing with cURL

Save this as `test_api.sh`:

```bash
#!/bin/bash

BACKEND_URL="http://localhost:5000"

echo "1. Testing health endpoint..."
curl "$BACKEND_URL/health"
echo -e "\n"

echo "2. Fetching Drive images..."
curl -X POST "$BACKEND_URL/api/fetch-drive" \
  -H "Content-Type: application/json" \
  -d '{"driveLink": "https://drive.google.com/drive/folders/YOUR_FOLDER_ID"}'
echo -e "\n"

echo "3. Searching photos..."
curl "$BACKEND_URL/api/search?query=sunset"
echo -e "\n"

echo "All tests complete!"
```

Run: `bash test_api.sh`
