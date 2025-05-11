#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Activate virtual environment if it exists
if [ -d "$PROJECT_ROOT/venv" ]; then
    source "$PROJECT_ROOT/venv/bin/activate"
fi

# Set up log directory
mkdir -p "$PROJECT_ROOT/logs/collection"

# Run the collector script in the background
cd "$PROJECT_ROOT"
nohup python3 scripts/collect_all_nba_data.py > logs/collection/nba_collector_output.log 2>&1 &

# Save the process ID
echo $! > "$PROJECT_ROOT/nba_collector.pid"

echo "NBA collector started in background. Process ID: $!"
echo "Logs are being written to logs/collection/nba_collector_output.log"
echo "To stop the collector, run: kill \$(cat nba_collector.pid)" 