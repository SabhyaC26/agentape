#!/bin/bash
# Lint script for agentape project

set -e

echo "🔍 Running ruff linter..."
ruff check agentape/ tests/ example.py

echo "✨ Running ruff formatter..."
ruff format agentape/ tests/ example.py

echo "✅ Linting complete!"
