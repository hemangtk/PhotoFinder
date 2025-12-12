# app.py (replace your current file with this)
import os
import threading
import time
from flask import Flask, request, jsonify
from flask_cors import CORS

load_env = os.getenv  # convenience

app = Flask(__name__)
CORS(app)

# Controls
SKIP_MODEL_LOAD = load_env("SKIP_MODEL_LOAD", "0") == "1"
MIN_FREE_BYTES = int(load_env("MIN_FREE_BYTES", str(200 * 1024 * 1024)))  # 200MB default

# Lazy-loaded service module holders
_services = {
    "drive": None,
    "caption": None,
    "embedding": None,
    "database": None,
}
_services_lock = threading.Lock()
_loading = False

def get_free_memory_bytes():
    """Return available memory in bytes if possible, else 0."""
    try:
        import psutil
        return psutil.virtual_memory().available
    except Exception:
        try:
            with open("/proc/meminfo", "r") as f:
                for line in f:
                    if line.startswith("MemAvailable:"):
                        parts = line.split()
                        return int(parts[1]) * 1024
        except Exception:
            return 0

def import_services():
    """Import service modules lazily (in a background thread)."""
    global _loading
    with _services_lock:
        if _loading:
            return
        _loading = True

    try:
        free = get_free_memory_bytes()
        app.logger.info(f"[import_services] free memory before import: {free}")
        if SKIP_MODEL_LOAD:
            app.logger.warning("SKIP_MODEL_LOAD set -> skipping heavy service imports")
            return
        if free and free < MIN_FREE_BYTES:
            app.logger.warning(f"Not enough free memory ({free} bytes) -> skipping imports")
            return

        # Delayed imports of service modules that may import heavy ML libs.
        # Do this inside try/except to capture import errors.
        try:
            from services import drive_service as drive_service_mod
            from services import caption_service as caption_service_mod
            from services import embedding_service as embedding_service_mod
            from services import database_service as database_service_mod
        except Exception as e:
            app.logger.exception("Failed to import service modules")
            # leave modules as None on failure
            return

        with _services_lock:
            _services["drive"] = drive_service_mod
            _services["caption"] = caption_service_mod
            _services["embedding"] = embedding_service_mod
            _services["database"] = database_service_mod

        app.logger.info("Service modules imported successfully")

    finally:
        with _services_lock:
            _loading = False

def start_background_import():
    t = threading.Thread(target=import_services, daemon=True)
    t.start()
    return t

@app.route('/health', methods=['GET'])
def health():
    ready = _services["caption"] is not None and _services["embedding"] is not None
    return jsonify({'status': 'healthy', 'ready': ready}), 200

@app.route('/trigger_load', methods=['POST', 'GET'])
def trigger_load():
    """Manual trigger to start importing heavy services in background."""
    if SKIP_MODEL_LOAD:
        return jsonify({"status": "skipped_by_env"}), 412
    start_background_import()
    return jsonify({"status": "loading_started"}), 202

# Existing endpoints now import or use services lazily and provide fallback responses
@app.route('/api/fetch-drive', methods=['POST'])
def fetch_drive():
    try:
        data = request.get_json() or {}
        drive_link = data.get('driveLink')

        if not drive_link:
            return jsonify({'error': 'Drive link is required'}), 400

        # drive_service is fairly lightweight, but we still import lazily
        drive_module = _services["drive"]
        if drive_module is None:
            # Try to import on first request (safely)
            try:
                from services import drive_service as drive_module
                with _services_lock:
                    _services["drive"] = drive_module
            except Exception:
                app.logger.exception("drive_service import failed")
                return jsonify({'error': 'service not ready'}), 503

        images = drive_module.fetch_drive_images(drive_link)
        return jsonify({'images': images, 'count': len(images)}), 200

    except Exception as e:
        app.logger.exception("Error fetching Drive images")
        return jsonify({'error': str(e)}), 500

@app.route('/api/caption', methods=['POST'])
def caption_images():
    try:
        data = request.get_json() or {}
        images = data.get('images', [])

        if not images:
            return jsonify({'error': 'No images provided'}), 400

        caption_module = _services["caption"]
        if caption_module is None:
            # If captioning service isn't loaded, return a safe fallback (202)
            return jsonify({'status': 'model_not_ready', 'captions': [], 'count': 0}), 202

        captions = caption_module.generate_captions(images)
        return jsonify({'captions': captions, 'count': len(captions)}), 200

    except Exception as e:
        app.logger.exception("Error generating captions")
        return jsonify({'error': str(e)}), 500

@app.route('/api/store', methods=['POST'])
def store():
    try:
        data = request.get_json() or {}
        photos = data.get('photos', [])

        if not photos:
            return jsonify({'error': 'No photos provided'}), 400

        db_module = _services["database"]
        if db_module is None:
            # try to import lightweight DB module if possible
            try:
                from services import database_service as db_module
                with _services_lock:
                    _services["database"] = db_module
            except Exception:
                app.logger.exception("database_service import failed")
                return jsonify({'error': 'database service not ready'}), 503

        result = db_module.store_photos(photos)
        return jsonify({'message': 'Photos stored successfully', 'count': result}), 200

    except Exception as e:
        app.logger.exception("Error storing photos")
        return jsonify({'error': str(e)}), 500

@app.route('/api/search', methods=['GET'])
def search():
    try:
        query = request.args.get('query')
        if not query:
            return jsonify({'error': 'Query parameter is required'}), 400

        emb_module = _services["embedding"]
        db_module = _services["database"]
        if emb_module is None or db_module is None:
            # If embedding/db service not ready — return a graceful 202 with no results
            return jsonify({'status': 'model_not_ready', 'results': [], 'count': 0}), 202

        query_embedding = emb_module.generate_embedding(query)
        results = db_module.search_photos(query_embedding)
        return jsonify({'results': results, 'count': len(results)}), 200

    except Exception as e:
        app.logger.exception("Error searching photos")
        return jsonify({'error': str(e)}), 500

# On startup: do not block. Kick off background import only if SKIP_MODEL_LOAD not set.
if __name__ == '__main__':
    # when running locally (debug), try to start import in background (non-blocking)
    if not SKIP_MODEL_LOAD:
        app.logger.info("Starting background import of services (non-blocking)")
        start_background_import()

    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
