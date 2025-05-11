#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Activate virtual environment if it exists
if [ -d "$PROJECT_ROOT/venv" ]; then
    source "$PROJECT_ROOT/venv/bin/activate"
fi

# Set up log directories
mkdir -p "$PROJECT_ROOT/logs/collection"

# Function to check if a process is running
check_process() {
    if [ -f "$1" ]; then
        pid=$(cat "$1")
        if ps -p $pid > /dev/null; then
            return 0  # Process is running
        fi
    fi
    return 1  # Process is not running
}

# Function to start a process
start_process() {
    process_name=$1
    script_path=$2
    pid_file=$3
    log_file=$4

    if check_process "$pid_file"; then
        echo "$process_name is already running"
    else
        cd "$PROJECT_ROOT"
        nohup python3 "$script_path" > "$log_file" 2>&1 &
        echo $! > "$pid_file"
        echo "$process_name started with PID $(cat $pid_file)"
    fi
}

# Function to stop a process
stop_process() {
    process_name=$1
    pid_file=$2

    if [ -f "$pid_file" ]; then
        pid=$(cat "$pid_file")
        if ps -p $pid > /dev/null; then
            echo "Stopping $process_name..."
            kill $pid
            rm "$pid_file"
        else
            echo "$process_name is not running"
            rm "$pid_file"
        fi
    else
        echo "$process_name is not running"
    fi
}

# Command line argument handling
case "$1" in
    start)
        # Start ID verification first
        start_process "NBA ID Verification" \
            "scripts/verify_nba_ids.py" \
            "nba_verifier.pid" \
            "logs/collection/nba_verifier_output.log"

        # Wait for verification to complete (5 minutes max)
        echo "Waiting for ID verification to complete..."
        sleep 300

        # Start data collection
        start_process "NBA Data Collection" \
            "scripts/collect_all_nba_data.py" \
            "nba_collector.pid" \
            "logs/collection/nba_collector_output.log"
        ;;
    stop)
        stop_process "NBA Data Collection" "nba_collector.pid"
        stop_process "NBA ID Verification" "nba_verifier.pid"
        ;;
    status)
        if check_process "nba_verifier.pid"; then
            echo "NBA ID Verification is running (PID: $(cat nba_verifier.pid))"
        else
            echo "NBA ID Verification is not running"
        fi
        if check_process "nba_collector.pid"; then
            echo "NBA Data Collection is running (PID: $(cat nba_collector.pid))"
        else
            echo "NBA Data Collection is not running"
        fi
        ;;
    restart)
        $0 stop
        sleep 5
        $0 start
        ;;
    *)
        echo "Usage: $0 {start|stop|status|restart}"
        exit 1
        ;;
esac

exit 0 