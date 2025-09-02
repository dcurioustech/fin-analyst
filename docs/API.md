# Financial Analysis Bot - API Documentation

This document provides comprehensive API documentation for the Financial Analysis Bot's web interface and programmatic access.

## 🌐 API Overview

The Financial Analysis Bot provides multiple API interfaces:
- **REST API**: For programmatic access and integration
- **WebSocket API**: For real-time chat functionality
- **Health API**: For monitoring and status checks

### Base URL
```
# Local development
http://localhost:8080

# Production (replace with your deployed URL)
https://your-service-url.run.app
```

## 🔗 REST API Endpoints

### Chat API

#### POST /api/chat
Send a message to the financial analysis bot and receive a response.

**Request Body:**
```json
{
  "message": "Analyze AAPL",
  "session_id": "optional-session-id"
}
```

**Response:**
```json
{
  "response": "📊 Apple Inc. (AAPL) - Company Analysis\n=====================================\n...",
  "session_id": "generated-or-provided-session-id",
  "timestamp": "2024-01-15T10:30:00Z",
  "analysis_type": "profile",
  "companies": ["AAPL"],
  "success": true
}
```

**Example Usage:**
```bash
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Analyze Tesla",
    "session_id": "my-analysis-session"
  }'
```

```python
import requests

response = requests.post('http://localhost:8080/api/chat', json={
    'message': 'Compare AAPL and MSFT',
    'session_id': 'comparison-session'
})

data = response.json()
print(data['response'])
```

### Session Management

#### GET /api/sessions/{session_id}
Retrieve information about a specific session.

**Response:**
```json
{
  "session_id": "my-session",
  "created_at": "2024-01-15T10:00:00Z",
  "last_activity": "2024-01-15T10:30:00Z",
  "message_count": 5,
  "companies_analyzed": ["AAPL", "MSFT", "GOOGL"],
  "analysis_types": ["profile", "comparison", "metrics"]
}
```

#### DELETE /api/sessions/{session_id}
Clear a session's conversation history.

**Response:**
```json
{
  "message": "Session cleared successfully",
  "session_id": "my-session",
  "success": true
}
```

### Health and Status

#### GET /health
Comprehensive health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0",
  "environment": "production",
  "components": {
    "database": {
      "status": "healthy",
      "response_time_ms": 12
    },
    "external_apis": {
      "yahoo_finance": {
        "status": "healthy",
        "response_time_ms": 245
      }
    },
    "cache": {
      "status": "healthy",
      "hit_rate": 0.85
    }
  },
  "metrics": {
    "uptime_seconds": 86400,
    "requests_per_minute": 15,
    "active_sessions": 3
  }
}
```

#### GET /
Web chat interface (HTML page).

Returns the interactive web chat interface for browser-based usage.

## 🔌 WebSocket API

### WebSocket Connection
Connect to real-time chat functionality.

**Endpoint:** `/ws/{session_id}`

**Connection:**
```javascript
const ws = new WebSocket('ws://localhost:8080/ws/my-session');

ws.onopen = function(event) {
    console.log('Connected to chat');
};

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Bot response:', data.response);
};

