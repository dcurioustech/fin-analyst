# Financial Analysis Assistant - Deployment Guide

This guide covers deploying the Financial Analysis Assistant to Google Cloud Platform (GCP) with full infrastructure setup.

## Prerequisites

### Required Tools
- [Google Cloud SDK (gcloud)](https://cloud.google.com/sdk/docs/install)
- [Terraform](https://developer.hashicorp.com/terraform/downloads) (optional, for infrastructure as code)
- [Docker](https://docs.docker.com/get-docker/) (for local testing)
- Python 3.11+

### Required Accounts & API Keys
- Google Cloud Platform account with billing enabled
- Google AI Studio API key (for Gemini)
- Optional: Alpha Vantage API key
- Optional: Polygon.io API key

## Quick Deployment

### 1. Setup GCP Project

```bash
# Create a new GCP project (or use existing)
gcloud projects create your-project-id --name="Financial Analysis Assistant"

# Set the project
gcloud config set project your-project-id

# Enable billing (required for most services)
# Do this through the GCP Console: https://console.cloud.google.com/billing
```

### 2. Clone and Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd financial-analysis-assistant

# Switch to the deployment branch
git checkout feature/gcp-infrastructure-and-chat-interface

# Run the setup script
chmod +x scripts/dev_setup.sh
./scripts/dev_setup.sh
```

### 3. Configure Environment

```bash
# Copy and edit the environment file
cp .env.example .env

# Edit .env with your API keys
nano .env
```

Required environment variables:
```bash
# API Keys
GOOGLE_API_KEY=your_google_api_key_here
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here  # Optional
POLYGON_API_KEY=your_polygon_key_here              # Optional

# GCP Configuration
PROJECT_ID=your-gcp-project-id
REGION=us-central1
ENVIRONMENT=prod
```

### 4. Deploy to GCP

```bash
# Make the deployment script executable
chmod +x infrastructure/gcp/deploy.sh

# Deploy everything
./infrastructure/gcp/deploy.sh your-project-id us-central1 prod
```

The deployment script will:
- Enable required GCP APIs
- Deploy infrastructure with Terraform (if available)
- Build and deploy the application with Cloud Build
- Provide the service URL

## Manual Deployment Steps

If you prefer to deploy manually or need more control:

### 1. Enable GCP APIs

```bash
gcloud services enable \
    run.googleapis.com \
    firestore.googleapis.com \
    redis.googleapis.com \
    storage.googleapis.com \
    monitoring.googleapis.com \
    secretmanager.googleapis.com \
    cloudbuild.googleapis.com \
    containerregistry.googleapis.com
```

### 2. Deploy Infrastructure with Terraform

```bash
cd infrastructure/gcp/terraform

# Initialize Terraform
terraform init

# Create terraform.tfvars
cat > terraform.tfvars << EOF
project_id  = "your-project-id"
region      = "us-central1"
environment = "prod"
EOF

# Plan and apply
terraform plan
terraform apply
```

### 3. Store API Keys in Secret Manager

```bash
# Store Google API key
echo -n "your_google_api_key" | gcloud secrets create google-api-key-prod --data-file=-

# Store other API keys (optional)
echo -n "your_alpha_vantage_key" | gcloud secrets create alpha-vantage-key-prod --data-file=-
echo -n "your_polygon_key" | gcloud secrets create polygon-key-prod --data-file=-
```

### 4. Build and Deploy Application

```bash
# Build the container
gcloud builds submit --tag gcr.io/your-project-id/financial-analysis-assistant .

# Deploy to Cloud Run
gcloud run deploy financial-analysis-assistant \
    --image gcr.io/your-project-id/financial-analysis-assistant \
    --region us-central1 \
    --platform managed \
    --allow-unauthenticated \
    --port 8080 \
    --memory 2Gi \
    --cpu 2 \
    --max-instances 100 \
    --set-env-vars PROJECT_ID=your-project-id
```

## Local Development

### 1. Setup Local Environment

```bash
# Run the development setup
./scripts/dev_setup.sh

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Local Environment

```bash
# Copy environment template
cp .env.example .env

# Edit with your API keys
nano .env
```

For local development, you can use:
```bash
# Minimal configuration for local development
GOOGLE_API_KEY=your_google_api_key_here
ENVIRONMENT=development
LOG_LEVEL=DEBUG

# Optional: Connect to GCP services from local
# PROJECT_ID=your-gcp-project-id
# GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
```

### 3. Run Locally

```bash
# Run the web application
python web_app.py

# Or run the CLI interface
python chat_interface.py

# Or run the original menu-driven interface
python main.py
```

## Testing the Deployment

### 1. Health Check

```bash
# Get the service URL
SERVICE_URL=$(gcloud run services describe financial-analysis-assistant \
    --region=us-central1 \
    --format="value(status.url)")

# Test health endpoint
curl $SERVICE_URL/health
```

### 2. Test Chat API

```bash
# Test the chat API
curl -X POST $SERVICE_URL/api/chat \
    -H "Content-Type: application/json" \
    -d '{"message": "Analyze Apple"}'
```

### 3. Test Web Interface

Open the service URL in your browser to access the web chat interface.

## Configuration Options

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `PROJECT_ID` | GCP Project ID | Yes | - |
| `REGION` | GCP Region | No | us-central1 |
| `ENVIRONMENT` | Environment (dev/staging/prod) | No | dev |
| `GOOGLE_API_KEY` | Google AI Studio API key | Yes | - |
| `ALPHA_VANTAGE_API_KEY` | Alpha Vantage API key | No | - |
| `POLYGON_API_KEY` | Polygon.io API key | No | - |
| `REDIS_HOST` | Redis host (auto-configured in GCP) | No | - |
| `REDIS_PORT` | Redis port | No | 6379 |
| `STORAGE_BUCKET` | Cloud Storage bucket name | No | auto-generated |

### GCP Services Configuration

#### Cloud Run
- **Memory**: 2Gi (configurable)
- **CPU**: 2 vCPU (configurable)
- **Max Instances**: 100 (configurable)
- **Port**: 8080

#### Firestore
- **Mode**: Native mode
- **Location**: Same as region

#### Redis (Memorystore)
- **Tier**: Basic (1GB)
- **Version**: Redis 6.x

#### Cloud Storage
- **Location**: Same as region
- **Versioning**: Enabled
- **Lifecycle**: 30-day deletion

## Monitoring and Logging

### Cloud Monitoring

The deployment automatically sets up:
- Application metrics
- Error reporting
- Performance monitoring
- Uptime checks

Access monitoring at: https://console.cloud.google.com/monitoring

### Logs

View application logs:
```bash
# View Cloud Run logs
gcloud logs read "resource.type=cloud_run_revision" --limit=50

# Follow logs in real-time
gcloud logs tail "resource.type=cloud_run_revision"
```

## Scaling and Performance

### Auto Scaling

Cloud Run automatically scales based on:
- Request volume
- CPU utilization
- Memory usage

Configure scaling:
```bash
gcloud run services update financial-analysis-assistant \
    --region us-central1 \
    --min-instances 0 \
    --max-instances 100 \
    --concurrency 80
```

### Performance Optimization

1. **Redis Caching**: Enabled automatically for session storage
2. **Connection Pooling**: Built into the application
3. **Async Processing**: FastAPI with async/await
4. **Resource Limits**: Configured for optimal performance

## Security

### Authentication

Currently configured for public access. To add authentication:

```bash
# Remove public access
gcloud run services remove-iam-policy-binding financial-analysis-assistant \
    --region us-central1 \
    --member="allUsers" \
    --role="roles/run.invoker"

# Add authenticated users
gcloud run services add-iam-policy-binding financial-analysis-assistant \
    --region us-central1 \
    --member="user:user@example.com" \
    --role="roles/run.invoker"
```

### API Key Security

- API keys are stored in Secret Manager
- Service account has minimal required permissions
- Secrets are accessed at runtime, not stored in container

## Troubleshooting

### Common Issues

1. **API Key Not Found**
   ```bash
   # Check if secret exists
   gcloud secrets list
   
   # Check secret value
   gcloud secrets versions access latest --secret="google-api-key-prod"
   ```

2. **Service Won't Start**
   ```bash
   # Check Cloud Run logs
   gcloud logs read "resource.type=cloud_run_revision" --limit=10
   ```

3. **Firestore Permission Denied**
   ```bash
   # Check service account permissions
   gcloud projects get-iam-policy your-project-id
   ```

4. **Redis Connection Failed**
   ```bash
   # Check Redis instance status
   gcloud redis instances list --region=us-central1
   ```

### Debug Mode

Enable debug logging:
```bash
gcloud run services update financial-analysis-assistant \
    --region us-central1 \
    --set-env-vars LOG_LEVEL=DEBUG
```

## Cost Optimization

### Estimated Costs (Monthly)

- **Cloud Run**: $10-50 (depending on usage)
- **Firestore**: $5-20 (depending on operations)
- **Redis**: $30-50 (Basic tier)
- **Cloud Storage**: $1-5 (depending on storage)
- **Secret Manager**: $1-2
- **Total**: ~$47-127/month for moderate usage

### Cost Reduction Tips

1. **Use minimum instances**: Set min-instances to 0
2. **Optimize Redis**: Use smaller instance for development
3. **Monitor usage**: Set up billing alerts
4. **Clean up old data**: Implement data retention policies

## Support

For issues or questions:
1. Check the logs first
2. Review this deployment guide
3. Check the main README.md for application-specific help
4. Create an issue in the repository

## Next Steps

After successful deployment:
1. Set up monitoring alerts
2. Configure custom domain (optional)
3. Set up CI/CD pipeline
4. Add authentication if needed
5. Scale based on usage patterns