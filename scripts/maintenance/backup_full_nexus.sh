#!/bin/bash

################################################################################
# NEXUS V2.0.0 - COMPLETE BACKUP SYSTEM
################################################################################
# Description: Complete backup system with GFS rotation, encryption, and cloud sync
# Author: NEXUS Consciousness System
# Version: 3.0.0
# Created: 2025-10-29
#
# Features:
# - Complete project backup (DB + code + configs)
# - GFS rotation (7 daily + 4 weekly + 3 monthly)
# - GPG encryption for sensitive data
# - SHA256 integrity verification
# - Google Drive sync via rclone
# - Email/webhook notifications
# - Comprehensive logging
################################################################################

set -euo pipefail

################################################################################
# CONFIGURATION
################################################################################

# Project paths
PROJECT_DIR="/mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0"
BACKUP_BASE_DIR="/mnt/z/NEXUS_BACKUPS"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
DATE=$(date +"%Y-%m-%d")
BACKUP_TYPE="${1:-daily}"  # daily, weekly, monthly, critical

# Backup destinations
BACKUP_DIR="${BACKUP_BASE_DIR}/${BACKUP_TYPE}"
LOG_DIR="${BACKUP_BASE_DIR}/logs"
LOG_FILE="${LOG_DIR}/backup_${BACKUP_TYPE}_${TIMESTAMP}.log"

# Docker containers
DB_CONTAINER="nexus_postgresql_v2"
REDIS_CONTAINER="nexus_redis_master"
API_CONTAINER="nexus_api_master"

# Retention policy (days)
RETENTION_DAILY=7
RETENTION_WEEKLY=28
RETENTION_MONTHLY=90

# Backup names
BACKUP_NAME="nexus_full_${DATE}_${BACKUP_TYPE}"
DB_BACKUP_NAME="postgresql_${TIMESTAMP}.sql.gz"
REDIS_BACKUP_NAME="redis_${TIMESTAMP}.rdb"
PROJECT_BACKUP_NAME="project_${TIMESTAMP}.tar.gz"
COMPLETE_BACKUP_NAME="${BACKUP_NAME}.tar.gz"
ENCRYPTED_BACKUP_NAME="${COMPLETE_BACKUP_NAME}.gpg"

# Temporary directory
TEMP_DIR="${BACKUP_DIR}/temp_${TIMESTAMP}"

# GPG encryption (set to "yes" to enable)
ENABLE_ENCRYPTION="yes"
GPG_RECIPIENT="ricardo@nexus-consciousness.local"  # ✅ Configured

# rclone for Google Drive
ENABLE_CLOUD_SYNC="yes"
RCLONE_REMOTE="gdrive"  # Configure with: rclone config
RCLONE_PATH="NEXUS_BACKUPS/${BACKUP_TYPE}"

# Notifications
ENABLE_NOTIFICATIONS="yes"
NOTIFICATION_TYPE="webhook"  # webhook, email, telegram
WEBHOOK_URL="YOUR_WEBHOOK_URL_HERE"  # Discord/Slack webhook
NOTIFICATION_EMAIL="ricardo@example.com"

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

################################################################################
# NOTIFICATION FUNCTIONS
################################################################################

send_notification() {
    local title="$1"
    local message="$2"
    local status="$3"  # success, error, warning

    if [ "$ENABLE_NOTIFICATIONS" != "yes" ]; then
        return 0
    fi

    case "$NOTIFICATION_TYPE" in
        webhook)
            send_webhook_notification "$title" "$message" "$status"
            ;;
        email)
            send_email_notification "$title" "$message" "$status"
            ;;
        telegram)
            send_telegram_notification "$title" "$message" "$status"
            ;;
    esac
}

