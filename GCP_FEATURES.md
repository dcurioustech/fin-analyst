# GCP Infrastructure and Enhanced Chat Interface

This document describes the new GCP infrastructure setup and enhanced conversational interface features added to the Financial Analysis Assistant.

## 🚀 New Features

### 1. Google Cloud Platform Integration

#### Infrastructure as Code
- **Terraform Configuration**: Complete infrastructure setup with `infrastructure/gcp/terraform/`
- **Automated Deployment**: One-command deployment with `infrastructure/gcp/deploy.sh`
- **Cloud Build**: Automated CI/CD pipeline with `infrastructure/gcp/cloudbuild.yaml`

#### GCP Services Integration
- **Cloud Run**: Serverless hosting with auto-scaling
- **Firestore**: Session persistence and conversation history
- **Memorystore (Redis)**: High-performance caching layer
- **Cloud Storage**: File storage for reports and charts
- **Secret Manager**: Secure API key management
- **Cloud Monitoring**: Application observability and alerting

### 2. Enhanced Web Interface

#### Modern Web Application
- **FastAPI Backend**: High-performance async web framework
- **Real-time Chat**: WebSocket support for instant responses
- **Session Management**: Persistent conversations across sessions
- **Responsive Design**: Works on desktop and mobile devices

#### API Endpoints
- `GET /` - Web chat interface
- `GET /health` - Health check and service status
- `POST /api/chat` - Chat API for programmatic access
- `WebSocket /ws/{session_id}` - Real-time chat connection
- `GET /api/sessions/{session_id}` - Session information
- `DELETE /api/sessions/{session_id}` - Clear session data

### 3. Enhanced CLI Interface

#### Session Persistence
- **Local Storage**: JSON-based session storage for local development
- **GCP Integration**: Firestore-backed sessions for production
- **Session Management**: Resume conversations, clear sessions
- **Cross-Platform**: Works with both local and cloud backends

#### New CLI Features
```bash
# Resume a specific session
python chat_interface.py --session-id my-session

# Clear session before starting
python chat_interface.py --clear-session

# Start with custom session ID
python chat_interface.py --session-id analysis-2024-01-15
```

## 🏗️ Architecture Overview

### Local Development
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   CLI/Web UI    │───▶│   Application    │───▶│  Local Storage  │
│                 │    │   (FastAPI)      │    │   (JSON files)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   LangGraph      │
                       │   (Financial     │
                       │    Analysis)     │
                       └──────────────────┘
```

### Production (GCP)
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Web Users     │───▶│   Cloud Run      │───▶│   Firestore     │
│                 │    │   (FastAPI)      │    │   (Sessions)    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌──────────────────┐    ┌─────────────────┐
                       │   Memorystore    │    │ Secret Manager  │
                       │   (Redis Cache)  │    │  (API Keys)     │
                       └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   LangGraph      │
                       │   (Financial     │
                       │    Analysis)     │
                       └──────────────────┘
```

## 🛠️ Setup and Deployment

### Quick Start (Local Development)
```bash
# Setup development environment
./scripts/dev_setup.sh

# Start web interface
python web_app.py

# Or start CLI interface
python chat_interface.py
```

### GCP Deployment
```bash
# One-command deployment
./infrastructure/gcp/deploy.sh your-project-id us-central1 prod

# Manual deployment with Terraform
cd infrastructure/gcp/terraform
terraform init
terraform apply
```

### Testing
```bash
# Test local setup
python scripts/test_deployment.py --local-only

# Test deployed service
python scripts/test_deployment.py --url https://your-service-url

# Comprehensive test
python scripts/test_deployment.py
```

## 📊 Configuration

### Environment Variables
The application now supports comprehensive configuration through environment variables:

```bash
# API Keys
GOOGLE_API_KEY=your_key_here
ALPHA_VANTAGE_API_KEY=optional_key
POLYGON_API_KEY=optional_key

# GCP Configuration
PROJECT_ID=your-gcp-project
REGION=us-central1
ENVIRONMENT=production

# Application Settings
LOG_LEVEL=INFO
PORT=8080
```

### GCP Services Configuration
All GCP services are configured through the Terraform modules:

