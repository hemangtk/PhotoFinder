from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

from services.drive_service import fetch_drive_images
from services.caption_service import generate_captions
from services.embedding_service import generate_embedding
from services.database_service import store_photos, search_photos

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'}), 200

@app.route('/api/fetch-drive', methods=['POST'])
def fetch_drive():
    try:
        data = request.get_json()
        drive_link = data.get('driveLink')

        if not drive_link:
            return jsonify({'error': 'Drive link is required'}), 400

        images = fetch_drive_images(drive_link)

        return jsonify({
            'images': images,
            'count': len(images)
        }), 200

    except Exception as e:
        print(f"Error fetching Drive images: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/caption', methods=['POST'])
def caption_images():
    try:
        data = request.get_json()
        images = data.get('images', [])

        if not images:
            return jsonify({'error': 'No images provided'}), 400

        captions = generate_captions(images)

        return jsonify({
            'captions': captions,
            'count': len(captions)
        }), 200

    except Exception as e:
        print(f"Error generating captions: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/store', methods=['POST'])
def store():
    try:
        data = request.get_json()
        photos = data.get('photos', [])

        if not photos:
            return jsonify({'error': 'No photos provided'}), 400

        result = store_photos(photos)

        return jsonify({
            'message': 'Photos stored successfully',
            'count': result
        }), 200

    except Exception as e:
        print(f"Error storing photos: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/search', methods=['GET'])
def search():
    try:
        query = request.args.get('query')

        if not query:
            return jsonify({'error': 'Query parameter is required'}), 400

        query_embedding = generate_embedding(query)
        results = search_photos(query_embedding)

        return jsonify({
            'results': results,
            'count': len(results)
        }), 200

    except Exception as e:
        print(f"Error searching photos: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