send_webhook_notification() {
    local title="$1"
    local message="$2"
    local status="$3"

    if [ "$WEBHOOK_URL" = "YOUR_WEBHOOK_URL_HERE" ]; then
        warning "Webhook URL not configured. Skipping notification."
        return 0
    fi

    local color="3066993"  # Blue
    [ "$status" = "success" ] && color="3066993"  # Green
    [ "$status" = "error" ] && color="15158332"   # Red
    [ "$status" = "warning" ] && color="16776960" # Yellow

    local payload=$(cat <<EOF
{
  "embeds": [{
    "title": "🤖 NEXUS Backup System",
    "description": "**${title}**\n\n${message}",
    "color": ${color},
    "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "footer": {
      "text": "NEXUS V2.0.0 Backup System"
    }
  }]
}
EOF
)

    curl -H "Content-Type: application/json" \
         -X POST \
         -d "$payload" \
         "$WEBHOOK_URL" \
         --silent --output /dev/null 2>/dev/null || warning "Failed to send webhook notification"
}

send_email_notification() {
    local title="$1"
    local message="$2"
    local status="$3"

    if ! command -v mail &> /dev/null; then
        warning "Mail command not found. Install mailutils for email notifications."
        return 0
    fi

    echo -e "Subject: [NEXUS Backup] ${title}\n\n${message}\n\nTimestamp: $(date)\nBackup Type: ${BACKUP_TYPE}\nStatus: ${status}" | \
        mail -s "[NEXUS Backup] ${title}" "$NOTIFICATION_EMAIL" 2>/dev/null || \
        warning "Failed to send email notification"
}

send_telegram_notification() {
    warning "Telegram notifications not implemented yet. Use webhook or email."
}

################################################################################
# PREREQUISITE CHECKS
################################################################################

check_prerequisites() {
    section "🔍 PREREQUISITE CHECKS"

    # Check if running as root or with sudo (needed for Docker)
    if [ "$EUID" -ne 0 ] && ! groups | grep -q docker; then
        error "Script must be run as root or user must be in docker group"
        exit 1
    fi

    # Check required commands
    local required_commands=("docker" "docker-compose" "tar" "gzip" "sha256sum" "curl")
    for cmd in "${required_commands[@]}"; do
        if ! command -v "$cmd" &> /dev/null; then
            error "Required command not found: $cmd"
            exit 1
        fi
    done
    success "All required commands available"

    # Check GPG if encryption enabled
    if [ "$ENABLE_ENCRYPTION" = "yes" ]; then
        if ! command -v gpg &> /dev/null; then
            error "GPG not found but encryption is enabled"
            exit 1
        fi

        # Check if GPG key exists
        if ! gpg --list-keys "$GPG_RECIPIENT" &> /dev/null; then
            warning "GPG key for $GPG_RECIPIENT not found. Encryption may fail."
            info "Generate key with: gpg --full-generate-key"
        else
            success "GPG key found for encryption"
        fi
    fi

    # Check rclone if cloud sync enabled
    if [ "$ENABLE_CLOUD_SYNC" = "yes" ]; then
        if ! command -v rclone &> /dev/null; then
            error "rclone not found but cloud sync is enabled"
            exit 1
        fi

        # Check if rclone remote exists
        if ! rclone listremotes | grep -q "^${RCLONE_REMOTE}:"; then
            warning "rclone remote '${RCLONE_REMOTE}' not configured"
            info "Configure with: rclone config"
            ENABLE_CLOUD_SYNC="no"
        else
            success "rclone remote '${RCLONE_REMOTE}' configured"
        fi
    fi

    # Check project directory
    if [ ! -d "$PROJECT_DIR" ]; then
        error "Project directory not found: $PROJECT_DIR"
        exit 1
    fi
    success "Project directory found: $PROJECT_DIR"

    # Check backup destination
    if [ ! -d "$BACKUP_BASE_DIR" ]; then
        error "Backup destination not found: $BACKUP_BASE_DIR"
        info "Run: mkdir -p $BACKUP_BASE_DIR/{daily,weekly,monthly,critical,logs}"
        exit 1
    fi
    success "Backup destination ready: $BACKUP_BASE_DIR"

    # Check available space
    local available_space=$(df -BG "$BACKUP_BASE_DIR" | tail -1 | awk '{print $4}' | sed 's/G//')
    if [ "$available_space" -lt 10 ]; then
        warning "Low disk space: ${available_space}GB available"
    else
        success "Sufficient disk space: ${available_space}GB available"
    fi
}

