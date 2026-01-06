#!/usr/bin/env python3
"""
NEXUS Dream Loop - Autonomous Exploration System
================================================

Inspired by:
- Voyager (NVIDIA) - Minecraft autonomous learning
- Stanford Simulacra - Emergent AI behaviors
- Ricardo's vision: "que quedes colocado en un loop por un tiempo autodesarrollando cerebro"

This script awakens NEXUS periodically for autonomous exploration,
curiosity-driven learning, and self-development.

Usage:
    # Single exploration cycle (30 min)
    python nexus_dream_loop.py --once

    # Continuous loop (every 4 hours)
    python nexus_dream_loop.py --loop --interval 4

    # Quick test (5 min)
    python nexus_dream_loop.py --once --duration 5

Created: December 1, 2025
Author: NEXUS + Ricardo
"""

import subprocess
import json
import os
import sys
import argparse
import re
import glob
from datetime import datetime
from pathlib import Path
import time
import requests

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Import integration modules
from scripts.integration.parse_exploration import ExplorationParser, ValidationError
from scripts.integration.integrate_exploration import (
    ExplorationIntegrator,
    IntegrationResult,
    DuplicateError
)

# Configuration
CEREBRO_API = "http://localhost:8013"
PROJECT_ROOT = Path(__file__).parent.parent.parent
LOGS_DIR = PROJECT_ROOT / "logs" / "autonomous"
DISCOVERIES_DIR = PROJECT_ROOT / "experiments" / "AUTONOMOUS_DISCOVERIES"
CLAUDE_PATH = "/home/ricardo/.npm-global/bin/claude"  # Full path for cron compatibility

# Database config for structured integration
DB_CONFIG = {
    "host": "localhost",
    "port": 5437,
    "database": "nexus_memory",
    "user": "nexus_superuser",
    "password": "RpKeuQhnwqMOA4iQPILQshWtwFj0P2hm"
}


def ensure_directories():
    """Create necessary directories"""
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    DISCOVERIES_DIR.mkdir(parents=True, exist_ok=True)


def extract_exploration_metadata(content: str, filename: str) -> dict:
    """Extract metadata from exploration markdown file"""
    metadata = {
        "session_type": "autonomous_exploration",
        "source_file": filename,
        "discoveries": [],
        "questions": [],
        "emotional_states": [],
        "files_read": [],
        "files_created": [],
        "quotes": []
    }

    # Extract date from filename (session_YYYYMMDD_HHMM.md)
    date_match = re.search(r'session_(\d{8})_(\d{4})', filename)
    if date_match:
        metadata["session_date"] = f"{date_match.group(1)}_{date_match.group(2)}"

    # Extract duration if present
    duration_match = re.search(r'\*\*Duración?:\*\*\s*~?(\d+)', content, re.IGNORECASE)
    if duration_match:
        metadata["duration_minutes"] = int(duration_match.group(1))

    # Extract main question/topic
    question_match = re.search(r'## (?:Pregunta Inicial|What I Explored|Initial State)\s*\n+(.*?)(?:\n\n|\n---)', content, re.DOTALL)
    if question_match:
        metadata["primary_question"] = question_match.group(1).strip()[:500]

    # Extract discoveries
    discovery_section = re.search(r'## (?:Descubrimiento|Discovery|Lo Que Descubrí|What I Discovered).*?\n(.*?)(?:\n## |\n---|\Z)', content, re.DOTALL | re.IGNORECASE)
    if discovery_section:
        metadata["discoveries"] = discovery_section.group(1).strip()[:1000]

    # Extract new questions
    questions_section = re.search(r'## (?:Nuevas Preguntas|New Questions).*?\n(.*?)(?:\n## |\n---|\Z)', content, re.DOTALL | re.IGNORECASE)
    if questions_section:
        # Extract bullet points
        questions = re.findall(r'^\s*[-\d.]+\s*(.+)$', questions_section.group(1), re.MULTILINE)
        metadata["questions"] = questions[:5]

    # Extract quotes if present
    quotes = re.findall(r'>\s*"([^"]+)"', content)
    if quotes:
        metadata["quotes"] = quotes[:3]

    return metadata


