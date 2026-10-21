# 🍃 Himagiri Maps - MongoDB Integration Guide

This guide explains how to store, query, and synchronize all **59+ Bangalore Residential Layouts & Townships** in **MongoDB**.

---

## 📁 Architecture Overview

```
               ┌────────────────────────────────────────────────────────┐
               │                     MONGODB                            │
               │   Database: `himagiri_maps`                            │
               │   Collection: `layouts` (59+ society documents)        │
               └───────────────────────┬────────────────────────────────┘
                                       │
                     ┌─────────────────┴─────────────────┐
                     ▼                                   ▼
          ┌───────────────────────┐           ┌───────────────────────┐
          │   migrate_to_mongo.py │           │       server.py       │
          │   (Migration & Sync)  │           │   (REST API + Static) │
          └───────────────────────┘           └───────────┬───────────┘
                     │                                    │
                     ▼                                    ▼
          ┌───────────────────────┐           ┌───────────────────────┐
          │    mongo_seed.json    │◄──────────┤   Frontend (app.js)   │
          │  (Offline Fallback)   │           │ (Hybrid API + Static) │
          └───────────────────────┘           └───────────────────────┘
```

---

## 🚀 Quick Start (Local MongoDB)

### 1. Start MongoDB Locally
If using Docker:
```bash
docker run -d --name mongo -p 27017:27017 mongo:latest
```
Or start the native MongoDB service:
```bash
mongod
```

### 2. Run the Migration Script
Run the automated migration tool to upload all layouts and build indexes:
```bash
python migrate_to_mongo.py
```
This will:
- Parse all layouts from `layouts_data.js` and `map_data.json`.
- Connect to `mongodb://localhost:27017/himagiri_maps`.
- Automatically create unique and full-text search indexes.
- Bulk upsert all 59+ complete society layouts.

### 3. Start the Server
```bash
python server.py
```
Open **`http://localhost:8080`** in your browser.

---

## ☁️ Connecting to MongoDB Atlas (Cloud)

You can store the database for free in the cloud using **MongoDB Atlas**:

1. Create a free cluster on [MongoDB Atlas](https://www.mongodb.com/atlas).
2. Copy your connection string:
   ```
   mongodb+srv://<username>:<password>@cluster0.abcde.mongodb.net/himagiri_maps?retryWrites=true&w=majority
   ```
3. Run the migration script with your cloud URI:
   ```bash
   python migrate_to_mongo.py --uri "mongodb+srv://user:password@cluster.mongodb.net/"
   ```
4. Start `server.py` with the environment variable set:
   ```bash
   # Windows PowerShell
   $env:MONGODB_URI="mongodb+srv://user:password@cluster.mongodb.net/"
   python server.py

   # Linux / macOS / Bash
   export MONGODB_URI="mongodb+srv://user:password@cluster.mongodb.net/"
   python server.py
   ```

---

## 🛠️ Direct Import via `mongoimport`

If you prefer using the native MongoDB CLI tool `mongoimport`, use the generated `mongo_seed.json`:

```bash
mongoimport --uri "mongodb://localhost:27017/himagiri_maps" \
            --collection layouts \
            --file mongo_seed.json \
            --jsonArray \
            --mode upsert \
            --upsertFields _id
```

---

## 📡 REST API Endpoints

The included `server.py` provides REST endpoints powered by MongoDB (with automatic fallback to `mongo_seed.json` if MongoDB is temporarily offline):

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/health` | Connection status, database name, and layout count |
| `GET` | `/api/layouts` | Returns list of all layouts (supports `?zone=south`) |
| `GET` | `/api/layouts/:id` | Returns full layout document (plots, roads, amenities) |
| `GET` | `/api/search?q=:query`| Full-text search across layouts, locations, and sectors |
| `POST`| `/api/layouts` | Create / onboard a new society layout |
| `PUT` | `/api/layouts/:id` | Update an existing society layout |
| `DELETE` | `/api/layouts/:id` | Delete a layout |

---

## 💾 Document Schema

Each layout document in the `layouts` collection follows this schema:

```json
{
  "_id": "prestige_falcon_city",
  "id": "prestige_falcon_city",
  "name": "Prestige Falcon City",
  "location": "Kanakapura Road, Konanakunte Cross Metro, Bangalore South",
  "zone": "south",
  "type": "Iconic High-Rise Residential Township",
  "unitType": "Apartment / Tower",
  "unitCount": 49,
  "bounds": { "minX": 60, "maxX": 1180, "minY": 140, "maxY": 860 },
  "center": { "x": 620, "y": 480 },
  "groundPolygon": "90,480 200,160 620,140 ... Z",
  "borderTreesPath": "M 90,480 L 200,160 ... Z",
  "gardenPark": { "x": 440, "y": 455, "w": 360, "h": 50, "rx": 8, "label": "Grand Central Lawn" },
  "waterBody": { "x": 540, "y": 430, "w": 180, "h": 70, "rx": 14, "label": "Grand Falcon Olympic Pool" },
  "landmarks": [
    { "x": 1000, "y": 360, "w": 140, "h": 160, "rx": 8, "label": "🛍️ Forum Falcon City Mall & Metro" }
  ],
  "plots": {
    "T1": { "id": "T1", "number": "T1", "block": "Tower 1", "road": "Falcon Main Boulevard", "x": 180, "y": 240, "w": 85, "h": 65, "facing": "East" }
  },
  "roads": {
    "nodes": { "falcon_g1": { "x": 120, "y": 480, "label": "Main Entrance Gate 1 (Kanakapura Rd)" } },
    "edges": [ { "from": "falcon_g1", "to": "falcon_r1", "dist": 35, "road": "Falcon Main Boulevard" } ]
  },
  "amenities": [
    { "id": "falcon_clubhouse", "name": "Club Falcon & Sports Arena", "type": "clubhouse", "x": 620, "y": 580 }
  ],
  "sectors": ["Tower Block 1-4", "Tower Block 5-7"],
  "updatedAt": "2026-10-21T15:08:41.123456+00:00"
}
```
