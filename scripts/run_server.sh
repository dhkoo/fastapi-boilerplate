#!/bin/bash

usage() {
    echo "Usage: $0 [-p PORT] [-m]"
    echo "  -p PORT        Set the port number (default: 8000)"
    echo "  -m             Run database migrations before starting the server"
    echo "  -h             Display this help message"
    exit 1
}

PORT=8000
RUN_MIGRATIONS=false

while getopts ":e:p:mh" opt; do
    case ${opt} in
        p )
            PORT=$OPTARG
            ;;
        m )
            RUN_MIGRATIONS=true
            ;;
        h )
            usage
            ;;
        \? )
            echo "Invalid option: $OPTARG" 1>&2
            usage
            ;;
        : )
            echo "Invalid option: $OPTARG requires an argument" 1>&2
            usage
            ;;
    esac
done

cd "$(dirname "$0")"/..

# Check if a .env file exists for the specified environment
ENV_FILE=".env"
if [ -f "$ENV_FILE" ]; then
    echo "Using environment file: $ENV_FILE"
    set -a
    source "$ENV_FILE"
    set +a
else
    echo "Warning: No environment file found at $ENV_FILE"
    exit 1
fi
# Run migrations if the -m flag is set
if [ "$RUN_MIGRATIONS" = true ]; then
    echo "Running database migrations..."
    ./scripts/manage_migration.sh upgrade
    if [ $? -ne 0 ]; then
        echo "Error: Database migration failed. Exiting."
        exit 1
    fi
fi

FULL_COMMAND="ENV_NAME=$ENV_NAME uvicorn app.main:app --reload --host 0.0.0.0 --port $PORT"
echo "[Executing Command]: $FULL_COMMAND"
eval $FULL_COMMAND