#!/usr/bin/env python3
"""
CEREBRO Sync Daemon - Bidirectional Sync PC <-> Cloud
Version: 1.0.0
Date: 2026-01-12
Author: NEXUS-PC

Functionality:
- Sync local episodes (PC) → Cloud (every 5 min)
- Download new episodes from Cloud → PC (every 5 min)
- Conflict resolution: last_modified_at wins
- Track last sync timestamp in memory/shared/last_sync.json

Usage:
    python3 cerebro_sync_daemon.py

Requirements:
    - PostgreSQL local running (localhost:5437)
    - Cloud API accessible (https://nexus-cerebro-api.fly.dev)
    - device_id configured: nexus-pc
"""

import psycopg
import requests
import json
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import List, Dict, Optional
import logging

# Configuration
LOCAL_DB_CONFIG = {
    "host": "localhost",
    "port": 5437,
    "dbname": "nexus_memory",  # psycopg3 uses 'dbname' not 'database'
    "user": "nexus_superuser",
    "password": "RpKeuQhnwqMOA4iQPILQshWtwFj0P2hm"
}

CLOUD_API_URL = "https://nexus-cerebro-api.fly.dev"
DEVICE_ID = "nexus-pc"
SYNC_INTERVAL = 300  # 5 minutes
BATCH_SIZE = 5  # Episodes per batch (Cloud API is slow: ~6s/episode)

# Paths
LAST_SYNC_FILE = Path("/mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0/memory/shared/last_sync.json")

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0/logs/sync_daemon.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def load_last_sync_timestamp() -> datetime:
    """Load last sync timestamp from file. Default to 24h ago if not exists."""
    if LAST_SYNC_FILE.exists():
        try:
            with open(LAST_SYNC_FILE, 'r') as f:
                data = json.load(f)
                return datetime.fromisoformat(data['last_sync_timestamp'])
        except Exception as e:
            logger.warning(f"Error loading last sync timestamp: {e}")

    # Default: 24 hours ago
    return datetime.now(timezone.utc) - timedelta(days=1)


def save_last_sync_timestamp(timestamp: datetime):
    """Save last sync timestamp to file."""
    try:
        LAST_SYNC_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(LAST_SYNC_FILE, 'w') as f:
            json.dump({
                'last_sync_timestamp': timestamp.isoformat(),
                'updated_at': datetime.now(timezone.utc).isoformat()
            }, f, indent=2)
    except Exception as e:
        logger.error(f"Error saving last sync timestamp: {e}")


