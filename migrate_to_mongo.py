#!/usr/bin/env python3
"""
MongoDB Migration & Synchronization Tool for Himagiri Maps
Imports all 60 residential layouts, campuses, plots, roads, and amenities into MongoDB.
Supports both local MongoDB and MongoDB Atlas cloud clusters.
"""

import os
import sys
import json
import argparse
from datetime import datetime, timezone

# Ensure stdout handles UTF-8 cleanly on Windows
if sys.platform == 'win32' and sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

try:
    import pymongo
    from pymongo import UpdateOne, ASCENDING, TEXT
    HAS_PYMONGO = True
except ImportError:
    HAS_PYMONGO = False


def load_all_layouts():
    """Reads layouts_data.js and map_data.json into a consolidated dictionary of layout documents."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    layouts_file = os.path.join(base_dir, "layouts_data.js")
    map_data_file = os.path.join(base_dir, "map_data.json")

    layouts = {}
    now_iso = datetime.now(timezone.utc).isoformat()

    # 1. Load layouts_data.js (59 layouts)
    if os.path.exists(layouts_file):
        with open(layouts_file, "r", encoding="utf-8") as f:
            content = f.read().strip()
            prefix = "window.LAYOUTS = "
            if content.startswith(prefix):
                content = content[len(prefix):].rstrip(";")
            try:
                raw_layouts = json.loads(content)
                for lid, ldoc in raw_layouts.items():
                    doc = dict(ldoc)
                    doc["_id"] = doc.get("id", lid)
                    doc["updatedAt"] = now_iso
                    layouts[doc["_id"]] = doc
            except Exception as e:
                print(f"[!] Warning parsing layouts_data.js: {e}")

    # 2. Load Himagiri Meadows master layout from map_data.json
    if os.path.exists(map_data_file):
        with open(map_data_file, "r", encoding="utf-8") as f:
            try:
                hdata = json.load(f)
                plots = hdata.get("plots", {})
                himagiri_doc = {
                    "_id": "himagiri",
                    "id": "himagiri",
                    "name": "Himagiri Meadows",
                    "location": "Bannerghatta Road, Gottigere, Bangalore South",
                    "zone": "south",
                    "type": "Residential Gated Community",
                    "unitType": "Plot",
                    "unitCount": len(plots),
                    "bounds": {"minX": 20, "maxX": 1270, "minY": 135, "maxY": 935},
                    "center": {"x": 645, "y": 535},
                    "groundPolygon": "40,320 80,180 300,160 850,140 1050,140 1260,170 1250,600 1150,620 950,830 800,900 500,890 280,880 30,830 30,620",
                    "borderTreesPath": "M 40,320 Q 150,160 300,160 T 850,140 T 1050,140 T 1260,170 L 1250,600 L 1150,620 L 950,830 L 800,900 L 500,890 L 280,880 L 30,830 Z",
                    "gardenPark": {"x": 440, "y": 625, "w": 370, "h": 45, "rx": 6, "label": "Central Community Garden"},
                    "plots": plots,
                    "roads": {
                        "nodes": hdata.get("nodes", {}),
                        "edges": hdata.get("edges", [])
                    },
                    "amenities": hdata.get("amenities", []),
                    "sectors": ['Aster', 'Bluebell', 'Carnation', 'Dhalia', 'Exotica', 'Florentine', 'Gardenia', 'Hibiscus'],
                    "roadLabels": [
                        {"name": "ASTER ROAD", "x": 188, "y": 482, "vertical": True},
                        {"name": "BLUEBELL ROAD", "x": 306, "y": 482, "vertical": True},
                        {"name": "CARNATION ROAD", "x": 424, "y": 482, "vertical": True},
                        {"name": "DHALIA ROAD", "x": 542, "y": 482, "vertical": True},
                        {"name": "EXOTICA ROAD", "x": 660, "y": 482, "vertical": True},
                        {"name": "FLORENTINE ROAD", "x": 778, "y": 482, "vertical": True},
                        {"name": "GARDENIA ROAD", "x": 896, "y": 482, "vertical": True},
                        {"name": "HIBISCUS ROAD", "x": 337, "y": 810, "vertical": True},
                        {"name": "MAIN AVENUE (GATE 1)", "x": 306, "y": 336, "vertical": False},
                        {"name": "CENTRAL GARDEN ROAD", "x": 600, "y": 626, "vertical": False},
                        {"name": "GATE 2 ENTRY ROAD", "x": 940, "y": 336, "vertical": False}
                    ],
                    "updatedAt": now_iso
                }
                layouts["himagiri"] = himagiri_doc
            except Exception as e:
                print(f"[!] Warning parsing map_data.json: {e}")

    return layouts


def export_seed_json(layouts, output_path):
    """Exports layouts as a JSON seed file for direct mongoimport or inspection."""
    docs = list(layouts.values())
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(docs, f, indent=2, ensure_ascii=False)
    print(f"[+] Exported {len(docs)} layout documents to {output_path}")
    return docs


def sync_to_mongodb(layouts, uri, db_name, collection_name):
    """Uploads/upserts layouts to MongoDB with proper indexes."""
    if not HAS_PYMONGO:
        print("[!] PyMongo is not installed. Run: pip install pymongo")
        return False

    display_uri = uri.split('@')[-1] if '@' in uri else uri
    print(f"[*] Connecting to MongoDB at: {display_uri}...")
    try:
        client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        print("[+] Successfully connected to MongoDB!")
    except Exception as e:
        print(f"[-] Failed to connect to MongoDB: {e}")
        print("\n💡 Tips:")
        print("   1. Local: Start MongoDB with 'mongod' or 'docker run -d -p 27017:27017 mongo'")
        print("   2. Cloud (MongoDB Atlas): Pass your connection string:")
        print("      python migrate_to_mongo.py --uri 'mongodb+srv://user:pass@cluster.mongodb.net/'")
        return False

    db = client[db_name]
    coll = db[collection_name]

    # Create Indexes
    try:
        print("[*] Ensuring MongoDB indexes...")
        coll.create_index([("id", ASCENDING)], unique=True)
        coll.create_index([("zone", ASCENDING)])
        coll.create_index([
            ("name", TEXT),
            ("location", TEXT),
            ("type", TEXT)
        ], name="layout_text_search")
        print("[+] Created indexes: id (unique), zone, and text search on (name, location, type).")
    except Exception as e:
        print(f"[!] Index note: {e}")

    # Bulk Upsert
    print(f"[*] Upserting {len(layouts)} layout documents into '{db_name}.{collection_name}'...")
    operations = [
        UpdateOne({"_id": doc["_id"]}, {"$set": doc}, upsert=True)
        for doc in layouts.values()
    ]

    result = coll.bulk_write(operations)
    delete_result = coll.delete_many({"_id": {"$nin": list(layouts.keys())}})
    print("=" * 60)
    print("  MONGODB SYNC COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print(f"  Matched:  {result.matched_count}")
    print(f"  Modified: {result.modified_count}")
    print(f"  Upserted: {len(result.upserted_ids)}")
    print(f"  Purged old/unverified: {delete_result.deleted_count}")
    print(f"  Total in collection: {coll.count_documents({})}")
    print("=" * 60)
    return True


def main():
    parser = argparse.ArgumentParser(description="Migrate layout maps into MongoDB.")
    parser.add_argument("--uri", "-u", default=os.getenv("MONGODB_URI", "mongodb://localhost:27017"),
                        help="MongoDB Connection URI (default: mongodb://localhost:27017 or MONGODB_URI env var)")
    parser.add_argument("--db", "-d", default=os.getenv("MONGODB_DB", "himagiri_maps"),
                        help="Database name (default: himagiri_maps)")
    parser.add_argument("--collection", "-c", default="layouts",
                        help="Collection name (default: layouts)")
    parser.add_argument("--export-only", action="store_true",
                        help="Only export mongo_seed.json without connecting to MongoDB")

    args = parser.parse_args()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    seed_path = os.path.join(base_dir, "mongo_seed.json")

    print("[*] Reading layout maps from project...")
    layouts = load_all_layouts()
    print(f"[+] Loaded {len(layouts)} layouts.")

    # Always generate/update the clean JSON seed file
    export_seed_json(layouts, seed_path)

    if args.export_only:
        print("[+] Export completed. Run without --export-only to sync to a live MongoDB instance.")
        return

    # Attempt sync to MongoDB
    sync_to_mongodb(layouts, args.uri, args.db, args.collection)


if __name__ == "__main__":
    main()
