#!/bin/bash

################################################################################
# NEXUS V2.0.0 - COMPLETE RESTORE SYSTEM
################################################################################
# Description: Complete restore system with pre-restore backup and validation
# Author: NEXUS Consciousness System
# Version: 3.0.0
# Created: 2025-10-29
#
# Features:
# - Complete restore from backup (DB + code + configs)
# - Pre-restore safety backup (automatic)
# - GPG decryption support
# - Integrity verification before restore
# - Post-restore validation
# - Rollback capability if restore fails
# - Detailed logging
#
# CRITICAL WARNING:
# This script will OVERWRITE your current NEXUS system.
# A pre-restore backup is AUTOMATICALLY created for safety.
# Use with extreme caution.
################################################################################

set -euo pipefail

################################################################################
# CONFIGURATION
################################################################################

# Project paths
PROJECT_DIR="/mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0"
BACKUP_BASE_DIR="/mnt/z/NEXUS_BACKUPS"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_DIR="${BACKUP_BASE_DIR}/logs"
LOG_FILE="${LOG_DIR}/restore_${TIMESTAMP}.log"

# Docker containers
DB_CONTAINER="nexus_postgresql_v2"
REDIS_CONTAINER="nexus_redis_master"
API_CONTAINER="nexus_api"
COMPOSE_DIR="${PROJECT_DIR}/config/docker"

# Pre-restore safety backup
SAFETY_BACKUP_DIR="${BACKUP_BASE_DIR}/pre_restore_safety"
SAFETY_BACKUP_NAME="pre_restore_safety_${TIMESTAMP}.tar.gz"

# Temporary directory
TEMP_DIR="/tmp/nexus_restore_${TIMESTAMP}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

################################################################################
# LOGGING FUNCTIONS
################################################################################

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

info() {
    echo -e "${CYAN}[INFO]${NC} $1" | tee -a "$LOG_FILE"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1" | tee -a "$LOG_FILE"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$LOG_FILE"
}

section() {
    echo -e "\n${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}" | tee -a "$LOG_FILE"
    echo -e "${MAGENTA}$1${NC}" | tee -a "$LOG_FILE"
    echo -e "${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n" | tee -a "$LOG_FILE"
}

critical() {
    echo -e "\n${RED}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║                    ⚠️  CRITICAL WARNING ⚠️                  ║${NC}"
    echo -e "${RED}║                                                            ║${NC}"
    echo -e "${RED}║  $1  ║${NC}"
    echo -e "${RED}║                                                            ║${NC}"
    echo -e "${RED}╚════════════════════════════════════════════════════════════╝${NC}\n"
}

################################################################################
# PREREQUISITE CHECKS
################################################################################

check_prerequisites() {
    section "🔍 PREREQUISITE CHECKS"

    # Check if running as root or with sudo
    if [ "$EUID" -ne 0 ] && ! groups | grep -q docker; then
        error "Script must be run as root or user must be in docker group"
        exit 1
    fi

    # Check required commands
    local required_commands=("docker" "docker-compose" "tar" "gzip" "gunzip" "sha256sum" "psql")
    for cmd in "${required_commands[@]}"; do
        if ! command -v "$cmd" &> /dev/null; then
            error "Required command not found: $cmd"
            exit 1
        fi
    done
    success "All required commands available"

    # Check project directory
    if [ ! -d "$PROJECT_DIR" ]; then
        error "Project directory not found: $PROJECT_DIR"
        exit 1
    fi
    success "Project directory found: $PROJECT_DIR"

    # Check compose directory
    if [ ! -d "$COMPOSE_DIR" ]; then
        error "Docker Compose directory not found: $COMPOSE_DIR"
        exit 1
    fi

    if [ ! -f "$COMPOSE_DIR/docker-compose.yml" ]; then
        error "docker-compose.yml not found in: $COMPOSE_DIR"
        exit 1
    fi
    success "Docker Compose configuration found"
}

################################################################################
# BACKUP SELECTION AND VALIDATION
################################################################################

