import psycopg2
from psycopg2.extras import execute_values
import os
from typing import List, Dict
from services.embedding_service import generate_embeddings_batch

def get_db_connection():
    supabase_url = os.getenv('SUPABASE_URL')
    service_role_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

    if not supabase_url:
        raise ValueError('SUPABASE_URL not set in environment variables')

    db_host = supabase_url.replace('https://', '').replace('http://', '')
    project_ref = db_host.split('.')[0]

    db_config = {
        'host': f'db.{project_ref}.supabase.co',
        'database': 'postgres',
        'user': 'postgres',
        'password': service_role_key,
        'port': 5432
    }

    return psycopg2.connect(**db_config)

def store_photos(photos: List[Dict[str, str]]) -> int:
    captions = [photo['caption'] for photo in photos]
    embeddings = generate_embeddings_batch(captions)

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        values = [
            (
                photo['fileName'],
                photo['driveLink'],
                photo['caption'],
                emb  # keep as Python list
            )
            for photo, emb in zip(photos, embeddings)
        ]

        insert_query = """
            INSERT INTO photos (file_name, drive_link, caption, embedding)
            VALUES %s
            ON CONFLICT (drive_link)
            DO UPDATE SET
                caption = EXCLUDED.caption,
                embedding = EXCLUDED.embedding,
                updated_at = now()
        """

        execute_values(cursor, insert_query, values)

        conn.commit()
        return len(photos)

    except Exception as e:
        conn.rollback()
        raise Exception(f'Database error: {str(e)}')

    finally:
        cursor.close()
        conn.close()


def search_photos(query_embedding: List[float], limit: int = 10) -> List[Dict]:
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        search_query = """
            SELECT
                id,
                file_name,
                drive_link,
                caption,
                1 - (embedding <=> %s::vector) as similarity
            FROM photos
            WHERE embedding IS NOT NULL
            ORDER BY embedding <=> %s::vector
            LIMIT %s
        """

        # Pass embedding as a list directly
        cursor.execute(search_query, (query_embedding, query_embedding, limit))

        results = cursor.fetchall()

        photos = []
        for row in results:
            photos.append({
                'id': str(row[0]),
                'file_name': row[1],
                'drive_link': row[2],
                'caption': row[3],
                'similarity': float(row[4]),
                'created_at': ''
            })

        return photos

    except Exception as e:
        raise Exception(f'Search error: {str(e)}')

    finally:
        cursor.close()
        conn.close()
