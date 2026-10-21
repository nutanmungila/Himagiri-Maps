#!/usr/bin/env python3
"""
Himagiri Meadows & Bangalore Layouts - MongoDB REST API & Static Server
Provides:
- MongoDB REST API endpoints (/api/layouts, /api/layouts/:id, /api/search, /api/health)
- Automatic fallback to mongo_seed.json if MongoDB is offline
- Full static file serving for Android phone and web browser
- LAN access on 0.0.0.0
"""

import os
import sys
import json
import socket
import socketserver
import urllib.parse
from http.server import SimpleHTTPRequestHandler
from datetime import datetime, timezone

# Ensure stdout handles UTF-8 on Windows
if sys.platform == 'win32' and sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

PORT = int(os.getenv("PORT", 8080))
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGODB_DB = os.getenv("MONGODB_DB", "himagiri_maps")

# Try to connect to MongoDB
mongo_client = None
mongo_db = None
mongo_coll = None

try:
    import pymongo
    mongo_client = pymongo.MongoClient(MONGODB_URI, serverSelectionTimeoutMS=2000)
    mongo_client.admin.command('ping')
    mongo_db = mongo_client[MONGODB_DB]
    mongo_coll = mongo_db["layouts"]
    print(f"[+] Connected to MongoDB at: {MONGODB_URI.split('@')[-1] if '@' in MONGODB_URI else MONGODB_URI}")
except Exception as e:
    print(f"[-] MongoDB offline or not reachable ({e}). Running in fallback mode with local seed data.")
    mongo_client = None
    mongo_coll = None

# Load fallback memory cache from mongo_seed.json or layouts_data.js
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FALLBACK_CACHE = {}

def load_fallback_cache():
    global FALLBACK_CACHE
    seed_file = os.path.join(BASE_DIR, "mongo_seed.json")
    if os.path.exists(seed_file):
        try:
            with open(seed_file, "r", encoding="utf-8") as f:
                docs = json.load(f)
                for doc in docs:
                    FALLBACK_CACHE[doc["_id"]] = doc
            print(f"[+] Loaded {len(FALLBACK_CACHE)} layouts into fallback memory cache.")
            return
        except Exception as e:
            print(f"[!] Error loading mongo_seed.json: {e}")

load_fallback_cache()


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = socket.gethostbyname(socket.gethostname())
    finally:
        s.close()
    return ip


class MongoAPIRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def send_json(self, status_code, data):
        body = json.dumps(data, ensure_ascii=False, default=str).encode('utf-8')
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        # 1. Health check
        if path == "/api/health":
            is_connected = False
            total_docs = len(FALLBACK_CACHE)
            if mongo_coll is not None:
                try:
                    total_docs = mongo_coll.count_documents({})
                    is_connected = True
                except Exception:
                    is_connected = False

            return self.send_json(200, {
                "status": "healthy",
                "database": "mongodb",
                "connected": is_connected,
                "dbName": MONGODB_DB,
                "collection": "layouts",
                "totalLayouts": total_docs,
                "timestamp": datetime.now(timezone.utc).isoformat()
            })

        # 2. Search API (/api/search?q=...)
        if path == "/api/search":
            q = query.get("q", [""])[0].strip().lower()
            if not q:
                return self.send_json(200, [])

            results = []
            if mongo_coll is not None:
                try:
                    regex = {"$regex": q, "$options": "i"}
                    cursor = mongo_coll.find({
                        "$or": [
                            {"name": regex},
                            {"location": regex},
                            {"zone": regex},
                            {"type": regex}
                        ]
                    }, {
                        "_id": 1, "id": 1, "name": 1, "location": 1, "zone": 1, "type": 1, "unitCount": 1
                    }).limit(15)
                    results = list(cursor)
                except Exception as e:
                    print(f"MongoDB search error: {e}")

            if not results:
                # Fallback search
                for doc in FALLBACK_CACHE.values():
                    if (q in doc.get("name", "").lower() or 
                        q in doc.get("location", "").lower() or 
                        q in doc.get("zone", "").lower()):
                        results.append({
                            "_id": doc["_id"],
                            "id": doc.get("id", doc["_id"]),
                            "name": doc.get("name"),
                            "location": doc.get("location"),
                            "zone": doc.get("zone"),
                            "type": doc.get("type"),
                            "unitCount": doc.get("unitCount", 0)
                        })
                    if len(results) >= 15:
                        break

            return self.send_json(200, results)

        # 3. List layouts (/api/layouts)
        if path == "/api/layouts":
            zone_filter = query.get("zone", [None])[0]
            layouts_list = []

            if mongo_coll is not None:
                try:
                    filter_q = {"zone": zone_filter} if zone_filter and zone_filter != "all" else {}
                    projection = {
                        "_id": 1, "id": 1, "name": 1, "location": 1, "zone": 1,
                        "type": 1, "unitType": 1, "unitCount": 1
                    }
                    cursor = mongo_coll.find(filter_q, projection).sort("name", 1)
                    layouts_list = list(cursor)
                except Exception as e:
                    print(f"MongoDB list error: {e}")

            if not layouts_list:
                for doc in FALLBACK_CACHE.values():
                    if not zone_filter or zone_filter == "all" or doc.get("zone") == zone_filter:
                        layouts_list.append({
                            "_id": doc["_id"],
                            "id": doc.get("id", doc["_id"]),
                            "name": doc.get("name"),
                            "location": doc.get("location"),
                            "zone": doc.get("zone"),
                            "type": doc.get("type"),
                            "unitType": doc.get("unitType"),
                            "unitCount": doc.get("unitCount", 0)
                        })

            return self.send_json(200, layouts_list)

        # 4. Get Single Layout (/api/layouts/<id>)
        if path.startswith("/api/layouts/"):
            layout_id = path.replace("/api/layouts/", "").strip()
            doc = None

            if mongo_coll is not None:
                try:
                    doc = mongo_coll.find_one({"$or": [{"_id": layout_id}, {"id": layout_id}]})
                except Exception as e:
                    print(f"MongoDB get error: {e}")

            if not doc:
                doc = FALLBACK_CACHE.get(layout_id)

            if doc:
                return self.send_json(200, doc)
            else:
                return self.send_json(404, {"error": f"Layout '{layout_id}' not found in database."})

        # Regular Static File Serving
        return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/api/layouts":
            content_len = int(self.headers.get('Content-Length', 0))
            if content_len == 0:
                return self.send_json(400, {"error": "Missing payload body."})

            try:
                body = json.loads(self.rfile.read(content_len).decode('utf-8'))
                layout_id = body.get("id") or body.get("_id")
                if not layout_id or not body.get("name"):
                    return self.send_json(400, {"error": "'id' and 'name' are required fields."})

                body["_id"] = layout_id
                body["updatedAt"] = datetime.now(timezone.utc).isoformat()

                if mongo_coll is not None:
                    mongo_coll.update_one({"_id": layout_id}, {"$set": body}, upsert=True)

                FALLBACK_CACHE[layout_id] = body
                return self.send_json(201, {"success": True, "id": layout_id, "message": "Layout saved to MongoDB."})
            except Exception as e:
                return self.send_json(500, {"error": str(e)})

        return self.send_json(404, {"error": "Endpoint not found."})

    def do_PUT(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path.startswith("/api/layouts/"):
            layout_id = path.replace("/api/layouts/", "").strip()
            content_len = int(self.headers.get('Content-Length', 0))
            try:
                body = json.loads(self.rfile.read(content_len).decode('utf-8'))
                body["_id"] = layout_id
                body["updatedAt"] = datetime.now(timezone.utc).isoformat()

                if mongo_coll is not None:
                    mongo_coll.update_one({"_id": layout_id}, {"$set": body}, upsert=True)

                FALLBACK_CACHE[layout_id] = body
                return self.send_json(200, {"success": True, "id": layout_id, "message": "Layout updated."})
            except Exception as e:
                return self.send_json(500, {"error": str(e)})

        return self.send_json(404, {"error": "Endpoint not found."})

    def do_DELETE(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path.startswith("/api/layouts/"):
            layout_id = path.replace("/api/layouts/", "").strip()
            if mongo_coll is not None:
                mongo_coll.delete_one({"_id": layout_id})

            FALLBACK_CACHE.pop(layout_id, None)
            return self.send_json(200, {"success": True, "deleted": layout_id})

        return self.send_json(404, {"error": "Endpoint not found."})


def run_server():
    ip = get_local_ip()
    socketserver.TCPServer.allow_reuse_address = True

    with socketserver.TCPServer(('0.0.0.0', PORT), MongoAPIRequestHandler) as httpd:
        print("=" * 65)
        print("  HIMAGIRI MAPS - MONGODB REST API & WEB SERVER")
        print("=" * 65)
        print(f"  [>] Local Web URL:    http://localhost:{PORT}")
        print(f"  [>] Mobile LAN URL:   http://{ip}:{PORT}")
        print(f"  [>] API Health Check: http://localhost:{PORT}/api/health")
        print(f"  [>] API Layouts List: http://localhost:{PORT}/api/layouts")
        print(f"  [>] API Single Map:   http://localhost:{PORT}/api/layouts/prestige_falcon_city")
        print("=" * 65)
        print("  Server is active. Press Ctrl+C to terminate.")
        print("=" * 65)
        sys.stdout.flush()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer terminated.")


if __name__ == '__main__':
    run_server()
