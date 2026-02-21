#!/bin/bash
# Run Ticketclue Django app locally.
# Run from terminal:  bash run_local.sh   (or:  cd flight-prod && bash run_local.sh)
# Prerequisites: sudo apt install python3.12-venv python3-pip

# Keep terminal open on error so you can read the message
on_exit() {
  err=$?
  if [ $err -ne 0 ]; then
    echo ""
    read -p "Press Enter to close..."
  fi
}
trap on_exit EXIT

set -e
# Resolve script dir so venv is always created in project folder (avoid e.g. /usr/bin/venv)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"
VENV_DIR="$SCRIPT_DIR/venv"

# Create venv if missing or incomplete (e.g. venv dir exists but bin/activate does not)
if [ ! -f "$VENV_DIR/bin/activate" ]; then
  echo "Creating virtual environment in $VENV_DIR ..."
  rm -rf "$VENV_DIR"
  python3 -m venv "$VENV_DIR"
fi
source "$VENV_DIR/bin/activate"

# Install deps
pip install -q -r requirements.txt

# Migrate DB (requires PostgreSQL running and .env configured)
python manage.py migrate --noinput

# Run server
echo "Starting server at http://127.0.0.1:8000/"
python manage.py runserver
