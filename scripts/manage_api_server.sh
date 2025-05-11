#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Activate virtual environment if it exists
if [ -d "$PROJECT_ROOT/venv" ]; then
    source "$PROJECT_ROOT/venv/bin/activate"
fi

# Add project root to PYTHONPATH
export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"

# Function to check if the server is running
check_server() {
    if [ -f "$PROJECT_ROOT/api_server.pid" ]; then
        pid=$(cat "$PROJECT_ROOT/api_server.pid")
        if ps -p $pid > /dev/null; then
            return 0  # Server is running
        fi
    fi
    return 1  # Server is not running
}

# Function to start the server
start_server() {
    if check_server; then
        echo "API server is already running"
        return
    fi
    
    cd "$PROJECT_ROOT"
    echo "Starting API server..."
    python scripts/run_api_server.py &
    
    # Wait for server to start
    sleep 2
    if check_server; then
        echo "API server started successfully"
        echo "API server is running on http://localhost:8001"
    else
        echo "Failed to start API server"
    fi
}

# Function to stop the server
stop_server() {
    if [ -f "$PROJECT_ROOT/api_server.pid" ]; then
        pid=$(cat "$PROJECT_ROOT/api_server.pid")
        echo "Stopping API server (PID: $pid)..."
        kill $pid 2>/dev/null
        rm -f "$PROJECT_ROOT/api_server.pid"
    else
        echo "No API server PID file found"
    fi
}

# Function to restart the server
restart_server() {
    stop_server
    sleep 2
    start_server
}

# Function to show server status
status_server() {
    if check_server; then
        pid=$(cat "$PROJECT_ROOT/api_server.pid")
        echo "API server is running (PID: $pid)"
        echo "API server is available at http://localhost:8001"
    else
        echo "API server is not running"
    fi
}

# Parse command line arguments
case "$1" in
    start)
        start_server
        ;;
    stop)
        stop_server
        ;;
    restart)
        restart_server
        ;;
    status)
        status_server
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac

exit 0 