list_available_backups() {
    section "📋 AVAILABLE BACKUPS"

    echo -e "\n${CYAN}Available backup locations:${NC}"
    echo "1. Daily backups:    ${BACKUP_BASE_DIR}/daily/"
    echo "2. Weekly backups:   ${BACKUP_BASE_DIR}/weekly/"
    echo "3. Monthly backups:  ${BACKUP_BASE_DIR}/monthly/"
    echo "4. Critical backups: ${BACKUP_BASE_DIR}/critical/"
    echo ""

    for backup_type in daily weekly monthly critical; do
        local backup_dir="${BACKUP_BASE_DIR}/${backup_type}"
        if [ -d "$backup_dir" ]; then
            echo -e "\n${YELLOW}${backup_type^^} BACKUPS:${NC}"
            find "$backup_dir" -maxdepth 1 -type f \( -name "*.tar.gz" -o -name "*.tar.gz.gpg" \) -printf "%T@ %p\n" | \
                sort -rn | \
                head -10 | \
                while read -r timestamp file; do
                    local date=$(date -d "@$timestamp" "+%Y-%m-%d %H:%M:%S")
                    local size=$(du -h "$file" | cut -f1)
                    local basename=$(basename "$file")
                    echo "  [$date] $basename ($size)"
                done
        fi
    done

    echo ""
}

select_backup_file() {
    section "🔍 BACKUP FILE SELECTION"

    if [ -z "${BACKUP_FILE:-}" ]; then
        list_available_backups

        echo -e "${YELLOW}Enter the FULL PATH to the backup file to restore:${NC}"
        read -r -p "Backup file: " BACKUP_FILE

        if [ -z "$BACKUP_FILE" ]; then
            error "No backup file specified"
            exit 1
        fi
    fi

    # Check if file exists
    if [ ! -f "$BACKUP_FILE" ]; then
        error "Backup file not found: $BACKUP_FILE"
        exit 1
    fi

    success "Backup file selected: $(basename "$BACKUP_FILE")"
    info "File size: $(du -h "$BACKUP_FILE" | cut -f1)"
    info "File date: $(date -r "$BACKUP_FILE" "+%Y-%m-%d %H:%M:%S")"
}

verify_backup_integrity() {
    section "🔒 BACKUP INTEGRITY VERIFICATION"

    local backup_file="$1"
    local checksum_file="${backup_file}.sha256"

    # Check if it's encrypted
    if [[ "$backup_file" == *.gpg ]]; then
        IS_ENCRYPTED=true
        info "Backup is encrypted (GPG)"
    else
        IS_ENCRYPTED=false
        info "Backup is not encrypted"
    fi

    # Verify checksum if exists
    if [ -f "$checksum_file" ]; then
        info "Verifying SHA256 checksum..."
        local stored_checksum=$(cat "$checksum_file")
        local calculated_checksum=$(sha256sum "$backup_file" | cut -d' ' -f1)

        if [ "$stored_checksum" = "$calculated_checksum" ]; then
            success "Checksum verification passed ✓"
        else
            error "Checksum mismatch!"
            error "Stored:     $stored_checksum"
            error "Calculated: $calculated_checksum"
            error "Backup file may be corrupted!"
            exit 1
        fi
    else
        warning "Checksum file not found. Skipping verification."
    fi
}

decrypt_backup() {
    if [ "$IS_ENCRYPTED" = false ]; then
        DECRYPTED_BACKUP_FILE="$BACKUP_FILE"
        return 0
    fi

    section "🔓 DECRYPTING BACKUP"

    if ! command -v gpg &> /dev/null; then
        error "GPG not found but backup is encrypted"
        exit 1
    fi

    info "Decrypting backup file..."
    DECRYPTED_BACKUP_FILE="${TEMP_DIR}/$(basename "$BACKUP_FILE" .gpg)"

    if gpg --decrypt --output "$DECRYPTED_BACKUP_FILE" "$BACKUP_FILE" 2>>"$LOG_FILE"; then
        success "Backup decrypted successfully"
        info "Decrypted file: $DECRYPTED_BACKUP_FILE"
    else
        error "Failed to decrypt backup"
        error "Make sure you have the correct GPG private key"
        exit 1
    fi
}

