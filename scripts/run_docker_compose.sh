#!/bin/bash

cd "$(dirname "$0")/.." || exit

ENV_FILE=".env"

if [ ! -f "$ENV_FILE" ]; then
    echo "Error: Environment file $ENV_FILE not found."
    exit 1
fi

set -a
source "$ENV_FILE"
set +a

required_vars=("POSTGRES_DB" "POSTGRES_PORT" "POSTGRES_USER" "POSTGRES_PASSWORD" "POSTGRES_HOST")
missing_vars=()

for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        missing_vars+=("$var")
    fi
done

if [ ${#missing_vars[@]} -ne 0 ]; then
    echo "Error: The following required environment variables are not set:"
    printf '%s\n' "${missing_vars[@]}"
    exit 1
fi

echo "Using the following environment variables:"
echo "POSTGRES_DB=$POSTGRES_DB"
echo "POSTGRES_PORT=$POSTGRES_PORT"
echo "POSTGRES_HOST=$POSTGRES_HOST"
echo "POSTGRES_USER=$POSTGRES_USER"
echo "POSTGRES_PASSWORD=********"

docker-compose --env-file "$ENV_FILE" up -d

if [ $? -eq 0 ]; then
    echo "Docker Compose services started successfully."
else
    echo "Error: Failed to start Docker Compose services."
    exit 1
fi

echo "Running containers:"
docker-compose ps