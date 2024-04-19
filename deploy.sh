#!/bin/bash

# Define the location of the docker-compose.yml file
COMPOSE_FILE=docker-compose.yml

# Function to check if Docker and docker-compose are installed
check_dependencies() {
    if ! command -v docker &>/dev/null; then
        echo "Error: Docker is not installed or not in the PATH."
        exit 1
    fi

    if ! command -v docker-compose &>/dev/null; then
        echo "Error: docker-compose is not installed or not in the PATH."
        exit 1
    fi
}

# Function to start services
start_services() {
    echo "Starting Docker services..."
    docker-compose -f "$COMPOSE_FILE" up -d --remove-orphans
    if [ $? -ne 0 ]; then
        echo "Error: Failed to start Docker services."
        exit 1
    fi
    echo "Docker services started successfully."
    docker ps
}

# Function to stop services
stop_services() {
    echo "Stopping Docker services..."
    docker-compose -f "$COMPOSE_FILE" down
    if [ $? -ne 0 ]; then
        echo "Error: Failed to stop Docker services."
        exit 1
    fi
    echo "Docker services stopped successfully."

    echo "Removing all unused data..."
    docker system prune -f
    echo "All unused data removed successfully."
}

# Function to restart services
restart_services() {
    stop_services
    start_services
}

# Function to display usage information
usage() {
    echo "Usage: $0 {start|stop|restart}"
    exit 1
}

# Main function
main() {
    check_dependencies

    if [ $# -ne 1 ]; then
        usage
    fi

    case "$1" in
        start)
            start_services
            ;;
        stop)
            stop_services
            ;;
        restart)
            restart_services
            ;;
        *)
            usage
            ;;
    esac
}

# Execute main function with command line arguments
main "$@"
