# Unburden America Docker Setup

Complete Docker environment for the Unburden America agent system with n8n workflow automation.

## 🚀 Quick Start

### Prerequisites
- Docker Engine 20.10+
- Docker Compose 2.0+
- 4GB+ RAM available for containers
- 10GB+ disk space

### One-Command Setup
```bash
chmod +x docker-setup.sh
./docker-setup.sh
```

### Manual Setup
1. **Copy environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit configuration:**
   ```bash
   nano .env
   # Set secure passwords and API keys
   ```

3. **Start services:**
   ```bash
   docker-compose up -d
   ```

## 🏗️ Architecture

### Services Overview

| Service | Port | Description |
|---------|------|-------------|
| **n8n** | 5678 | Workflow automation engine |
| **agent-api** | 8000 | Agent orchestration API |
| **content-service** | 8001 | Video/image generation |
| **analytics-service** | 8002 | KPI tracking & reporting |
| **petition-service** | 8003 | Petition & certificates |
| **postgres** | 5432 | Primary database |
| **redis** | 6379 | Caching & job queues |
| **nginx** | 80/443 | Reverse proxy |

### Data Flow
```
User Request → nginx → n8n → Agent API → AI Services
                  ↓
Analytics ← Content ← Petition ← Verification Gates
```

## 🔧 Configuration

### Required Environment Variables
```bash
# Security (CHANGE THESE!)
POSTGRES_PASSWORD=your_secure_password
AGENT_DB_PASSWORD=agent_db_password
ANALYTICS_DB_PASSWORD=analytics_db_password
PETITION_DB_PASSWORD=petition_db_password
N8N_JWT_SECRET=your_jwt_secret_32_chars_min
API_SECRET_KEY=your_api_secret_32_chars_min

# AI APIs
OPENAI_API_KEY=sk-your-openai-key
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key

# Email Notifications
SMTP_HOST=smtp.gmail.com
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password
SMTP_SENDER=noreply@your-domain.com

# n8n Workflow Defaults
WEBHOOK_BASE_URL=http://localhost:5678
NOTIFICATION_EMAIL=alerts@your-domain.com
```

### Optional Configuration
```bash
# Development settings
ENVIRONMENT=development
DEBUG=false
LOG_LEVEL=info

# Custom service URLs
N8N_URL=http://localhost:5678
AGENT_API_URL=http://localhost:8000
```

## 📦 n8n Workflow Import

### 1. Access n8n
Open http://localhost:5678 in your browser

### 2. Set Environment Variables
Go to Settings → Environment Variables and add:
```
AGENT_BASE_URL=http://agent-api:8000
WEBHOOK_BASE_URL=http://localhost:5678
NOTIFICATION_EMAIL=alerts@your-domain.com
```

### 3. Set Up Credentials
Create credentials for:
- **Agent API Bearer Token** (HTTP Bearer Auth)
- **Email SMTP** (for notifications)

### 4. Import Workflows
Import in this order:
1. `n8n_pack/workflows/error_handling_workflow.json`
2. `n8n_pack/workflows/main_campaign_workflow.json`
3. `n8n_pack/workflows/petition_workflow.json`
4. `n8n_pack/workflows/analytics_workflow.json`

### 5. Activate Workflows
- ✅ Error Handling (always active)
- ✅ Analytics (daily reports)
- ✅ Petition (live processing)
- 🟡 Main Campaign (manual trigger)

## 🧪 Testing

### Health Checks
```bash
# Check all services
curl http://localhost:8000/health  # Agent API
curl http://localhost:8001/health  # Content Service
curl http://localhost:8002/health  # Analytics Service
curl http://localhost:8003/health  # Petition Service
curl http://localhost:5678/healthz # n8n
```

### Test Agent API
```bash
curl -X POST http://localhost:8000/agents/policy-fact-check \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-token" \
  -d '{"payload": {"claim_text": "Test claim", "context": "Testing"}}'
```

### Test Petition Flow
```bash
curl -X POST http://localhost:8003/sign \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com", 
    "zip_code": "12345",
    "consent_updates": true
  }'
```

## 📊 Monitoring & Logs

### View Service Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f agent-api
docker-compose logs -f n8n
```

### Container Status
```bash
# Check running containers
docker-compose ps

# Resource usage
docker stats
```

### Database Access
```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U n8n -d n8n

# Connect to Redis
docker-compose exec redis redis-cli
```

## 🛠️ Management Commands

### Start/Stop Services
```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# Restart specific service
docker-compose restart agent-api
```

### Update Services
```bash
# Pull latest images
docker-compose pull

# Rebuild and restart
docker-compose up -d --build
```

### Backup Data
```bash
# Backup PostgreSQL
docker-compose exec postgres pg_dump -U n8n n8n > backup.sql

# Backup n8n workflows
docker cp $(docker-compose ps -q n8n):/home/node/.n8n ./n8n-backup/
```

## 🔒 Security Considerations

### Production Deployment
- [ ] Change all default passwords
- [ ] Use proper SSL certificates
- [ ] Configure firewall rules
- [ ] Set up log aggregation
- [ ] Enable container scanning
- [ ] Use secrets management

### Network Security
- Services communicate via internal Docker network
- Only necessary ports exposed to host
- nginx provides SSL termination and rate limiting

## 🚨 Troubleshooting

### Common Issues

**Services won't start:**
```bash
# Check Docker daemon
sudo systemctl status docker

# Check resource usage
df -h
free -h
```

**Database connection errors:**
```bash
# Reset database
docker-compose down
docker volume rm webapp_postgres_data
docker-compose up -d postgres
```

**n8n workflows failing:**
- Check credentials are properly configured
- Verify environment variables are set
- Check agent API is responding: `curl http://localhost:8000/health`

**Out of disk space:**
```bash
# Clean up Docker
docker system prune -a
docker volume prune
```

### Log Analysis
```bash
# Check startup logs
docker-compose logs postgres | grep -i ready
docker-compose logs n8n | grep -i started

# Monitor real-time logs
docker-compose logs -f --tail=100
```

## 🆘 Support

### Debug Information
When reporting issues, include:
```bash
# System info
docker version
docker-compose version
cat .env | grep -v PASSWORD | grep -v SECRET | grep -v KEY

# Service status
docker-compose ps
curl -s http://localhost:8000/health | jq .
```

### Reset Environment
```bash
# Nuclear option - destroys all data
docker-compose down -v
docker system prune -a
rm -rf logs/ data/ certificates/ output/
./docker-setup.sh
```