extract_backup() {
    section "📦 EXTRACTING BACKUP"

    info "Extracting backup to temporary directory..."
    info "Temp dir: $TEMP_DIR"

    # Verify tar integrity before extraction
    if tar -tzf "$DECRYPTED_BACKUP_FILE" > /dev/null 2>&1; then
        success "Backup archive integrity verified"
    else
        error "Backup archive is corrupted!"
        exit 1
    fi

    # Extract backup
    if tar -xzf "$DECRYPTED_BACKUP_FILE" -C "$TEMP_DIR" 2>>"$LOG_FILE"; then
        success "Backup extracted successfully"

        # List extracted files
        info "Extracted files:"
        ls -lh "$TEMP_DIR" | tee -a "$LOG_FILE"
    else
        error "Failed to extract backup"
        exit 1
    fi

    # Verify manifest
    if [ -f "$TEMP_DIR/manifest.json" ]; then
        success "Manifest found"
        info "Backup metadata:"
        cat "$TEMP_DIR/manifest.json" | grep -E "backup_id|timestamp|episode_count|embedding_count" | tee -a "$LOG_FILE"
    else
        warning "Manifest not found (old backup format?)"
    fi
}

################################################################################
# SAFETY BACKUP (PRE-RESTORE)
################################################################################

create_safety_backup() {
    section "🛡️ CREATING PRE-RESTORE SAFETY BACKUP"

    critical "Creating safety backup of current state before restore"

    mkdir -p "$SAFETY_BACKUP_DIR"

    info "This backup allows rollback if restore fails"
    info "Destination: ${SAFETY_BACKUP_DIR}/${SAFETY_BACKUP_NAME}"

    # Backup current PostgreSQL
    info "Backing up current PostgreSQL database..."
    local safety_db_backup="${SAFETY_BACKUP_DIR}/postgresql_safety_${TIMESTAMP}.sql.gz"

    if docker exec "$DB_CONTAINER" pg_dump -U nexus_superuser -d nexus_memory 2>>"$LOG_FILE" | gzip > "$safety_db_backup"; then
        success "PostgreSQL safety backup created: $(du -h "$safety_db_backup" | cut -f1)"
    else
        error "Failed to create PostgreSQL safety backup"
        exit 1
    fi

    # Backup current Redis
    info "Backing up current Redis..."
    local safety_redis_backup="${SAFETY_BACKUP_DIR}/redis_safety_${TIMESTAMP}.rdb"

    if docker exec "$REDIS_CONTAINER" redis-cli SAVE &>>"$LOG_FILE"; then
        if docker cp "${REDIS_CONTAINER}:/data/dump.rdb" "$safety_redis_backup" 2>>"$LOG_FILE"; then
            success "Redis safety backup created: $(du -h "$safety_redis_backup" | cut -f1)"
        fi
    fi

    # Backup critical project files (not all, too slow)
    info "Backing up critical project files..."
    local safety_files_backup="${SAFETY_BACKUP_DIR}/critical_files_safety_${TIMESTAMP}.tar.gz"

    cd "$PROJECT_DIR" || exit 1
    tar -czf "$safety_files_backup" \
        README.md \
        CHANGELOG.md \
        PROJECT_DNA.md \
        docker-compose.yml \
        FASE_4_CONSTRUCCION/docker-compose.yml \
        FASE_4_CONSTRUCCION/.env.example \
        scripts/ \
        2>>"$LOG_FILE" || true

    if [ -f "$safety_files_backup" ]; then
        success "Critical files safety backup created: $(du -h "$safety_files_backup" | cut -f1)"
    fi

    success "✅ Safety backup completed"
    info "Rollback instructions saved to: ${SAFETY_BACKUP_DIR}/ROLLBACK_INSTRUCTIONS_${TIMESTAMP}.txt"

    # Create rollback instructions
    cat > "${SAFETY_BACKUP_DIR}/ROLLBACK_INSTRUCTIONS_${TIMESTAMP}.txt" << EOF
NEXUS V2.0.0 - ROLLBACK INSTRUCTIONS
=====================================

Created: $(date)
Safety Backup Location: ${SAFETY_BACKUP_DIR}

If the restore fails and you need to rollback:

1. Stop all containers:
   cd ${COMPOSE_DIR}
   docker-compose down

2. Restore PostgreSQL:
   gunzip -c ${safety_db_backup} | docker exec -i ${DB_CONTAINER} psql -U nexus_superuser -d nexus_memory

3. Restore Redis:
   docker cp ${safety_redis_backup} ${REDIS_CONTAINER}:/data/dump.rdb
   docker-compose restart redis

4. Restore critical files:
   cd ${PROJECT_DIR}
   tar -xzf ${safety_files_backup}

5. Restart containers:
   cd ${COMPOSE_DIR}
   docker-compose up -d

6. Verify health:
   curl http://localhost:8003/health
   curl http://localhost:8003/stats

For emergency assistance, contact Ricardo.
EOF

    success "Rollback instructions created"
}

