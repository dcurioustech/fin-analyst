#!/bin/bash

# Development setup script for Financial Analysis Assistant
set -e

echo "🔧 Setting up Financial Analysis Assistant for local development"

# Check Python version
python_version=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
required_version="3.11"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 3.11+ is required. Current version: $python_version"
    exit 1
fi

echo "✅ Python version: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file..."
    cat > .env << 'EOF'
# API Keys
GOOGLE_API_KEY=your_google_api_key_here
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
POLYGON_API_KEY=your_polygon_key_here

# Development settings
ENVIRONMENT=development
LOG_LEVEL=INFO

# GCP settings (for local development with GCP services)
# PROJECT_ID=fin-analyst-470122
# REDIS_HOST=localhost
# REDIS_PORT=6379
# STORAGE_BUCKET=your-bucket-name

# Local Redis (if running locally)
# REDIS_URL=redis://localhost:6379
EOF
    
    echo "📝 Created .env file. Please update it with your API keys."
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs
mkdir -p data/cache
mkdir -p static

# Run tests to verify setup
echo "🧪 Running basic tests..."
python -m pytest tests/ -v --tb=short || echo "⚠️  Some tests failed, but setup is complete"

echo ""
echo "✅ Development setup complete!"
echo ""
echo "Next steps:"
echo "1. Update .env file with your API keys"
echo "2. Start the development server:"
echo "   python web_app.py"
echo ""
echo "3. Or run the CLI interface:"
echo "   python chat_interface.py"
echo ""
echo "4. Run tests:"
echo "   python -m pytest tests/"
echo ""
echo "5. For GCP development, set up local services:"
echo "   - Install and run Redis locally"
echo "   - Set up GCP credentials: gcloud auth application-default login"