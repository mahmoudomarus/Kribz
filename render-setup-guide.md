# Render Migration Guide

## Step 1: Setup External Services

### Redis Setup
1. Go to [Upstash Redis](https://console.upstash.com/)
2. Create account and new database
3. Copy the Redis URL (format: `redis://...`)
4. Set as `REDIS_URL` environment variable

### RabbitMQ Setup  
1. Go to [CloudAMQP](https://www.cloudamqp.com/)
2. Create account and new instance (Little Lemur - FREE)
3. Copy the AMQP URL (format: `amqp://...`)
4. Set as `CLOUDAMQP_URL` environment variable

## Step 2: Create Web Service on Render

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repo: `https://github.com/mahmoudomarus/Kribz`
4. Configure:
   - **Name**: `Kribz-Backend`
   - **Environment**: Docker
   - **Root Directory**: `backend`
   - **Dockerfile Path**: `Dockerfile` (relative to root dir)
   - **Region**: Oregon (or closest to you)
   - **Branch**: `main`
   - **Auto-Deploy**: Yes
   - **Health Check Path**: `/api/health`

## Step 3: Create Background Worker

1. Click "New +" → "Background Worker" 
2. Connect same GitHub repo
3. Configure:
   - **Name**: `Kribz-Worker`
   - **Environment**: Docker  
   - **Root Directory**: `backend`
   - **Dockerfile Path**: `Dockerfile`
   - **Start Command**: `uv run dramatiq --skip-logging --processes 2 --threads 2 run_agent_background`
   - **Region**: Oregon (same as web service)
   - **Branch**: `main`
   - **Auto-Deploy**: Yes

## Step 4: Environment Variables (Both Services)

Set these environment variables in both Web Service and Worker:

### Core App Variables
```bash
ENV_MODE=production
PYTHONPATH=/app
```

### Database (Supabase - from your current setup)
```bash
SUPABASE_URL=https://rbsswyljndnvrjnfexya.supabase.co
SUPABASE_ANON_KEY=<your_anon_key>
SUPABASE_SERVICE_ROLE_KEY=<your_service_role_key>
```

### Redis (from Upstash)
```bash
REDIS_URL=<your_upstash_redis_url>
```

### RabbitMQ (from CloudAMQP)
```bash
CLOUDAMQP_URL=<your_cloudamqp_url>
```

### Security
```bash
MCP_CREDENTIAL_ENCRYPTION_KEY=<generate_32_char_key>
```

### Optional (if you use them)
```bash
SENTRY_DSN=<your_sentry_dsn>
LANGFUSE_SECRET_KEY=<your_langfuse_key>
LANGFUSE_PUBLIC_KEY=<your_langfuse_public_key>
LANGFUSE_HOST=<your_langfuse_host>
```

## Step 5: Update Frontend

Update your Vercel frontend environment variable:
```bash
NEXT_PUBLIC_BACKEND_URL=https://kribz-backend.onrender.com
```

## Step 6: Verify Deployment

1. Check Web Service logs for successful startup
2. Check Worker logs for Dramatiq connection to RabbitMQ  
3. Test health endpoint: `https://your-service.onrender.com/api/health`
4. Test end-to-end agent run from frontend

## Notes

- Render free tier spins down after inactivity (first request may be slow)
- Consider upgrading to Starter plan ($7/month) for no spin-down
- Worker and Web service should be in same region for lowest latency
- Monitor logs during initial deployment for any missing environment variables