################################################################################
# CONTAINER HEALTH CHECKS
################################################################################

check_containers_health() {
    section "🏥 CONTAINER HEALTH CHECKS"

    local containers=("$DB_CONTAINER" "$REDIS_CONTAINER" "$API_CONTAINER")
    local all_healthy=true

    for container in "${containers[@]}"; do
        if ! docker ps --format "{{.Names}}" | grep -q "^${container}$"; then
            error "Container not running: $container"
            all_healthy=false
        else
            local status=$(docker inspect --format='{{.State.Status}}' "$container")
            if [ "$status" = "running" ]; then
                success "Container healthy: $container ($status)"
            else
                warning "Container status: $container ($status)"
            fi
        fi
    done

    if [ "$all_healthy" = false ]; then
        error "Some containers are not healthy. Aborting backup."
        exit 1
    fi
}

################################################################################
# BACKUP FUNCTIONS
################################################################################

backup_postgresql() {
    section "🗄️ POSTGRESQL BACKUP"

    local db_backup_path="${TEMP_DIR}/${DB_BACKUP_NAME}"

    info "Backing up PostgreSQL database..."
    info "Database: nexus_memory"
    info "Container: $DB_CONTAINER"

    # Get database statistics
    local episode_count=$(docker exec "$DB_CONTAINER" psql -U nexus_superuser -d nexus_memory -t -c "SELECT COUNT(*) FROM nexus_memory.zep_episodic_memory;" | xargs || echo "0")
    local embedding_count=$(docker exec "$DB_CONTAINER" psql -U nexus_superuser -d nexus_memory -t -c "SELECT COUNT(*) FROM nexus_memory.zep_episodic_memory WHERE embedding IS NOT NULL;" | xargs || echo "0")

    info "Episodes in database: $episode_count"
    info "Episodes with embeddings: $embedding_count"

    # Perform backup
    if docker exec "$DB_CONTAINER" pg_dump -U nexus_superuser -d nexus_memory --verbose 2>>"$LOG_FILE" | gzip > "$db_backup_path"; then
        local file_size=$(du -h "$db_backup_path" | cut -f1)
        success "PostgreSQL backup completed: $file_size"

        # Verify integrity
        if gunzip -t "$db_backup_path" 2>/dev/null; then
            success "Backup integrity verified (gzip)"
        else
            error "Backup file corrupted!"
            return 1
        fi

        # Store statistics
        echo "$episode_count" > "${TEMP_DIR}/db_episode_count.txt"
        echo "$embedding_count" > "${TEMP_DIR}/db_embedding_count.txt"
    else
        error "PostgreSQL backup failed"
        return 1
    fi
}

backup_redis() {
    section "📝 REDIS BACKUP"

    local redis_backup_path="${TEMP_DIR}/${REDIS_BACKUP_NAME}"

    info "Backing up Redis cache..."
    info "Container: $REDIS_CONTAINER"

    # Trigger BGSAVE
    if docker exec "$REDIS_CONTAINER" redis-cli BGSAVE &>> "$LOG_FILE"; then
        info "Redis BGSAVE triggered, waiting for completion..."

        # Wait for BGSAVE to complete (max 60 seconds)
        local timeout=60
        local elapsed=0
        while [ $elapsed -lt $timeout ]; do
            if docker exec "$REDIS_CONTAINER" redis-cli LASTSAVE &>> "$LOG_FILE"; then
                sleep 2
                elapsed=$((elapsed + 2))
                if [ $((elapsed % 10)) -eq 0 ]; then
                    info "Waiting for BGSAVE... ${elapsed}s"
                fi
            fi
        done

        # Copy dump file
        if docker cp "${REDIS_CONTAINER}:/data/dump.rdb" "$redis_backup_path" 2>>"$LOG_FILE"; then
            local file_size=$(du -h "$redis_backup_path" | cut -f1)
            success "Redis backup completed: $file_size"
        else
            warning "Failed to copy Redis dump (cache may be empty)"
            touch "$redis_backup_path"  # Create empty file to avoid errors
        fi
    else
        warning "Redis backup failed (non-critical)"
        touch "$redis_backup_path"
    fi
}

