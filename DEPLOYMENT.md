# 🚀 Deployment Guide - Amharic Dataset MCP Tools

Complete deployment instructions for production and development environments.

## 📦 Quick Start

### Local Development

```bash
# Clone and install
git clone <repository-url>
cd amharic-dataset-mcp
pip install -e ".[dev]"

# Start MCP server
amharic-dataset-server --port 3001
```

### Docker Deployment

```bash
# Build image
docker build -t amharic-dataset-mcp .

# Run container
docker run -d -p 3001:3001 \
  -v ./data:/app/data \
  --name amharic-mcp \
  amharic-dataset-mcp
```

### Claude Code Integration

Add to your Claude Code settings:

```json
{
  "mcpServers": {
    "amharic-dataset": {
      "command": "amharic-dataset-server",
      "args": ["--port", "3001"]
    }
  }
}
```

## 🏗️ Production Deployment

### 1. Environment Setup

```bash
# Production dependencies
pip install amharic-dataset-mcp

# Environment variables
export LOG_LEVEL=INFO
export DATABASE_URL=postgresql://user:pass@localhost/amharic_db
export MCP_PORT=3001
```

### 2. Database Configuration

**PostgreSQL (Recommended)**:
```bash
# Setup PostgreSQL
docker run -d \
  --name amharic-postgres \
  -e POSTGRES_DB=amharic_db \
  -e POSTGRES_USER=amharic_user \
  -e POSTGRES_PASSWORD=secure_password \
  -p 5432:5432 \
  -v amharic_data:/var/lib/postgresql/data \
  postgres:15

# Create indexes
docker exec amharic-postgres psql -U amharic_user -d amharic_db -c "
CREATE INDEX idx_amharic_text_gin ON amharic_authentic_data USING gin(to_tsvector('english', text));
CREATE INDEX idx_source ON amharic_authentic_data (source);  
CREATE INDEX idx_quality ON amharic_authentic_data (quality_score);
"
```

### 3. Load Balancer Configuration

**Nginx Configuration**:
```nginx
upstream amharic_mcp {
    server 127.0.0.1:3001;
    server 127.0.0.1:3002; 
    server 127.0.0.1:3003;
}

server {
    listen 80;
    server_name amharic-mcp.example.com;
    
    location / {
        proxy_pass http://amharic_mcp;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 4. Scaling Configuration

**Docker Compose for Scaling**:
```yaml
version: '3.8'

services:
  amharic-mcp-1:
    build: .
    ports:
      - "3001:3001"
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/amharic_db
      - MCP_PORT=3001
    depends_on:
      - postgres
      - redis
    
  amharic-mcp-2:
    build: .
    ports:
      - "3002:3001"
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/amharic_db  
      - MCP_PORT=3001
    depends_on:
      - postgres
      - redis
      
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: amharic_db
      POSTGRES_USER: amharic_user
      POSTGRES_PASSWORD: secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      
  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

## 🔧 Configuration Options

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `MCP_PORT` | `3001` | MCP server port |
| `DATABASE_URL` | `sqlite:///amharic_dataset.db` | Database connection URL |
| `MAX_WORKERS` | `4` | Number of worker processes |
| `BATCH_SIZE` | `100` | Default batch processing size |
| `QUALITY_THRESHOLD` | `0.6` | Default quality threshold |

### Configuration File

Create `config.json`:
```json
{
  "server": {
    "port": 3001,
    "workers": 4,
    "timeout": 30
  },
  "database": {
    "url": "postgresql://user:pass@localhost/amharic_db",
    "pool_size": 10,
    "max_overflow": 20
  },
  "collection": {
    "sources": ["bbc_amharic", "voa_amharic"],
    "max_items_per_source": 1000,
    "rate_limit_delay": 1.0
  },
  "quality": {
    "threshold": 0.6,
    "enhancement_enabled": true,
    "scoring_weights": {
      "grammar": 0.30,
      "cultural": 0.20,
      "naturalness": 0.15,
      "purity": 0.25,
      "vocabulary": 0.10
    }
  }
}
```

## 🔍 Monitoring & Observability