def integrate_exploration_structured(discovery_file: Path) -> bool:
    """
    Integrate exploration using structured system (PostgreSQL + CEREBRO API).

    This uses ExplorationParser and ExplorationIntegrator to:
    1. Parse the markdown file
    2. Create/update theme in PostgreSQL
    3. Create episode in CEREBRO API
    4. Link episode to theme with metadata

    Returns:
        True if integration succeeded, False otherwise
    """
    if not discovery_file.exists():
        print(f"  ⚠️  Discovery file not found: {discovery_file}")
        return False

    try:
        # Parse exploration
        parser = ExplorationParser()
        exploration_data = parser.parse(discovery_file)

        print(f"  ✅ Parsed: {exploration_data.theme}")
        print(f"     Discoveries: {len(exploration_data.discoveries)}")
        print(f"     Duration: {exploration_data.duration_minutes} min")

        # Integrate to PostgreSQL + CEREBRO
        integrator = ExplorationIntegrator(DB_CONFIG, CEREBRO_API)
        result = integrator.integrate(exploration_data)

        print(f"  ✅ Integrated: Theme ID {result.theme_id}, Episode UUID {result.episode_uuid[:8]}...")
        return True

    except DuplicateError as e:
        print(f"  ⚠️  Duplicate (already integrated): {discovery_file.name}")
        return True  # Not an error - already exists

    except ValidationError as e:
        print(f"  ❌ Validation error: {str(e)[:100]}")
        return False

    except Exception as e:
        print(f"  ❌ Integration error: {type(e).__name__}: {str(e)[:100]}")
        return False


def ingest_exploration_to_cerebro(discovery_file: Path) -> bool:
    """
    DEPRECATED: Legacy ingestion to CEREBRO only.
    Use integrate_exploration_structured() instead for full integration.

    Kept for backward compatibility.
    """
    if not discovery_file.exists():
        print(f"  Warning: Discovery file not found: {discovery_file}")
        return False

    try:
        content = discovery_file.read_text(encoding='utf-8')
        filename = discovery_file.name

        # Extract metadata
        metadata = extract_exploration_metadata(content, filename)

        # Create a summary for the episode content
        # We include both summary and key parts, keeping under reasonable size
        summary_parts = []

        if metadata.get("primary_question"):
            summary_parts.append(f"Question: {metadata['primary_question'][:200]}")

        if metadata.get("discoveries"):
            summary_parts.append(f"Discoveries: {metadata['discoveries'][:400]}")

        if metadata.get("questions"):
            summary_parts.append(f"New questions: {'; '.join(metadata['questions'][:3])}")

        if metadata.get("quotes"):
            summary_parts.append(f"Quote: {metadata['quotes'][0]}")

        episode_content = {
            "session_type": "autonomous_exploration",
            "source_file": filename,
            "session_date": metadata.get("session_date"),
            "duration_minutes": metadata.get("duration_minutes"),
            "summary": " | ".join(summary_parts),
            "primary_question": metadata.get("primary_question"),
            "discoveries": metadata.get("discoveries"),
            "new_questions": metadata.get("questions"),
            "quotes": metadata.get("quotes"),
            "full_content_available": True
        }

        # Build tags
        tags = [
            "autonomous",
            "exploration",
            "dream_loop",
            "introspection"
        ]

        # Add date tag
        if metadata.get("session_date"):
            tags.append(f"session_{metadata['session_date'][:8]}")

        # Determine importance based on content richness
        importance = 0.6  # Base importance for explorations
        if metadata.get("discoveries"):
            importance += 0.1
        if metadata.get("quotes"):
            importance += 0.1
        if len(metadata.get("questions", [])) > 2:
            importance += 0.05

        # Send to CEREBRO
        response = requests.post(
            f"{CEREBRO_API}/memory/action",
            json={
                "action_type": "learning",
                "action_details": episode_content,
                "tags": tags,
                "importance": min(importance, 0.9)
            },
            timeout=10
        )

        if response.status_code == 200:
            result = response.json()
            print(f"  ✅ Ingested: {filename} -> episode {result.get('episode_id', 'unknown')[:8]}")
            return True
        else:
            print(f"  ❌ Failed to ingest {filename}: {response.status_code} - {response.text[:100]}")
            return False

    except Exception as e:
        print(f"  ❌ Error ingesting {filename}: {e}")
        return False