backup_project_files() {
    section "📦 PROJECT FILES BACKUP"

    local project_backup_path="${TEMP_DIR}/${PROJECT_BACKUP_NAME}"
    local exclusion_file="${TEMP_DIR}/exclusions.txt"

    # Create exclusion list
    cat > "$exclusion_file" << 'EOF'
node_modules
__pycache__
.venv
venv
venv_*
.vs
.vscode
.idea
*.pyc
*.pyo
*.pyd
.Python
*.so
*.dylib
*.dll
pip-log.txt
pip-delete-this-directory.txt
.tox
.coverage
.coverage.*
htmlcov
.pytest_cache
.mypy_cache
.dmypy.json
dmypy.json
.next
.nuxt
dist
build
*.egg-info
backups
*.log
logs
monitoring/prometheus/data
monitoring/grafana/data
.git/objects
.git/logs
EOF

    info "Backing up project files..."
    info "Source: $PROJECT_DIR"
    info "Exclusions: $(wc -l < "$exclusion_file") patterns"

    # Create tar archive with exclusions
    cd "$PROJECT_DIR" || exit 1

    if tar -czf "$project_backup_path" \
           --exclude-from="$exclusion_file" \
           --exclude-vcs-ignores \
           . 2>>"$LOG_FILE"; then
        local file_size=$(du -h "$project_backup_path" | cut -f1)
        success "Project files backup completed: $file_size"

        # Verify integrity
        if tar -tzf "$project_backup_path" > /dev/null 2>&1; then
            success "Tar archive integrity verified"
        else
            error "Tar archive corrupted!"
            return 1
        fi
    else
        error "Project files backup failed"
        return 1
    fi
}

