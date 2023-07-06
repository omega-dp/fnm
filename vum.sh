#!/bin/bash

# Start the Django server in the background using nohup
start_server() {
  nohup ./manage.py runserver 178.18.254.142:8000 > server.log 2>&1 &
  echo "Django server started. PID: $!"
}

# Get the PID of the currently running Django server process
get_server_pid() {
  local pid=$(pgrep -f "manage.py runserver")
  if [ -n "$pid" ]; then
    echo "Django server is running. PID: $pid"
  else
    echo "Django server is not running."
  fi
}

# Stop the Django server process
stop_server() {
  local pid=$(pgrep -f "manage.py runserver")
  if [ -n "$pid" ]; then
    echo "Stopping Django server (PID: $pid)..."
    kill "$pid"
    echo "Django server stopped."
  else
    echo "Django server is not running."
  fi
}

# Display usage instructions
usage() {
  echo "Usage: ./django_server.sh [start|stop|status]"
}

# Main script logic
if [ $# -eq 0 ]; then
  usage
  exit 1
fi

case "$1" in
  start)
    start_server
    ;;
  stop)
    stop_server
    ;;
  status)
    get_server_pid
    ;;
  *)
    usage
    exit 1
    ;;
esac

exit 0
