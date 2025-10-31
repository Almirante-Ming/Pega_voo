#!/bin/bash

set -e

COMPOSE_FILE="docker-compose.postgres.yml"
CONTAINER_NAME="task_fly_postgres"

case "$1" in
    start)
        echo "🚀 Starting PostgreSQL 17 container..."
        docker-compose -f $COMPOSE_FILE up -d
        echo "⏳ Waiting for PostgreSQL to be ready..."
        sleep 5
        docker-compose -f $COMPOSE_FILE exec postgres pg_isready -U tinto -d task_fly_db
        echo "✅ PostgreSQL is ready!"
        echo "📊 Connection details:"
        echo "   Host: localhost"
        echo "   Port: 5454"
        echo "   Database: task_fly_db"
        echo "   User: tinto"
        echo "   Password: masterkey"
        ;;
    
    stop)
        echo "🛑 Stopping PostgreSQL container..."
        docker-compose -f $COMPOSE_FILE down
        echo "✅ PostgreSQL stopped"
        ;;
    
    restart)
        echo "🔄 Restarting PostgreSQL container..."
        docker-compose -f $COMPOSE_FILE restart
        echo "✅ PostgreSQL restarted"
        ;;
    
    logs)
        echo "📋 Showing PostgreSQL logs..."
        docker-compose -f $COMPOSE_FILE logs -f postgres
        ;;
    
    connect)
        echo "🔌 Connecting to PostgreSQL..."
        docker-compose -f $COMPOSE_FILE exec postgres psql -U tinto -d task_fly_db
        ;;
    
    status)
        echo "📊 PostgreSQL container status:"
        docker-compose -f $COMPOSE_FILE ps
        echo ""
        echo "🏥 Health check:"
        docker-compose -f $COMPOSE_FILE exec postgres pg_isready -U tinto -d task_fly_db || echo "❌ PostgreSQL not ready"
        ;;
    
    backup)
        BACKUP_FILE="backup_$(date +%Y%m%d_%H%M%S).sql"
        echo "💾 Creating backup: $BACKUP_FILE"
        docker-compose -f $COMPOSE_FILE exec -T postgres pg_dump -U tinto -d task_fly_db > $BACKUP_FILE
        echo "✅ Backup created: $BACKUP_FILE"
        ;;
    
    restore)
        if [ -z "$2" ]; then
            echo "❌ Please provide backup file: $0 restore <backup_file>"
            exit 1
        fi
        echo "📥 Restoring from backup: $2"
        cat "$2" | docker-compose -f $COMPOSE_FILE exec -T postgres psql -U tinto -d task_fly_db
        echo "✅ Backup restored"
        ;;
    
    clean)
        echo "🧹 Removing PostgreSQL container and data..."
        read -p "⚠️  This will delete all data. Continue? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            docker-compose -f $COMPOSE_FILE down -v
            docker volume rm task_fly_postgres_data 2>/dev/null || true
            echo "✅ PostgreSQL container and data removed"
        else
            echo "❌ Operation cancelled"
        fi
        ;;
    
    init)
        echo "🏗️  Initializing PostgreSQL for Task Fly..."
        
        # Start container
        docker-compose -f $COMPOSE_FILE up -d
        
        # Wait for PostgreSQL
        echo "⏳ Waiting for PostgreSQL to be ready..."
        sleep 10
        
        # Check if ready
        until docker-compose -f $COMPOSE_FILE exec postgres pg_isready -U tinto -d task_fly_db; do
            echo "⏳ Still waiting for PostgreSQL..."
            sleep 2
        done
        
        echo "✅ PostgreSQL initialized and ready!"
        echo "🔧 You can now run migrations:"
        echo "   cd src/api && alembic upgrade head"
        ;;
    
    *)
        echo "🐘 PostgreSQL Docker Management for Task Fly"
        echo ""
        echo "Usage: $0 {start|stop|restart|logs|connect|status|backup|restore|clean|init}"
        echo ""
        echo "Commands:"
        echo "  start    - Start PostgreSQL container"
        echo "  stop     - Stop PostgreSQL container"
        echo "  restart  - Restart PostgreSQL container"
        echo "  logs     - Show PostgreSQL logs"
        echo "  connect  - Connect to PostgreSQL CLI"
        echo "  status   - Show container status"
        echo "  backup   - Create database backup"
        echo "  restore  - Restore from backup file"
        echo "  clean    - Remove container and data (DESTRUCTIVE)"
        echo "  init     - Initialize fresh PostgreSQL instance"
        echo ""
        echo "Connection details:"
        echo "  Host: localhost"
        echo "  Port: 5454"
        echo "  Database: task_fly_db"
        echo "  User: tinto"
        echo "  Password: masterkey"
        exit 1
        ;;
esac