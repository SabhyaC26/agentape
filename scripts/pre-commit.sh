#!/bin/bash
# Pre-commit hook for agentape
# Runs ruff linting on staged Python files
#
# To install this hook, run:
#   cp scripts/pre-commit.sh .git/hooks/pre-commit
#   chmod +x .git/hooks/pre-commit

set -e

echo "🔍 Running pre-commit checks..."

# Get list of staged Python files
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '\.py$' || true)

if [ -z "$STAGED_FILES" ]; then
    echo "✅ No Python files to check"
    exit 0
fi

echo "Checking files:"
echo "$STAGED_FILES"

# Run ruff check on staged files
echo ""
echo "Running ruff check..."
ruff check $STAGED_FILES

# Run ruff format check (without modifying files)
echo ""
echo "Checking formatting..."
ruff format --check $STAGED_FILES

echo ""
echo "✅ Pre-commit checks passed!"
