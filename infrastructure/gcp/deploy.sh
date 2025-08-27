#!/bin/bash

# Deployment script for Financial Analysis Assistant on GCP
set -e

# Configuration
PROJECT_ID=${1:-"fin-analyst-470122"}
REGION=${2:-"us-central1"}
ENVIRONMENT=${3:-"dev"}

echo "🚀 Deploying Financial Analysis Assistant to GCP"
echo "Project: $PROJECT_ID"
echo "Region: $REGION"
echo "Environment: $ENVIRONMENT"

# Check if gcloud is installed and authenticated
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI is not installed. Please install it first."
    exit 1
fi

# Set the project
gcloud config set project $PROJECT_ID

# Enable required APIs
echo "📡 Enabling required APIs..."
gcloud services enable \
    run.googleapis.com \
    firestore.googleapis.com \
    redis.googleapis.com \
    storage.googleapis.com \
    monitoring.googleapis.com \
    secretmanager.googleapis.com \
    cloudbuild.googleapis.com \
    containerregistry.googleapis.com

# Deploy infrastructure with Terraform (if terraform directory exists)
if [ -d "infrastructure/gcp/terraform" ]; then
    echo "🏗️  Deploying infrastructure with Terraform..."
    cd infrastructure/gcp/terraform
    
    # Initialize Terraform
    terraform init
    
    # Create terraform.tfvars if it doesn't exist
    if [ ! -f "terraform.tfvars" ]; then
        echo "Creating terraform.tfvars..."
        cat > terraform.tfvars << EOF
project_id  = "$PROJECT_ID"
region      = "$REGION"
environment = "$ENVIRONMENT"
EOF
    fi
    
    # Plan and apply
    terraform plan
    terraform apply -auto-approve
    
    cd ../../..
fi

# Build and deploy with Cloud Build
echo "🔨 Building and deploying application..."
gcloud builds submit \
    --config=infrastructure/gcp/cloudbuild.yaml \
    --substitutions=_ENVIRONMENT=$ENVIRONMENT,_REGION=$REGION \
    .

# Get the service URL (after Cloud Build deployment)
echo "⏳ Waiting for service to be available..."
sleep 10
SERVICE_URL=$(gcloud run services describe financial-analysis-assistant-$ENVIRONMENT \
    --region=$REGION \
    --format="value(status.url)" 2>/dev/null || echo "Service not yet deployed")

echo "✅ Deployment complete!"
echo "🌐 Service URL: $SERVICE_URL"
echo ""
echo "Next steps:"
echo "1. Set up your API keys in Secret Manager:"
echo "   - google-api-key-$ENVIRONMENT"
echo "   - alpha-vantage-key-$ENVIRONMENT (optional)"
echo "   - polygon-key-$ENVIRONMENT (optional)"
echo ""
echo "2. Test the deployment:"
echo "   curl $SERVICE_URL/health"
echo ""
echo "3. Access the web interface:"
echo "   open $SERVICE_URL"