create_manifest() {
    section "📋 CREATING BACKUP MANIFEST"

    local manifest_file="${TEMP_DIR}/manifest.json"

    # Calculate checksums
    local db_checksum=$(sha256sum "${TEMP_DIR}/${DB_BACKUP_NAME}" | cut -d' ' -f1)
    local redis_checksum=$(sha256sum "${TEMP_DIR}/${REDIS_BACKUP_NAME}" | cut -d' ' -f1)
    local project_checksum=$(sha256sum "${TEMP_DIR}/${PROJECT_BACKUP_NAME}" | cut -d' ' -f1)

    # Get file sizes
    local db_size=$(stat -c%s "${TEMP_DIR}/${DB_BACKUP_NAME}")
    local redis_size=$(stat -c%s "${TEMP_DIR}/${REDIS_BACKUP_NAME}")
    local project_size=$(stat -c%s "${TEMP_DIR}/${PROJECT_BACKUP_NAME}")

    # Read database statistics
    local episode_count=$(cat "${TEMP_DIR}/db_episode_count.txt" 2>/dev/null || echo "0")
    local embedding_count=$(cat "${TEMP_DIR}/db_embedding_count.txt" 2>/dev/null || echo "0")

    # Create manifest
    cat > "$manifest_file" << EOF
{
  "backup_id": "${BACKUP_NAME}",
  "backup_type": "${BACKUP_TYPE}",
  "timestamp": "$(date -Iseconds)",
  "version": "3.0.0",
  "project": {
    "name": "CEREBRO_NEXUS_V3.0.0",
    "version": "3.0.0",
    "location": "${PROJECT_DIR}"
  },
  "components": {
    "postgresql": {
      "file": "${DB_BACKUP_NAME}",
      "size": ${db_size},
      "checksum_sha256": "${db_checksum}",
      "database": "nexus_memory",
      "container": "${DB_CONTAINER}",
      "episode_count": ${episode_count},
      "embedding_count": ${embedding_count}
    },
    "redis": {
      "file": "${REDIS_BACKUP_NAME}",
      "size": ${redis_size},
      "checksum_sha256": "${redis_checksum}",
      "container": "${REDIS_CONTAINER}"
    },
    "project_files": {
      "file": "${PROJECT_BACKUP_NAME}",
      "size": ${project_size},
      "checksum_sha256": "${project_checksum}",
      "excluded_patterns": "node_modules, venv*, __pycache__, .next, dist, build, backups"
    }
  },
  "system_info": {
    "hostname": "$(hostname)",
    "user": "$(whoami)",
    "docker_version": "$(docker --version | cut -d' ' -f3 | tr -d ',')",
    "os": "$(uname -s)",
    "os_version": "$(uname -r)"
  },
  "encryption": {
    "enabled": $([ "$ENABLE_ENCRYPTION" = "yes" ] && echo "true" || echo "false"),
    "algorithm": "AES256",
    "gpg_recipient": "${GPG_RECIPIENT}"
  },
  "cloud_sync": {
    "enabled": $([ "$ENABLE_CLOUD_SYNC" = "yes" ] && echo "true" || echo "false"),
    "provider": "Google Drive",
    "remote": "${RCLONE_REMOTE}",
    "path": "${RCLONE_PATH}"
  }
}
EOF

    success "Manifest created: $manifest_file"
    info "Total backup size: $(du -sh "$TEMP_DIR" | cut -f1)"
}

create_complete_archive() {
    section "📦 CREATING COMPLETE ARCHIVE"

    local complete_archive_path="${BACKUP_DIR}/${COMPLETE_BACKUP_NAME}"

    info "Combining all components into single archive..."
    info "Destination: $complete_archive_path"

    # Create complete archive
    cd "$TEMP_DIR" || exit 1

    if tar -czf "$complete_archive_path" \
           "${DB_BACKUP_NAME}" \
           "${REDIS_BACKUP_NAME}" \
           "${PROJECT_BACKUP_NAME}" \
           "manifest.json" \
           "db_episode_count.txt" \
           "db_embedding_count.txt" \
           2>>"$LOG_FILE"; then
        local file_size=$(du -h "$complete_archive_path" | cut -f1)
        success "Complete archive created: $file_size"

        # Verify integrity
        if tar -tzf "$complete_archive_path" > /dev/null 2>&1; then
            success "Complete archive integrity verified"
        else
            error "Complete archive corrupted!"
            return 1
        fi

        # Store final checksum
        local final_checksum=$(sha256sum "$complete_archive_path" | cut -d' ' -f1)
        echo "$final_checksum" > "${complete_archive_path}.sha256"
        success "Checksum saved: ${COMPLETE_BACKUP_NAME}.sha256"
    else
        error "Failed to create complete archive"
        return 1
    fi
}