### Health Checks

```bash
# Server health
curl http://localhost:3001/health

# Database connectivity
curl http://localhost:3001/health/db

# Tool availability
curl http://localhost:3001/health/tools
```

### Logging Configuration

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/amharic-mcp.log'),
        logging.StreamHandler()
    ]
)
```

### Metrics Collection

```python
# Prometheus metrics example
from prometheus_client import Counter, Histogram, start_http_server

# Define metrics
REQUESTS_TOTAL = Counter('amharic_mcp_requests_total', 'Total requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('amharic_mcp_request_duration_seconds', 'Request duration')

# Start metrics server
start_http_server(8000)
```

## 🛡️ Security Configuration

### Authentication

```python
# API key authentication
API_KEYS = {
    "client_1": "api_key_1",
    "client_2": "api_key_2" 
}

async def authenticate_request(request):
    api_key = request.headers.get("X-API-Key")
    return api_key in API_KEYS
```

### Rate Limiting

```python
# Redis-based rate limiting
import aioredis
from aioredis import Redis

async def rate_limit_check(client_id: str, limit: int = 100):
    redis: Redis = await aioredis.from_url("redis://localhost")
    current = await redis.incr(f"rate_limit:{client_id}")
    if current == 1:
        await redis.expire(f"rate_limit:{client_id}", 3600)  # 1 hour
    return current <= limit
```

## 📈 Performance Tuning

### Database Optimization

```sql
-- PostgreSQL optimization
ALTER TABLE amharic_authentic_data SET (fillfactor = 90);
CREATE INDEX CONCURRENTLY idx_text_length ON amharic_authentic_data (length);
CREATE INDEX CONCURRENTLY idx_timestamp ON amharic_authentic_data (timestamp);

-- Analyze tables
ANALYZE amharic_authentic_data;
```

### Memory Optimization

```python
# Memory-efficient batch processing
async def process_large_dataset(items, batch_size=1000):
    for i in range(0, len(items), batch_size):
        batch = items[i:i+batch_size]
        await process_batch(batch)
        # Clear batch from memory
        del batch
        await asyncio.sleep(0.1)  # Prevent blocking
```

## 🔄 Backup & Recovery

### Database Backup

```bash
# PostgreSQL backup
pg_dump -h localhost -U amharic_user -d amharic_db > amharic_backup.sql

# Automated backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump -h localhost -U amharic_user -d amharic_db | gzip > "amharic_backup_$DATE.sql.gz"
```

### Data Recovery

```bash
# Restore from backup
gunzip -c amharic_backup_20240813_120000.sql.gz | psql -h localhost -U amharic_user -d amharic_db
```

## 🚀 Deployment Checklist

### Pre-deployment

- [ ] Environment variables configured
- [ ] Database setup and optimized
- [ ] SSL certificates installed
- [ ] Load balancer configured
- [ ] Monitoring systems ready
- [ ] Backup procedures tested

### Deployment

- [ ] Build and test Docker images
- [ ] Deploy to staging environment
- [ ] Run integration tests
- [ ] Deploy to production
- [ ] Verify health checks pass
- [ ] Monitor initial traffic

### Post-deployment

- [ ] Monitor performance metrics
- [ ] Check error rates and logs
- [ ] Verify data quality
- [ ] Test scaling behavior
- [ ] Document any issues

## 📞 Support & Troubleshooting

### Common Issues

**Connection Timeouts**:
```bash
# Increase timeout settings
export MCP_TIMEOUT=60
```

**Memory Issues**:
```bash
# Reduce batch sizes
export BATCH_SIZE=50
export MAX_WORKERS=2
```

**Database Connection Issues**:
```bash
# Check connection pool
export DB_POOL_SIZE=20
export DB_MAX_OVERFLOW=10
```

### Log Analysis

```bash
# Search for errors
grep "ERROR" /var/log/amharic-mcp.log | tail -20

# Monitor performance
grep "duration" /var/log/amharic-mcp.log | awk '{print $NF}' | sort -n
```

---

**🇪🇹 Ready for production deployment of Ethiopian language AI tools!**