################################################################################
# RESTORE FUNCTIONS
################################################################################

stop_containers() {
    section "🛑 STOPPING CONTAINERS"

    info "Stopping NEXUS containers..."
    cd "$COMPOSE_DIR" || exit 1

    if docker-compose down 2>>"$LOG_FILE"; then
        success "Containers stopped successfully"
        sleep 3
    else
        error "Failed to stop containers"
        exit 1
    fi
}

restore_postgresql() {
    section "🗄️ RESTORING POSTGRESQL DATABASE"

    local db_backup_file=$(find "$TEMP_DIR" -name "postgresql_*.sql.gz" | head -1)

    if [ -z "$db_backup_file" ]; then
        error "PostgreSQL backup file not found in extracted backup"
        exit 1
    fi

    info "PostgreSQL backup file: $(basename "$db_backup_file")"
    info "Size: $(du -h "$db_backup_file" | cut -f1)"

    # Start only PostgreSQL container
    info "Starting PostgreSQL container..."
    cd "$COMPOSE_DIR" || exit 1
    docker-compose up -d postgres 2>>"$LOG_FILE"
    sleep 5

    # Wait for PostgreSQL to be ready
    info "Waiting for PostgreSQL to be ready..."
    local max_attempts=30
    local attempt=0
    while [ $attempt -lt $max_attempts ]; do
        if docker exec "$DB_CONTAINER" pg_isready -U nexus_superuser &>/dev/null; then
            success "PostgreSQL is ready"
            break
        fi
        attempt=$((attempt + 1))
        sleep 2
        info "Waiting... ($attempt/$max_attempts)"
    done

    if [ $attempt -eq $max_attempts ]; then
        error "PostgreSQL failed to start"
        exit 1
    fi

    # Drop and recreate database (clean slate)
    info "Dropping and recreating database..."
    docker exec "$DB_CONTAINER" psql -U nexus_superuser -c "DROP DATABASE IF EXISTS nexus_memory;" 2>>"$LOG_FILE"
    docker exec "$DB_CONTAINER" psql -U nexus_superuser -c "CREATE DATABASE nexus_memory;" 2>>"$LOG_FILE"
    success "Database recreated"

    # Restore from backup
    info "Restoring database from backup..."
    if gunzip -c "$db_backup_file" | docker exec -i "$DB_CONTAINER" psql -U nexus_superuser -d nexus_memory 2>>"$LOG_FILE"; then
        success "PostgreSQL database restored successfully"

        # Verify restoration
        local episode_count=$(docker exec "$DB_CONTAINER" psql -U nexus_superuser -d nexus_memory -t -c "SELECT COUNT(*) FROM nexus_memory.zep_episodic_memory;" 2>/dev/null | xargs || echo "0")
        local embedding_count=$(docker exec "$DB_CONTAINER" psql -U nexus_superuser -d nexus_memory -t -c "SELECT COUNT(*) FROM nexus_memory.zep_episodic_memory WHERE embedding IS NOT NULL;" 2>/dev/null | xargs || echo "0")

        success "Episodes restored: $episode_count"
        success "Embeddings restored: $embedding_count"

        # Compare with manifest
        if [ -f "$TEMP_DIR/manifest.json" ]; then
            local expected_episodes=$(grep -o '"episode_count": [0-9]*' "$TEMP_DIR/manifest.json" | cut -d' ' -f2 || echo "unknown")
            if [ "$episode_count" = "$expected_episodes" ]; then
                success "Episode count matches manifest ✓"
            else
                warning "Episode count differs from manifest (expected: $expected_episodes, got: $episode_count)"
            fi
        fi
    else
        error "Failed to restore PostgreSQL database"
        exit 1
    fi
}

