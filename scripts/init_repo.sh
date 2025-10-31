#!/usr/bin/env bash
set -euo pipefail

if ! git --version >/dev/null 2>&1; then
  echo "git not found. Install git first." >&2
  exit 1
fi

REPO_NAME="${1:-sql-claims-pipeline-2025}"
GITHUB_USER="${2:-YOUR_GITHUB_USERNAME}"
PRIVATE="${3:-true}"

echo "Initializing local repo..."
git init
git add .
git commit -m "Initial commit: SQL-first claims pipeline (2025)"
git branch -M main

echo "Create the GitHub repo in your account (choose one):"
echo "  1) Web UI: https://github.com/new (name: ${REPO_NAME})"
echo "  2) GitHub CLI: gh repo create ${GITHUB_USER}/${REPO_NAME} --${PRIVATE:+private} --source=. --remote=origin --push"
echo
echo "Once created, set remote & push:"
echo "  git remote add origin git@github.com:${GITHUB_USER}/${REPO_NAME}.git"
echo "  git push -u origin main"

echo "Done."
