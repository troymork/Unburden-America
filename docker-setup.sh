#!/usr/bin/env bash
set -euo pipefail

echo "🚀 Setting up Unburden America Docker Environment"
echo "================================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "   Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "   Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    
    echo ""
    echo "⚠️  IMPORTANT: Edit the .env file with your configuration:"
    echo "   - Set secure passwords for all services"
    echo "   - Add your OpenAI/Anthropic API keys"
    echo "   - Configure SMTP settings for notifications"
    echo ""
    echo "   Edit command: nano .env"
    echo ""
    read -p "Press Enter to continue after editing .env file..."
fi

# Create required directories
echo "📁 Creating required directories..."
mkdir -p {logs,data,certificates,output}

# Pull latest images
echo "📥 Pulling Docker images..."
docker-compose pull

# Build custom services
echo "🔨 Building custom services..."
docker-compose build

# Create network if it doesn't exist
echo "🌐 Setting up Docker network..."
docker network create unburden-net 2>/dev/null || echo "Network already exists"

# Initialize database
echo "🗄️  Starting database..."
docker-compose up -d postgres redis

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
sleep 10

# Start all services
echo "🚀 Starting all services..."
docker-compose up -d

# Wait for services to start
echo "⏳ Waiting for services to initialize..."
sleep 30

# Health check
echo "🏥 Running health checks..."
SERVICES=(
    "http://localhost:8000/health|Agent API"
    "http://localhost:8001/health|Content Service" 
    "http://localhost:8002/health|Analytics Service"
    "http://localhost:8003/health|Petition Service"
    "http://localhost:5678/healthz|n8n"
)

ALL_HEALTHY=true
for service in "${SERVICES[@]}"; do
    IFS='|' read -r url name <<< "$service"
    if curl -f -s "$url" >/dev/null; then
        echo "✅ $name is healthy"
    else
        echo "❌ $name is not responding"
        ALL_HEALTHY=false
    fi
done

echo ""
echo "🎉 Docker Environment Setup Complete!"
echo "====================================="
echo ""

if $ALL_HEALTHY; then
    echo "✅ All services are running and healthy!"
else
    echo "⚠️  Some services may need more time to start. Check logs with:"
    echo "   docker-compose logs [service-name]"
fi

echo ""
echo "🌐 Service URLs:"
echo "   n8n Workflow Engine: http://localhost:5678"
echo "   Agent API: http://localhost:8000/docs"
echo "   Content Service: http://localhost:8001/docs"
echo "   Analytics Service: http://localhost:8002/docs"
echo "   Petition Service: http://localhost:8003/docs"
echo ""
echo "📊 Next Steps:"
echo "   1. Open n8n at http://localhost:5678"
echo "   2. Import workflows from n8n_pack/"
echo "   3. Configure environment variables in n8n"
echo "   4. Set up credentials (Bearer auth + SMTP)"
echo "   5. Test workflows with sample data"
echo ""
echo "📖 Documentation:"
echo "   Setup Guide: n8n_pack/templates/import_instructions.md"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "🛠️  Management Commands:"
echo "   Stop all: docker-compose down"
echo "   View logs: docker-compose logs -f [service]"
echo "   Restart service: docker-compose restart [service]"
echo "   Update services: docker-compose pull && docker-compose up -d"