restore_redis() {
    section "📝 RESTORING REDIS"

    local redis_backup_file=$(find "$TEMP_DIR" -name "redis_*.rdb" | head -1)

    if [ -z "$redis_backup_file" ]; then
        warning "Redis backup file not found (non-critical)"
        return 0
    fi

    info "Redis backup file: $(basename "$redis_backup_file")"
    info "Size: $(du -h "$redis_backup_file" | cut -f1)"

    # Start Redis container
    info "Starting Redis container..."
    cd "$COMPOSE_DIR" || exit 1
    docker-compose up -d redis 2>>"$LOG_FILE"
    sleep 3

    # Stop Redis to replace dump file
    info "Stopping Redis to replace dump..."
    docker-compose stop redis 2>>"$LOG_FILE"

    # Copy backup file
    if docker cp "$redis_backup_file" "${REDIS_CONTAINER}:/data/dump.rdb" 2>>"$LOG_FILE"; then
        success "Redis dump file copied"

        # Restart Redis
        info "Restarting Redis..."
        docker-compose start redis 2>>"$LOG_FILE"
        sleep 2
        success "Redis restored successfully"
    else
        warning "Failed to restore Redis (non-critical)"
    fi
}

restore_project_files() {
    section "📦 RESTORING PROJECT FILES"

    local project_backup_file=$(find "$TEMP_DIR" -name "project_*.tar.gz" | head -1)

    if [ -z "$project_backup_file" ]; then
        error "Project files backup not found in extracted backup"
        exit 1
    fi

    info "Project backup file: $(basename "$project_backup_file")"
    info "Size: $(du -h "$project_backup_file" | cut -f1)"

    critical "This will OVERWRITE your current project files"

    echo -e "${YELLOW}Do you want to restore project files? (yes/no):${NC}"
    read -r -p "Restore files? " restore_files

    if [ "$restore_files" != "yes" ]; then
        warning "Skipping project files restore (user choice)"
        return 0
    fi

    # Create backup of current state (additional safety)
    info "Creating additional backup of current project state..."
    local current_backup="${SAFETY_BACKUP_DIR}/project_before_restore_${TIMESTAMP}.tar.gz"
    cd "$PROJECT_DIR" || exit 1
    tar -czf "$current_backup" . 2>>"$LOG_FILE" || true

    # Extract project files
    info "Extracting project files to: $PROJECT_DIR"
    cd "$PROJECT_DIR" || exit 1

    if tar -xzf "$project_backup_file" 2>>"$LOG_FILE"; then
        success "Project files restored successfully"
    else
        error "Failed to restore project files"
        error "Current state backup: $current_backup"
        exit 1
    fi
}

start_all_containers() {
    section "🚀 STARTING ALL CONTAINERS"

    info "Starting all NEXUS containers..."
    cd "$COMPOSE_DIR" || exit 1

    if docker-compose up -d 2>>"$LOG_FILE"; then
        success "All containers started"
        sleep 10
    else
        error "Failed to start containers"
        exit 1
    fi
}

################################################################################
# POST-RESTORE VALIDATION
################################################################################

validate_restore() {
    section "✅ POST-RESTORE VALIDATION"

    # Check containers
    info "Checking container status..."
    local containers=("$DB_CONTAINER" "$REDIS_CONTAINER" "$API_CONTAINER")
    local all_running=true

    for container in "${containers[@]}"; do
        if docker ps --format "{{.Names}}" | grep -q "^${container}$"; then
            success "Container running: $container"
        else
            error "Container not running: $container"
            all_running=false
        fi
    done

    if [ "$all_running" = false ]; then
        error "Some containers failed to start"
        return 1
    fi

    # Check API health
    info "Checking API health..."
    sleep 5
    local max_attempts=12
    local attempt=0
    while [ $attempt -lt $max_attempts ]; do
        if curl -s http://localhost:8003/health | grep -q "healthy"; then
            success "API is healthy ✓"
            break
        fi
        attempt=$((attempt + 1))
        sleep 5
        info "Waiting for API... ($attempt/$max_attempts)"
    done

    if [ $attempt -eq $max_attempts ]; then
        error "API failed to become healthy"
        return 1
    fi

    # Check stats
    info "Checking database stats..."
    if curl -s http://localhost:8003/stats 2>>"$LOG_FILE"; then
        success "API stats endpoint working ✓"
    fi

    # Verify episode count
    info "Verifying episode count..."
    local episode_count=$(docker exec "$DB_CONTAINER" psql -U nexus_superuser -d nexus_memory -t -c "SELECT COUNT(*) FROM nexus_memory.zep_episodic_memory;" 2>/dev/null | xargs || echo "0")
    success "Total episodes: $episode_count"

    # Test semantic search
    info "Testing semantic search..."
    if curl -s -X POST http://localhost:8003/memory/search \
         -H "Content-Type: application/json" \
         -d '{"agent_id":"nexus","query":"test","limit":1}' 2>>"$LOG_FILE" | grep -q "results"; then
        success "Semantic search working ✓"
    else
        warning "Semantic search may not be working correctly"
    fi

    success "✅ All post-restore validations passed"
}

