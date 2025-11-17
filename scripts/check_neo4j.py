#!/usr/bin/env python3
"""
Quick script to check Neo4j health and count data
"""
import sys
from neo4j import GraphDatabase

def check_neo4j():
    uri = "bolt://localhost:7687"
    username = "neo4j"
    password = "password123"

    try:
        driver = GraphDatabase.driver(uri, auth=(username, password))

        with driver.session() as session:
            # Check GDS version
            try:
                result = session.run("CALL gds.version()")
                gds_version = result.single()
                print(f"✅ Neo4j GDS version: {gds_version[0] if gds_version else 'N/A'}")
            except Exception as e:
                print(f"⚠️  Neo4j GDS not available: {e}")

            # Count episodes
            result = session.run("MATCH (n:Episode) RETURN count(n) as total")
            total_episodes = result.single()['total']
            print(f"📊 Total Episode nodes: {total_episodes:,}")

            # Count relationships by type
            result = session.run("""
                MATCH ()-[r]->()
                RETURN type(r) as rel_type, count(r) as count
                ORDER BY count DESC
            """)
            print("\n📊 Relationships by type:")
            for record in result:
                print(f"  - {record['rel_type']}: {record['count']:,}")

            # Total relationships
            result = session.run("MATCH ()-[r]->() RETURN count(r) as total")
            total_rels = result.single()['total']
            print(f"\n📊 Total relationships: {total_rels:,}")

        driver.close()
        print("\n✅ Neo4j is healthy and accessible")
        return True

    except Exception as e:
        print(f"❌ Neo4j connection failed: {e}")
        return False

if __name__ == "__main__":
    success = check_neo4j()
    sys.exit(0 if success else 1)
