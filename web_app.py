"""
Web Application for Financial Analysis Assistant.

This module provides a FastAPI-based web interface and API
for the Financial Analysis Assistant with GCP integration.
"""

import logging
import os
from contextlib import asynccontextmanager
from typing import Any, Dict, Optional

import redis.asyncio as redis
import uvicorn
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from google.cloud import firestore, storage
from pydantic import BaseModel

from agents.graph import financial_orchestrator
from agents.state import FinancialOrchestratorState, create_initial_state
from config.settings import configure_pandas
from utils.error_handling import setup_logging

# Setup logging
setup_logging("INFO")
logger = logging.getLogger(__name__)

# Global variables for GCP services
db = None
redis_client = None
storage_client = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown."""
    # Startup
    logger.info("Starting Financial Analysis Assistant Web App")

    # Configure pandas
    configure_pandas()

    # Initialize GCP services
    global db, redis_client, storage_client

    try:
        # Initialize Firestore
        db = firestore.Client()
        logger.info("Firestore client initialized")

        # Initialize Redis if available
        redis_host = os.getenv("REDIS_HOST")
        redis_port = int(os.getenv("REDIS_PORT", 6379))

        if redis_host:
            redis_client = redis.Redis(
                host=redis_host, port=redis_port, decode_responses=True
            )
            await redis_client.ping()
            logger.info("Redis client initialized")
        else:
            logger.warning("Redis not configured - caching disabled")

        # Initialize Cloud Storage
        storage_client = storage.Client()
        logger.info("Cloud Storage client initialized")

    except Exception as e:
        logger.error(f"Error initializing GCP services: {e}")
        # Continue without GCP services for local development

    yield

    # Shutdown
    logger.info("Shutting down Financial Analysis Assistant Web App")
    if redis_client:
        await redis_client.close()


# Create FastAPI app
app = FastAPI(
    title="Financial Analysis Assistant",
    description="AI-powered financial analysis and conversation assistant",
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models
class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    session_id: str
    companies: list = []
    analysis_type: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    version: str
    services: Dict[str, str]


# Connection manager for WebSocket connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        self.active_connections[session_id] = websocket
        logger.info(f"WebSocket connected: {session_id}")

    def disconnect(self, session_id: str):
        if session_id in self.active_connections:
            del self.active_connections[session_id]
            logger.info(f"WebSocket disconnected: {session_id}")

    async def send_message(self, message: str, session_id: str):
        if session_id in self.active_connections:
            await self.active_connections[session_id].send_text(message)


manager = ConnectionManager()


# Routes
@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main chat interface."""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Financial Analysis Assistant</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .header { background: #2196F3; color: white; padding: 20px; border-radius: 10px 10px 0 0; text-align: center; }
            .chat-container { height: 400px; overflow-y: auto; padding: 20px; border-bottom: 1px solid #eee; }
            .message { margin: 10px 0; padding: 10px; border-radius: 5px; }
            .user-message { background: #e3f2fd; margin-left: 20%; text-align: right; }
            .bot-message { background: #f5f5f5; margin-right: 20%; }
            .input-container { padding: 20px; display: flex; gap: 10px; }
            .input-container input { flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
            .input-container button { padding: 10px 20px; background: #2196F3; color: white; border: none; border-radius: 5px; cursor: pointer; }
            .input-container button:hover { background: #1976D2; }
            .status { padding: 10px; text-align: center; color: #666; font-size: 12px; }
            .loading { color: #2196F3; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🏦 Financial Analysis Assistant</h1>
                <p>Ask me about stocks, companies, and financial analysis</p>
            </div>
            <div class="chat-container" id="chatContainer">
                <div class="message bot-message">
                    👋 Hello! I'm your Financial Analysis Assistant. I can help you analyze companies, compare stocks, and provide financial insights. Try asking me something like "Analyze Apple" or "Compare Tesla and Ford".
                </div>
            </div>
            <div class="status" id="status">Ready</div>
            <div class="input-container">
                <input type="text" id="messageInput" placeholder="Ask me about any company or stock..." onkeypress="handleKeyPress(event)">
                <button onclick="sendMessage()">Send</button>
            </div>
        </div>

        <script>
            let sessionId = Math.random().toString(36).substring(7);
            
            function addMessage(content, isUser = false) {
                const chatContainer = document.getElementById('chatContainer');
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
                messageDiv.innerHTML = content.replace(/\\n/g, '<br>');
                chatContainer.appendChild(messageDiv);
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }
            
            function setStatus(text, isLoading = false) {
                const status = document.getElementById('status');
                status.textContent = text;
                status.className = isLoading ? 'status loading' : 'status';
            }
            
            async function sendMessage() {
                const input = document.getElementById('messageInput');
                const message = input.value.trim();
                
                if (!message) return;
                
                addMessage(message, true);
                input.value = '';
                setStatus('Analyzing...', true);
                
                try {
                    const response = await fetch('/api/chat', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            message: message,
                            session_id: sessionId
                        })
                    });
                    
                    const data = await response.json();
                    
                    if (response.ok) {
                        addMessage(data.response);
                        if (data.companies && data.companies.length > 0) {
                            setStatus(`Context: ${data.companies.join(', ')}`);
                        } else {
                            setStatus('Ready');
                        }
                    } else {
                        addMessage(`Error: ${data.detail || 'Something went wrong'}`);
                        setStatus('Error');
                    }
                } catch (error) {
                    addMessage(`Error: ${error.message}`);
                    setStatus('Error');
                }
            }
            
            function handleKeyPress(event) {
                if (event.key === 'Enter') {
                    sendMessage();
                }
            }
        </script>
    </body>
    </html>
    """


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    services = {
        "firestore": "connected" if db else "disconnected",
        "redis": "connected" if redis_client else "disconnected",
        "storage": "connected" if storage_client else "disconnected",
    }

    return HealthResponse(status="healthy", version="1.0.0", services=services)


@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(chat_message: ChatMessage):
    """Main chat API endpoint."""
    try:
        logger.info(f"Processing chat message: {chat_message.message[:100]}...")

        # Get or create session state
        session_id = chat_message.session_id or f"session_{os.urandom(8).hex()}"
        state = await get_session_state(session_id)

        # Process the message through LangGraph
        result_state = financial_orchestrator.process_user_request(
            chat_message.message, state
        )

        # Save session state
        await save_session_state(session_id, result_state)

        # Return response
        return ChatResponse(
            response=result_state.get(
                "agent_response", "I'm sorry, I couldn't process your request."
            ),
            session_id=session_id,
            companies=result_state.get("companies", []),
            analysis_type=result_state.get("analysis_type"),
        )

    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """WebSocket endpoint for real-time chat."""
    await manager.connect(websocket, session_id)

    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()

            try:
                # Get session state
                state = await get_session_state(session_id)

                # Process message
                result_state = financial_orchestrator.process_user_request(data, state)

                # Save session state
                await save_session_state(session_id, result_state)

                # Send response
                response = {
                    "response": result_state.get(
                        "agent_response", "I'm sorry, I couldn't process your request."
                    ),
                    "companies": result_state.get("companies", []),
                    "analysis_type": result_state.get("analysis_type"),
                }

                await websocket.send_json(response)

            except Exception as e:
                logger.error(f"Error processing WebSocket message: {e}")
                await websocket.send_json({"error": str(e)})

    except WebSocketDisconnect:
        manager.disconnect(session_id)


@app.get("/api/sessions/{session_id}")
async def get_session(session_id: str):
    """Get session information."""
    try:
        state = await get_session_state(session_id)
        return {
            "session_id": session_id,
            "companies": state.get("companies", []),
            "analysis_type": state.get("analysis_type"),
            "message_count": len(state.get("messages", [])),
        }
    except Exception as e:
        logger.error(f"Error getting session: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/sessions/{session_id}")
async def clear_session(session_id: str):
    """Clear session data."""
    try:
        if db:
            db.collection("sessions").document(session_id).delete()

        if redis_client:
            await redis_client.delete(f"session:{session_id}")

        return {"message": "Session cleared successfully"}

    except Exception as e:
        logger.error(f"Error clearing session: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Helper functions
async def get_session_state(session_id: str) -> FinancialOrchestratorState:
    """Get session state from storage."""
    try:
        # Try Redis first (faster)
        if redis_client:
            cached_state = await redis_client.get(f"session:{session_id}")
            if cached_state:
                import json

                return json.loads(cached_state)

        # Try Firestore
        if db:
            doc = db.collection("sessions").document(session_id).get()
            if doc.exists:
                return doc.to_dict()

        # Return new state if not found
        return create_initial_state()

    except Exception as e:
        logger.error(f"Error getting session state: {e}")
        return create_initial_state()


async def save_session_state(session_id: str, state: FinancialOrchestratorState):
    """Save session state to storage."""
    try:
        import json

        # Save to Redis (with TTL)
        if redis_client:
            await redis_client.setex(
                f"session:{session_id}",
                3600,  # 1 hour TTL
                json.dumps(state, default=str),
            )

        # Save to Firestore (persistent)
        if db:
            db.collection("sessions").document(session_id).set(state)

    except Exception as e:
        logger.error(f"Error saving session state: {e}")


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(
        "web_app:app",
        host="0.0.0.0",
        port=port,
        log_level="info",
        reload=os.getenv("ENVIRONMENT") == "development",
    )