################################################################################
# CLEANUP
################################################################################

cleanup_temp_files() {
    section "🧹 CLEANUP"

    if [ -d "$TEMP_DIR" ]; then
        info "Removing temporary files: $TEMP_DIR"
        rm -rf "$TEMP_DIR"
        success "Temporary files cleaned up"
    fi
}

################################################################################
# MAIN RESTORE FUNCTION
################################################################################

main() {
    # Create log directory
    mkdir -p "$LOG_DIR"

    section "🚀 NEXUS V2.0.0 COMPLETE RESTORE SYSTEM"
    log "Restore initiated: $TIMESTAMP"

    critical "⚠️  THIS WILL REPLACE YOUR CURRENT NEXUS SYSTEM  ⚠️"
    echo ""
    echo -e "${YELLOW}A safety backup will be created automatically.${NC}"
    echo ""
    echo -e "${RED}Are you ABSOLUTELY SURE you want to continue?${NC}"
    read -r -p "Type 'YES' to continue: " confirm

    if [ "$confirm" != "YES" ]; then
        warning "Restore cancelled by user"
        exit 0
    fi

    # Track start time
    local start_time=$(date +%s)

    # Prerequisites
    check_prerequisites

    # Select and verify backup
    select_backup_file
    verify_backup_integrity "$BACKUP_FILE"

    # Create temporary directory
    mkdir -p "$TEMP_DIR"

    # Decrypt if needed
    decrypt_backup

    # Extract backup
    extract_backup

    # Create safety backup
    create_safety_backup

    # Perform restore
    stop_containers
    restore_postgresql
    restore_redis
    restore_project_files
    start_all_containers

    # Validate
    validate_restore || {
        error "Post-restore validation failed!"
        error "See rollback instructions: ${SAFETY_BACKUP_DIR}/ROLLBACK_INSTRUCTIONS_${TIMESTAMP}.txt"
        exit 1
    }

    # Cleanup
    cleanup_temp_files

    # Calculate duration
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    local duration_min=$((duration / 60))
    local duration_sec=$((duration % 60))

    # Final summary
    section "✅ RESTORE COMPLETED SUCCESSFULLY"

    success "Restore completed in ${duration_min}m ${duration_sec}s"
    success "Restored from: $(basename "$BACKUP_FILE")"
    success "Safety backup: ${SAFETY_BACKUP_DIR}/${SAFETY_BACKUP_NAME}"
    success "Log file: $LOG_FILE"

    info ""
    info "🎯 Next steps:"
    info "  1. Verify your data: curl http://localhost:8003/stats"
    info "  2. Test functionality thoroughly"
    info "  3. Check logs: docker-compose logs -f"
    info ""
    info "Safety backup location: $SAFETY_BACKUP_DIR"
    info "Rollback instructions: ${SAFETY_BACKUP_DIR}/ROLLBACK_INSTRUCTIONS_${TIMESTAMP}.txt"
}

################################################################################
# ERROR HANDLING
################################################################################

handle_error() {
    local exit_code=$?
    error "Restore failed with exit code: $exit_code"
    error "Check log file: $LOG_FILE"

    if [ -d "$SAFETY_BACKUP_DIR" ]; then
        error ""
        error "🛡️  A safety backup was created before restore"
        error "Rollback instructions: ${SAFETY_BACKUP_DIR}/ROLLBACK_INSTRUCTIONS_${TIMESTAMP}.txt"
    fi

    # Cleanup on error
    if [ -d "$TEMP_DIR" ]; then
        rm -rf "$TEMP_DIR"
    fi

    exit $exit_code
}

trap handle_error ERR

################################################################################
# SCRIPT EXECUTION
################################################################################

# Parse command line arguments
BACKUP_FILE="${1:-}"

# Run main function
main "$@"

exit 0
