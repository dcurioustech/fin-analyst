#!/bin/bash

# Simple deployment wrapper script
# This script can be run from the project root directory

set -e

# Check if we're in the right directory
if [ ! -f "main.py" ] || [ ! -d "infrastructure" ]; then
    echo "❌ Please run this script from the project root directory"
    echo "   (the directory containing main.py and infrastructure/)"
    exit 1
fi

# Run the actual deployment script
exec ./infrastructure/gcp/deploy.sh "$@"