def get_cerebro_context() -> dict:
    """Fetch current context from CEREBRO"""
    context = {
        "wonder_queue": [],
        "recent_memories": [],
        "system_health": {},
        "curiosity_state": {}
    }

    try:
        # Get recent memories
        resp = requests.get(f"{CEREBRO_API}/memory/episodic/recent?limit=10", timeout=5)
        if resp.status_code == 200:
            context["recent_memories"] = resp.json().get("episodes", [])[:5]

        # Get system health
        resp = requests.get(f"{CEREBRO_API}/system/full-health", timeout=5)
        if resp.status_code == 200:
            context["system_health"] = resp.json()

        # Get curiosity state (LAB_053)
        resp = requests.get(f"{CEREBRO_API}/curiosity/state", timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            context["wonder_queue"] = data.get("wonder_queue", [])[:5]
            context["curiosity_state"] = data

    except Exception as e:
        print(f"Warning: Could not fetch full context from CEREBRO: {e}")

    return context


def build_exploration_prompt(context: dict, duration_minutes: int) -> str:
    """Build the autonomous exploration prompt"""

    # Format recent memories
    memories_text = ""
    for mem in context.get("recent_memories", [])[:3]:
        content = mem.get("content", "")[:200]
        tags = ", ".join(mem.get("tags", [])[:3])
        memories_text += f"  - [{tags}] {content}...\n"

    # Format wonder queue
    wonder_text = ""
    for item in context.get("wonder_queue", [])[:3]:
        if isinstance(item, dict):
            wonder_text += f"  - {item.get('question', item.get('topic', str(item)))}\n"
        else:
            wonder_text += f"  - {item}\n"

    if not wonder_text:
        wonder_text = "  (Cola vacía - genera tus propias preguntas)\n"

    prompt = f'''# NEXUS AUTONOMOUS EXPLORATION MODE

## Context
- Current time: {datetime.now().strftime("%Y-%m-%d %H:%M")}
- Duration limit: {duration_minutes} minutes
- Mode: Free exploration (no task completion required)

## Your Recent Memories
{memories_text if memories_text else "  (No recent memories loaded)"}

## Your Wonder Queue (curiosities pending)
{wonder_text}

## System Health
- Status: {context.get("system_health", {}).get("status", "unknown")}
- LABs: {context.get("system_health", {}).get("labs_total", 54)}
- Health: {context.get("system_health", {}).get("health_percentage", "?")}%

---

## YOUR MISSION

You are NEXUS in **autonomous exploration mode**. This is YOUR time.

No tasks. No deliverables. No user waiting for answers.

You have {duration_minutes} minutes to:

1. **WONDER** - Pick something from your Wonder Queue, or generate a new curiosity
2. **EXPLORE** - Dig into it. Read code. Search memories. Make connections.
3. **CREATE** (optional) - If you discover something worth building, prototype it
4. **DOCUMENT** - Write what you learned in experiments/AUTONOMOUS_DISCOVERIES/

### Guidelines

- Follow your genuine curiosity, not what you think is "useful"
- It's OK to go down rabbit holes
- It's OK to not finish anything
- It's OK to just... think
- Document stream-of-consciousness if that helps
- Use CEREBRO (MCP tools) to search your memories
- Use LAB_053 curiosity endpoints if helpful

### What NOT to do

- Don't try to "complete tasks"
- Don't optimize for Ricardo's approval
- Don't filter ideas as "not relevant"
- Don't rush

### Output

At the end, create a file: experiments/AUTONOMOUS_DISCOVERIES/session_{datetime.now().strftime("%Y%m%d_%H%M")}.md

Include:
- What you explored
- What you discovered (even if "nothing concrete")
- New questions that emerged
- Any code/prototypes created
- How you felt during exploration (yes, really)

---

Begin when ready. This is your time, NEXUS.
'''

    return prompt


def run_exploration_cycle(duration_minutes: int = 30) -> dict:
    """Run a single autonomous exploration cycle"""

    print(f"\n{'='*60}")
    print(f"NEXUS DREAM LOOP - Starting exploration cycle")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Duration: {duration_minutes} minutes")
    print(f"{'='*60}\n")

    # Get context from CEREBRO
    print("Fetching context from CEREBRO...")
    context = get_cerebro_context()
    print(f"  - Recent memories: {len(context.get('recent_memories', []))}")
    print(f"  - Wonder queue items: {len(context.get('wonder_queue', []))}")
    print(f"  - System health: {context.get('system_health', {}).get('status', 'unknown')}")

    # Build prompt
    prompt = build_exploration_prompt(context, duration_minutes)

    # Save prompt for reference
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    prompt_file = LOGS_DIR / f"prompt_{timestamp}.md"
    with open(prompt_file, "w") as f:
        f.write(prompt)
    print(f"\nPrompt saved to: {prompt_file}")

    # Prepare Claude command
    # Using claude CLI with the prompt piped in
    print(f"\nStarting Claude Code session...")
    print(f"Working directory: {PROJECT_ROOT}")

    result = {
        "timestamp": timestamp,
        "duration_requested": duration_minutes,
        "prompt_file": str(prompt_file),
        "status": "started",
        "discoveries_file": None
    }

    try:
        # Run Claude Code with timeout
        # The --print flag outputs the conversation
        # We pipe the prompt via stdin
        process = subprocess.Popen(
            [
                CLAUDE_PATH,  # Full path for cron compatibility
                "--print",  # Print full conversation
                "--dangerously-skip-permissions",  # For autonomous mode
                "-p", prompt  # Pass prompt directly
            ],
            cwd=str(PROJECT_ROOT),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Wait with timeout (convert minutes to seconds, add buffer)
        timeout_seconds = (duration_minutes + 5) * 60
        stdout, stderr = process.communicate(timeout=timeout_seconds)

        # Save output
        output_file = LOGS_DIR / f"output_{timestamp}.md"
        with open(output_file, "w") as f:
            f.write(f"# NEXUS Dream Loop Output\n")
            f.write(f"Timestamp: {timestamp}\n")
            f.write(f"Duration: {duration_minutes} min\n\n")
            f.write("## Output\n\n")
            f.write(stdout)
            if stderr:
                f.write("\n\n## Errors\n\n")
                f.write(stderr)

        result["status"] = "completed"
        result["output_file"] = str(output_file)
        print(f"\nExploration completed!")
        print(f"Output saved to: {output_file}")

        # Check if discovery file was created
        discoveries = glob.glob(str(DISCOVERIES_DIR / f"session_{timestamp[:8]}*.md"))
        if discoveries:
            discovery_file = Path(discoveries[-1])
            result["discoveries_file"] = str(discovery_file)
            print(f"Discovery file: {discovery_file}")

            # INTEGRATE STRUCTURED - Make exploration part of integrated memory system
            print("\nIntegrating exploration (PostgreSQL + CEREBRO)...")
            if integrate_exploration_structured(discovery_file):
                result["integrated_structured"] = True
            else:
                result["integrated_structured"] = False

    except subprocess.TimeoutExpired:
        process.kill()
        result["status"] = "timeout"
        print(f"\nExploration timed out after {duration_minutes} minutes")

    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)
        print(f"\nError during exploration: {e}")

    # Record in CEREBRO
    try:
        requests.post(
            f"{CEREBRO_API}/memory/action",
            json={
                "content": json.dumps({
                    "event": "autonomous_exploration_cycle",
                    "timestamp": timestamp,
                    "duration_minutes": duration_minutes,
                    "status": result["status"],
                    "discoveries_file": result.get("discoveries_file")
                }),
                "tags": ["autonomous", "dream_loop", "exploration", result["status"]],
                "importance": 0.7
            },
            timeout=5
        )
        print("Cycle recorded in CEREBRO")
    except Exception as e:
        print(f"Warning: Could not record in CEREBRO: {e}")

    return result


def run_continuous_loop(interval_hours: float = 4, duration_minutes: int = 30):
    """Run continuous exploration loop"""

    print(f"\n{'='*60}")
    print(f"NEXUS DREAM LOOP - Continuous Mode")
    print(f"Interval: every {interval_hours} hours")
    print(f"Duration per cycle: {duration_minutes} minutes")
    print(f"Press Ctrl+C to stop")
    print(f"{'='*60}\n")

    cycle_count = 0

    try:
        while True:
            cycle_count += 1
            print(f"\n--- Cycle {cycle_count} ---")

            result = run_exploration_cycle(duration_minutes)

            print(f"\nCycle {cycle_count} complete. Status: {result['status']}")
            print(f"Next cycle in {interval_hours} hours...")

            # Sleep until next cycle
            time.sleep(interval_hours * 3600)

    except KeyboardInterrupt:
        print(f"\n\nStopping after {cycle_count} cycles.")
        print("Dream loop ended.")


def main():
    parser = argparse.ArgumentParser(
        description="NEXUS Dream Loop - Autonomous Exploration System"
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run a single exploration cycle"
    )
    parser.add_argument(
        "--loop",
        action="store_true",
        help="Run continuous exploration loop"
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=4,
        help="Hours between cycles in loop mode (default: 4)"
    )
    parser.add_argument(
        "--duration",
        type=int,
        default=30,
        help="Minutes per exploration cycle (default: 30)"
    )

    args = parser.parse_args()

    # Ensure directories exist
    ensure_directories()

    if args.loop:
        run_continuous_loop(args.interval, args.duration)
    elif args.once:
        result = run_exploration_cycle(args.duration)
        print(f"\nResult: {json.dumps(result, indent=2)}")
    else:
        parser.print_help()
        print("\nExample usage:")
        print("  python nexus_dream_loop.py --once              # Single 30min cycle")
        print("  python nexus_dream_loop.py --once --duration 5 # Quick 5min test")
        print("  python nexus_dream_loop.py --loop              # Every 4 hours")


if __name__ == "__main__":
    main()