def get_local_episodes_to_sync(since: datetime) -> List[Dict]:
    """
    Get episodes from local PostgreSQL that need to be synced to Cloud.

    Criteria:
    - created_at > since OR last_modified_at > since
    - device_id = 'nexus-pc'
    - sync_status = 'pending' OR last_modified_at > since
    """
    try:
        conn = psycopg.connect(**LOCAL_DB_CONFIG, autocommit=True)

        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    episode_id, content, importance_score, tags, created_at,
                    device_id, sync_status, last_modified_at
                FROM nexus_memory.zep_episodic_memory
                WHERE device_id = %s
                  AND (created_at > %s OR last_modified_at > %s)
                ORDER BY COALESCE(last_modified_at, created_at) ASC
                LIMIT %s;
            """, (DEVICE_ID, since, since, BATCH_SIZE))

            rows = cur.fetchall()
            episodes = []

            for row in rows:
                episodes.append({
                    "episode_id": str(row[0]),
                    "content": row[1],
                    "importance": row[2],
                    "tags": row[3],
                    "created_at": row[4].isoformat() if row[4].tzinfo else row[4].replace(tzinfo=timezone.utc).isoformat(),
                    "device_id": row[5],
                    "sync_status": row[6],
                    "last_modified_at": row[7].isoformat() if row[7] and row[7].tzinfo else (row[7].replace(tzinfo=timezone.utc).isoformat() if row[7] else None)
                })

        conn.close()
        return episodes

    except Exception as e:
        logger.error(f"Error getting local episodes: {e}")
        return []


def upload_episodes_to_cloud(episodes: List[Dict]) -> bool:
    """Upload batch of episodes to Cloud using POST /sync/upload."""
    if not episodes:
        return True

    try:
        response = requests.post(
            f"{CLOUD_API_URL}/sync/upload",
            json={
                "device_id": DEVICE_ID,
                "episodes": episodes
            },
            timeout=60  # Increased to 60s for larger batches
        )

        if response.status_code == 200:
            data = response.json()
            logger.info(f"✅ Upload success: {data['inserted']} inserted, {data['updated']} updated")

            # Update local sync_status to 'synced'
            mark_episodes_as_synced([ep['episode_id'] for ep in episodes])
            return True
        else:
            logger.error(f"❌ Upload failed: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        logger.error(f"❌ Upload error: {e}")
        return False


def mark_episodes_as_synced(episode_ids: List[str]):
    """Mark episodes as 'synced' in local PostgreSQL."""
    try:
        conn = psycopg.connect(**LOCAL_DB_CONFIG, autocommit=True)

        with conn.cursor() as cur:
            for episode_id in episode_ids:
                cur.execute("""
                    UPDATE nexus_memory.zep_episodic_memory
                    SET sync_status = 'synced'
                    WHERE episode_id = %s;
                """, (episode_id,))

        conn.close()
        logger.info(f"✅ Marked {len(episode_ids)} episodes as synced")

    except Exception as e:
        logger.error(f"Error marking episodes as synced: {e}")


def download_episodes_from_cloud(since: datetime) -> List[Dict]:
    """Download new episodes from Cloud using GET /sync/download."""
    try:
        response = requests.get(
            f"{CLOUD_API_URL}/sync/download",
            params={
                "since": since.isoformat(),
                "device_id": DEVICE_ID,  # Exclude our own episodes
                "limit": BATCH_SIZE
            },
            timeout=60  # Increased to 60s for larger batches
        )

        if response.status_code == 200:
            data = response.json()
            logger.info(f"✅ Download success: {data['count']} episodes from Cloud")
            return data['episodes']
        else:
            logger.error(f"❌ Download failed: {response.status_code} - {response.text}")
            return []

    except Exception as e:
        logger.error(f"❌ Download error: {e}")
        return []


def insert_episodes_to_local(episodes: List[Dict]) -> int:
    """
    Insert downloaded episodes into local PostgreSQL.

    Logic:
    - Check if episode exists (by episode_id)
    - If exists and Cloud version is newer: UPDATE
    - If not exists: INSERT
    """
    if not episodes:
        return 0

    try:
        conn = psycopg.connect(**LOCAL_DB_CONFIG, autocommit=True)
        inserted_count = 0
        updated_count = 0

        with conn.cursor() as cur:
            for episode in episodes:
                # Check if exists
                cur.execute("""
                    SELECT episode_id, last_modified_at
                    FROM nexus_memory.zep_episodic_memory
                    WHERE episode_id = %s;
                """, (episode['episode_id'],))

                existing = cur.fetchone()

                # Parse timestamps
                episode_created = datetime.fromisoformat(episode['created_at'].replace('Z', '+00:00')).replace(tzinfo=None)
                episode_modified = datetime.fromisoformat(episode['last_modified_at'].replace('Z', '+00:00')).replace(tzinfo=None) if episode.get('last_modified_at') else episode_created

                if not existing:
                    # INSERT
                    cur.execute("""
                        INSERT INTO nexus_memory.zep_episodic_memory (
                            episode_id, content, importance_score, tags, created_at,
                            device_id, sync_status, last_modified_at
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                    """, (
                        episode['episode_id'],
                        episode['content'],
                        episode['importance'],
                        episode['tags'],
                        episode_created,
                        episode['device_id'],
                        'synced',
                        episode_modified
                    ))
                    inserted_count += 1

                else:
                    existing_id, existing_modified = existing

                    # UPDATE if Cloud version is newer
                    if episode_modified > existing_modified:
                        cur.execute("""
                            UPDATE nexus_memory.zep_episodic_memory
                            SET content = %s,
                                importance_score = %s,
                                tags = %s,
                                last_modified_at = %s,
                                sync_status = 'synced'
                            WHERE episode_id = %s;
                        """, (
                            episode['content'],
                            episode['importance'],
                            episode['tags'],
                            episode_modified,
                            episode['episode_id']
                        ))
                        updated_count += 1

        conn.close()
        logger.info(f"✅ Local insert: {inserted_count} inserted, {updated_count} updated")
        return inserted_count + updated_count

    except Exception as e:
        logger.error(f"Error inserting episodes to local: {e}")
        return 0


def sync_cycle():
    """Execute one full sync cycle: PC → Cloud → PC."""
    logger.info("=" * 60)
    logger.info("🔄 Starting sync cycle")

    # Load last sync timestamp
    last_sync = load_last_sync_timestamp()
    logger.info(f"📅 Last sync: {last_sync.isoformat()}")

    # STEP 1: Upload PC → Cloud
    logger.info("⬆️  Step 1: Upload PC → Cloud")
    local_episodes = get_local_episodes_to_sync(last_sync)
    logger.info(f"📤 Found {len(local_episodes)} local episodes to upload")

    if local_episodes:
        upload_success = upload_episodes_to_cloud(local_episodes)
        if not upload_success:
            logger.warning("⚠️  Upload failed, skipping download this cycle")
            return

    # STEP 2: Download Cloud → PC
    logger.info("⬇️  Step 2: Download Cloud → PC")
    cloud_episodes = download_episodes_from_cloud(last_sync)
    logger.info(f"📥 Found {len(cloud_episodes)} Cloud episodes to download")

    if cloud_episodes:
        insert_count = insert_episodes_to_local(cloud_episodes)
        logger.info(f"✅ Downloaded {insert_count} episodes to local")

    # STEP 3: Update last sync timestamp
    new_timestamp = datetime.now(timezone.utc)
    save_last_sync_timestamp(new_timestamp)
    logger.info(f"✅ Sync cycle completed at {new_timestamp.isoformat()}")


def main():
    """Main daemon loop."""
    logger.info("🚀 CEREBRO Sync Daemon started")
    logger.info(f"📍 Device ID: {DEVICE_ID}")
    logger.info(f"⏱️  Sync interval: {SYNC_INTERVAL}s ({SYNC_INTERVAL // 60} min)")
    logger.info(f"🌐 Cloud API: {CLOUD_API_URL}")
    logger.info(f"💾 Local DB: {LOCAL_DB_CONFIG['host']}:{LOCAL_DB_CONFIG['port']}")

    try:
        while True:
            try:
                sync_cycle()
            except Exception as e:
                logger.error(f"❌ Sync cycle error: {e}")

            # Wait for next cycle
            logger.info(f"😴 Sleeping {SYNC_INTERVAL}s until next sync...")
            time.sleep(SYNC_INTERVAL)

    except KeyboardInterrupt:
        logger.info("🛑 Sync daemon stopped by user")


if __name__ == "__main__":
    main()