- **Auto-scaling**: 0-100 instances based on demand
- **Memory**: 2Gi per instance (configurable)
- **CPU**: 2 vCPU per instance (configurable)
- **Timeout**: 5 minutes for long-running analysis
- **Caching**: Redis with 1-hour TTL for sessions

## 🔒 Security Features

### API Key Management
- **Secret Manager**: All API keys stored securely in GCP Secret Manager
- **Runtime Access**: Keys accessed at runtime, never stored in containers
- **Least Privilege**: Service accounts with minimal required permissions

### Network Security
- **HTTPS Only**: All traffic encrypted in transit
- **VPC Integration**: Redis accessible only from Cloud Run
- **IAM Controls**: Fine-grained access control for all resources

### Data Protection
- **Session Encryption**: All session data encrypted at rest
- **Audit Logging**: All API access logged for security monitoring
- **Data Retention**: Automatic cleanup of old sessions and cache data

## 📈 Performance Optimizations

### Caching Strategy
- **Redis Cache**: Session data cached for fast access
- **Local Fallback**: JSON file storage when Redis unavailable
- **TTL Management**: Automatic expiration of cached data

### Async Processing
- **FastAPI**: Async/await for non-blocking operations
- **Connection Pooling**: Efficient database connections
- **Concurrent Requests**: Handle multiple users simultaneously

### Resource Management
- **Auto-scaling**: Scale to zero when not in use
- **Memory Optimization**: Efficient memory usage patterns
- **CPU Optimization**: Optimized for financial data processing

## 🔍 Monitoring and Observability

### Built-in Monitoring
- **Health Checks**: Comprehensive health endpoint
- **Service Status**: Real-time status of all GCP services
- **Performance Metrics**: Response times and error rates

### Cloud Monitoring Integration
- **Automatic Metrics**: CPU, memory, request metrics
- **Custom Metrics**: Business logic metrics
- **Alerting**: Automated alerts for issues
- **Dashboards**: Pre-configured monitoring dashboards

### Logging
- **Structured Logging**: JSON-formatted logs for analysis
- **Log Levels**: Configurable logging levels
- **Cloud Logging**: Centralized log management
- **Error Tracking**: Automatic error reporting

## 🚀 Usage Examples

### Web Interface
1. Open your browser to the deployed URL
2. Start chatting: "Analyze Apple's financials"
3. Follow up: "How does it compare to Microsoft?"
4. Session automatically saved and restored

### API Usage
```python
import requests

# Chat API
response = requests.post('https://your-service/api/chat', json={
    'message': 'Analyze Tesla',
    'session_id': 'my-session'
})

data = response.json()
print(data['response'])
```

### CLI Usage
```bash
# Start new session
python chat_interface.py

# Resume specific session
python chat_interface.py --session-id analysis-session-1

# Clear and start fresh
python chat_interface.py --clear-session
```

## 🔄 Migration from Previous Version

### Backward Compatibility
- **Existing CLI**: Original `main.py` still works unchanged
- **Analysis Functions**: All existing analysis capabilities preserved
- **Configuration**: Existing `.env` files compatible

### New Capabilities
- **Session Persistence**: Conversations now persist across restarts
- **Web Access**: Access from any browser, no CLI required
- **Scalability**: Handle multiple users simultaneously
- **Cloud Integration**: Professional-grade infrastructure

## 📚 Additional Resources

- **[Deployment Guide](DEPLOYMENT_GUIDE.md)**: Complete deployment instructions
- **[API Documentation](web_app.py)**: FastAPI auto-generated docs at `/docs`
- **[Terraform Modules](infrastructure/gcp/terraform/)**: Infrastructure as code
- **[Test Suite](scripts/test_deployment.py)**: Comprehensive testing tools

## 🤝 Contributing

When contributing to the GCP infrastructure:

1. **Create Feature Branch**: Always work on feature branches
2. **Test Locally**: Use `scripts/test_deployment.py --local-only`
3. **Test Deployment**: Deploy to dev environment first
4. **Update Documentation**: Update relevant documentation
5. **Security Review**: Ensure security best practices

## 📞 Support

For GCP-related issues:
1. Check Cloud Run logs: `gcloud logs read "resource.type=cloud_run_revision"`
2. Verify service status: `gcloud run services list`
3. Test health endpoint: `curl https://your-service/health`
4. Review monitoring dashboards in GCP Console