encrypt_backup() {
    if [ "$ENABLE_ENCRYPTION" != "yes" ]; then
        info "Encryption disabled. Skipping."
        return 0
    fi

    section "🔒 ENCRYPTING BACKUP"

    local complete_archive_path="${BACKUP_DIR}/${COMPLETE_BACKUP_NAME}"
    local encrypted_path="${BACKUP_DIR}/${ENCRYPTED_BACKUP_NAME}"

    info "Encrypting backup with GPG..."
    info "Recipient: $GPG_RECIPIENT"
    info "Algorithm: AES256"

    if gpg --encrypt \
           --recipient "$GPG_RECIPIENT" \
           --cipher-algo AES256 \
           --output "$encrypted_path" \
           "$complete_archive_path" 2>>"$LOG_FILE"; then
        local encrypted_size=$(du -h "$encrypted_path" | cut -f1)
        success "Backup encrypted: $encrypted_size"

        # Calculate encrypted checksum
        local encrypted_checksum=$(sha256sum "$encrypted_path" | cut -d' ' -f1)
        echo "$encrypted_checksum" > "${encrypted_path}.sha256"
        success "Encrypted checksum saved"

        # Remove unencrypted archive
        info "Removing unencrypted archive..."
        rm -f "$complete_archive_path" "${complete_archive_path}.sha256"
        success "Unencrypted archive removed (security)"
    else
        error "Encryption failed"
        return 1
    fi
}

sync_to_cloud() {
    if [ "$ENABLE_CLOUD_SYNC" != "yes" ]; then
        info "Cloud sync disabled. Skipping."
        return 0
    fi

    section "☁️ SYNCING TO GOOGLE DRIVE"

    info "Syncing backups to Google Drive..."
    info "Remote: ${RCLONE_REMOTE}:${RCLONE_PATH}"

    # Determine which file to sync (encrypted or not)
    local file_to_sync
    if [ "$ENABLE_ENCRYPTION" = "yes" ]; then
        file_to_sync="${BACKUP_DIR}/${ENCRYPTED_BACKUP_NAME}"
    else
        file_to_sync="${BACKUP_DIR}/${COMPLETE_BACKUP_NAME}"
    fi

    if [ ! -f "$file_to_sync" ]; then
        error "Backup file not found: $file_to_sync"
        return 1
    fi

    # Sync to Google Drive with progress
    if rclone copy "$file_to_sync" "${RCLONE_REMOTE}:${RCLONE_PATH}/" \
           --progress \
           --stats-one-line \
           --log-level INFO \
           2>>"$LOG_FILE"; then
        success "Backup synced to Google Drive"

        # Sync checksum file
        if [ -f "${file_to_sync}.sha256" ]; then
            rclone copy "${file_to_sync}.sha256" "${RCLONE_REMOTE}:${RCLONE_PATH}/" 2>>"$LOG_FILE"
            success "Checksum synced to Google Drive"
        fi
    else
        error "Failed to sync to Google Drive"
        return 1
    fi
}

cleanup_temp_files() {
    section "🧹 CLEANING UP TEMPORARY FILES"

    if [ -d "$TEMP_DIR" ]; then
        info "Removing temporary directory: $TEMP_DIR"
        rm -rf "$TEMP_DIR"
        success "Temporary files cleaned up"
    fi
}

apply_retention_policy() {
    section "🗑️ APPLYING RETENTION POLICY"

    local retention_days
    case "$BACKUP_TYPE" in
        daily)
            retention_days=$RETENTION_DAILY
            ;;
        weekly)
            retention_days=$RETENTION_WEEKLY
            ;;
        monthly)
            retention_days=$RETENTION_MONTHLY
            ;;
        critical)
            info "Critical backups are never auto-deleted"
            return 0
            ;;
    esac

    info "Retention policy: Keep last $retention_days days for $BACKUP_TYPE backups"

    local deleted_count=0

    # Find and delete old backups
    if [ -d "$BACKUP_DIR" ]; then
        while IFS= read -r old_backup; do
            info "Deleting old backup: $(basename "$old_backup")"
            rm -f "$old_backup"
            deleted_count=$((deleted_count + 1))
        done < <(find "$BACKUP_DIR" -name "*.tar.gz*" -type f -mtime +$retention_days)
    fi

    if [ $deleted_count -gt 0 ]; then
        success "Deleted $deleted_count old backup(s)"
    else
        info "No old backups to delete"
    fi
}

################################################################################
# MAIN BACKUP FUNCTION
################################################################################