ws.send(JSON.stringify({
    message: 'Analyze Apple'
}));
```

**Message Format:**
```json
{
  "message": "Analyze AAPL",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

**Response Format:**
```json
{
  "response": "📊 Apple Inc. (AAPL) - Company Analysis...",
  "session_id": "my-session",
  "timestamp": "2024-01-15T10:30:15Z",
  "analysis_type": "profile",
  "companies": ["AAPL"],
  "success": true
}
```

## 📊 Request/Response Schemas

### Chat Request Schema
```json
{
  "type": "object",
  "properties": {
    "message": {
      "type": "string",
      "description": "User's financial analysis request",
      "example": "Analyze Apple's financial metrics"
    },
    "session_id": {
      "type": "string",
      "description": "Optional session identifier for conversation context",
      "example": "user-session-123"
    }
  },
  "required": ["message"]
}
```

### Chat Response Schema
```json
{
  "type": "object",
  "properties": {
    "response": {
      "type": "string",
      "description": "Bot's analysis response"
    },
    "session_id": {
      "type": "string",
      "description": "Session identifier"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "Response timestamp"
    },
    "analysis_type": {
      "type": "string",
      "enum": ["profile", "metrics", "income_statement", "balance_sheet", "cash_flow", "comparison"],
      "description": "Type of analysis performed"
    },
    "companies": {
      "type": "array",
      "items": {"type": "string"},
      "description": "List of company ticker symbols analyzed"
    },
    "success": {
      "type": "boolean",
      "description": "Whether the request was successful"
    },
    "error": {
      "type": "string",
      "description": "Error message if success is false"
    }
  },
  "required": ["response", "session_id", "timestamp", "success"]
}
```

## 🔐 Authentication

### Current Status
The API currently operates without authentication for ease of use. All endpoints are publicly accessible.

### Future Authentication (Planned)
```bash
# Future API key authentication
curl -X POST http://localhost:8080/api/chat \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"message": "Analyze AAPL"}'
```

### Rate Limiting
- **Default Limit**: 100 requests per minute per IP
- **Burst Limit**: 10 requests per second
- **Headers**: Rate limit information included in response headers

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1642248600
```

## 🚨 Error Handling

### HTTP Status Codes
- **200 OK**: Successful request
- **400 Bad Request**: Invalid request format or parameters
- **429 Too Many Requests**: Rate limit exceeded
- **500 Internal Server Error**: Server error
- **503 Service Unavailable**: Service temporarily unavailable

### Error Response Format
```json
{
  "error": {
    "code": "INVALID_TICKER",
    "message": "The ticker symbol 'INVALID' was not found",
    "details": {
      "ticker": "INVALID",
      "suggestions": ["AAPL", "MSFT", "GOOGL"]
    }
  },
  "success": false,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Common Error Codes
- **INVALID_TICKER**: Ticker symbol not found
- **ANALYSIS_FAILED**: Analysis could not be completed
- **RATE_LIMIT_EXCEEDED**: Too many requests
- **SESSION_NOT_FOUND**: Session ID not found
- **INVALID_REQUEST**: Malformed request

## 📝 Usage Examples

### Python Client Example
```python
import requests
import json

class FinancialAnalysisClient:
    def __init__(self, base_url="http://localhost:8080"):
        self.base_url = base_url
        self.session_id = None
    
    def analyze(self, message):
        """Send analysis request and return response."""
        response = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "message": message,
                "session_id": self.session_id
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            self.session_id = data.get('session_id')
            return data['response']
        else:
            raise Exception(f"API Error: {response.status_code}")
    
    def clear_session(self):
        """Clear current session."""
        if self.session_id:
            requests.delete(f"{self.base_url}/api/sessions/{self.session_id}")
            self.session_id = None

# Usage
client = FinancialAnalysisClient()
result = client.analyze("Analyze Apple")
print(result)

result = client.analyze("What about Microsoft?")  # Uses context
print(result)
```

### JavaScript Client Example
```javascript
class FinancialAnalysisClient {
    constructor(baseUrl = 'http://localhost:8080') {
        this.baseUrl = baseUrl;
        this.sessionId = null;
    }
    
    async analyze(message) {
        const response = await fetch(`${this.baseUrl}/api/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                session_id: this.sessionId
            })
        });
        
        if (response.ok) {
            const data = await response.json();
            this.sessionId = data.session_id;
            return data.response;
        } else {
            throw new Error(`API Error: ${response.status}`);
        }
    }
    
    async clearSession() {
        if (this.sessionId) {
            await fetch(`${this.baseUrl}/api/sessions/${this.sessionId}`, {
                method: 'DELETE'
            });
            this.sessionId = null;
        }
    }
}

// Usage
const client = new FinancialAnalysisClient();

client.analyze('Analyze Tesla')
    .then(result => console.log(result))
    .catch(error => console.error(error));
```

### cURL Examples
```bash
# Basic analysis
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Analyze AAPL"}'

# With session context
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Compare it with Microsoft",
    "session_id": "my-session"
  }'

# Check health
curl http://localhost:8080/health

# Clear session
curl -X DELETE http://localhost:8080/api/sessions/my-session
```

## 🔧 Configuration

### Environment Variables
The API behavior can be configured through environment variables:

```bash
# Server configuration
PORT=8080
HOST=0.0.0.0

# API settings
MAX_REQUESTS_PER_MINUTE=100
MAX_BURST_REQUESTS=10
SESSION_TIMEOUT_MINUTES=60

# Features
ENABLE_WEBSOCKETS=true
ENABLE_CORS=true
CORS_ORIGINS=["http://localhost:3000", "https://yourdomain.com"]
```

### CORS Configuration
```python
# For web applications
CORS_ORIGINS = [
    "http://localhost:3000",  # React development
    "http://localhost:8080",  # Local testing
    "https://yourdomain.com"  # Production domain
]
```

## 📊 Monitoring and Analytics

### Request Logging
All API requests are logged with the following information:
- Request timestamp
- Endpoint accessed
- Response time
- Status code
- Session ID (if provided)
- Analysis type performed
- Companies analyzed

### Metrics Available
- **Request Rate**: Requests per minute/hour
- **Response Time**: Average and percentile response times
- **Error Rate**: Percentage of failed requests
- **Session Activity**: Active sessions and session duration
- **Analysis Types**: Distribution of analysis types requested
- **Popular Companies**: Most frequently analyzed companies

### Health Monitoring
The `/health` endpoint provides detailed system status:
- **Component Health**: Database, external APIs, cache status
- **Performance Metrics**: Response times, throughput
- **Resource Usage**: Memory, CPU utilization
- **Error Rates**: Recent error statistics

## 🚀 Integration Guide

### Getting Started
1. **Start the service** locally or deploy to production
2. **Test the health endpoint** to verify service is running
3. **Send a test request** to the chat API
4. **Implement error handling** for your use case
5. **Set up session management** if needed

### Best Practices
1. **Use session IDs** for conversational context
2. **Implement retry logic** for network errors
3. **Handle rate limits** gracefully
4. **Cache responses** when appropriate
5. **Monitor API health** regularly

### Production Considerations
1. **Set up monitoring** for API endpoints
2. **Configure rate limiting** based on usage patterns
3. **Implement authentication** if required
4. **Set up logging** and alerting
5. **Plan for scaling** based on demand

---

This API documentation provides everything needed to integrate with the Financial Analysis Bot programmatically. For additional support, refer to the [User Guide](../USER_GUIDE.md) and [Developer Guide](../DEVELOPER_GUIDE.md).