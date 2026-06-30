#!/bin/bash
# AI Medical Record Extractor - Deployment Script
# This script automates the deployment process

set -e  # Exit on error

echo "=========================================="
echo "AI Medical Record Extractor - Deployment"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
APP_NAME="medical-extractor"
APP_DIR="/opt/medical-extractor"
BACKUP_DIR="/opt/backups/medical-extractor"
LOG_DIR="/var/log/medical-extractor"

# Functions
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

check_command() {
    if command -v $1 &> /dev/null; then
        print_success "$1 is installed"
        return 0
    else
        print_error "$1 is not installed"
        return 1
    fi
}

# Check prerequisites
echo "Checking prerequisites..."
check_command docker
check_command docker-compose
print_success "Prerequisites check complete"
echo ""

# Create backup if deployment exists
if [ -d "$APP_DIR" ]; then
    echo "Creating backup of existing deployment..."
    mkdir -p "$BACKUP_DIR"
    BACKUP_NAME="backup-$(date +%Y%m%d-%H%M%S)"
    cp -r "$APP_DIR/data" "$BACKUP_DIR/$BACKUP_NAME-data" 2>/dev/null || true
    cp -r "$APP_DIR/uploads" "$BACKUP_DIR/$BACKUP_NAME-uploads" 2>/dev/null || true
    print_success "Backup created at $BACKUP_DIR/$BACKUP_NAME"
    echo ""
fi

# Stop existing containers
echo "Stopping existing containers..."
if [ -f docker-compose.yml ]; then
    docker-compose down || true
    print_success "Containers stopped"
else
    print_warning "No docker-compose.yml found"
fi
echo ""

# Build and start services
echo "Building and starting services..."
docker-compose up -d --build

# Wait for services to be ready
echo "Waiting for services to start..."
sleep 10

# Check if backend is healthy
echo "Checking backend health..."
MAX_RETRIES=10
RETRY_COUNT=0
while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if curl -f http://localhost:8000/health &> /dev/null; then
        print_success "Backend is healthy"
        break
    else
        RETRY_COUNT=$((RETRY_COUNT + 1))
        if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
            print_error "Backend health check failed"
            echo "Check logs with: docker-compose logs backend"
            exit 1
        fi
        echo "Retrying... ($RETRY_COUNT/$MAX_RETRIES)"
        sleep 3
    fi
done
echo ""

# Check if frontend is accessible
echo "Checking frontend..."
if curl -f http://localhost/ &> /dev/null; then
    print_success "Frontend is accessible"
else
    print_warning "Frontend check failed (may still be starting)"
fi
echo ""

# Display status
echo "=========================================="
echo "Deployment Status"
echo "=========================================="
docker-compose ps
echo ""

# Display access information
echo "=========================================="
echo "Access Information"
echo "=========================================="
echo "Frontend: http://localhost"
echo "Backend API: http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo "Health Check: http://localhost:8000/health"
echo ""

# Display logs command
echo "=========================================="
echo "Useful Commands"
echo "=========================================="
echo "View logs: docker-compose logs -f"
echo "View backend logs: docker-compose logs -f backend"
echo "View frontend logs: docker-compose logs -f frontend"
echo "Stop services: docker-compose down"
echo "Restart services: docker-compose restart"
echo "Update and redeploy: ./deploy.sh"
echo ""

print_success "Deployment complete!"