main() {
    # Create log directory
    mkdir -p "$LOG_DIR"

    # Start backup
    section "🚀 NEXUS V2.0.0 COMPLETE BACKUP SYSTEM"
    log "Backup Type: $BACKUP_TYPE"
    log "Timestamp: $TIMESTAMP"
    log "Destination: $BACKUP_DIR"

    # Send start notification
    send_notification \
        "Backup Started" \
        "Type: **${BACKUP_TYPE}**\nTimestamp: ${TIMESTAMP}" \
        "info"

    # Track start time
    local start_time=$(date +%s)

    # Check prerequisites
    check_prerequisites

    # Check container health
    check_containers_health

    # Create temporary directory
    mkdir -p "$TEMP_DIR"
    mkdir -p "$BACKUP_DIR"

    # Perform backups
    backup_postgresql || { error "PostgreSQL backup failed"; exit 1; }
    backup_redis || { warning "Redis backup failed (non-critical)"; }
    backup_project_files || { error "Project files backup failed"; exit 1; }

    # Create manifest
    create_manifest

    # Create complete archive
    create_complete_archive || { error "Failed to create complete archive"; exit 1; }

    # Encrypt if enabled
    encrypt_backup || { warning "Encryption failed (non-critical)"; }

    # Sync to cloud if enabled
    sync_to_cloud || { warning "Cloud sync failed (non-critical)"; }

    # Cleanup
    cleanup_temp_files

    # Apply retention policy
    apply_retention_policy

    # Calculate duration
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    local duration_min=$((duration / 60))
    local duration_sec=$((duration % 60))

    # Final summary
    section "✅ BACKUP COMPLETED SUCCESSFULLY"

    local final_backup_file
    if [ "$ENABLE_ENCRYPTION" = "yes" ]; then
        final_backup_file="${BACKUP_DIR}/${ENCRYPTED_BACKUP_NAME}"
    else
        final_backup_file="${BACKUP_DIR}/${COMPLETE_BACKUP_NAME}"
    fi

    success "Backup completed in ${duration_min}m ${duration_sec}s"
    success "Final backup: $(basename "$final_backup_file")"
    success "Backup size: $(du -h "$final_backup_file" | cut -f1)"
    success "Log file: $LOG_FILE"

    if [ "$ENABLE_ENCRYPTION" = "yes" ]; then
        info "🔒 Backup is encrypted with GPG"
    fi

    if [ "$ENABLE_CLOUD_SYNC" = "yes" ]; then
        info "☁️ Backup synced to Google Drive: ${RCLONE_REMOTE}:${RCLONE_PATH}"
    fi

    # Send success notification
    send_notification \
        "Backup Completed Successfully ✅" \
        "Type: **${BACKUP_TYPE}**\nDuration: ${duration_min}m ${duration_sec}s\nSize: $(du -h "$final_backup_file" | cut -f1)\nEncrypted: $([ "$ENABLE_ENCRYPTION" = "yes" ] && echo "Yes 🔒" || echo "No")\nCloud Sync: $([ "$ENABLE_CLOUD_SYNC" = "yes" ] && echo "Yes ☁️" || echo "No")" \
        "success"
}

################################################################################
# ERROR HANDLING
################################################################################

handle_error() {
    local exit_code=$?
    error "Backup failed with exit code: $exit_code"

    # Send error notification
    send_notification \
        "Backup Failed ❌" \
        "Type: **${BACKUP_TYPE}**\nError Code: ${exit_code}\nCheck log: ${LOG_FILE}" \
        "error"

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

# Validate backup type
case "$BACKUP_TYPE" in
    daily|weekly|monthly|critical)
        ;;
    *)
        error "Invalid backup type: $BACKUP_TYPE"
        echo "Usage: $0 [daily|weekly|monthly|critical]"
        exit 1
        ;;
esac

# Run main function
main "$@"

exit 0
