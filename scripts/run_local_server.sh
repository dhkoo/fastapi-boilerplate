#!/bin/bash

usage() {
    echo "Usage: $0 [-e ENV_NAME] [-p PORT]"
    echo "  -e ENV_NAME    Set the environment name (default: local)"
    echo "                 Available environments: local, dev, stage, prod"
    echo "  -p PORT        Set the port number (default: 8000)"
    echo "  -h             Display this help message"
    echo
    echo "Note: This script looks for environment-specific .env files in the env directory."
    echo "      For example, for the 'prod' environment, it will use 'env/.env.prod' if it exists."
    exit 1
}

ENV_NAME="local"
PORT=8000

while getopts ":e:p:h" opt; do
    case ${opt} in
        e )
            ENV_NAME=$OPTARG
            ;;
        p )
            PORT=$OPTARG
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
ENV_FILE="env/.env.${ENV_NAME}"
if [ -f "$ENV_FILE" ]; then
    echo "Using environment file: $ENV_FILE"
    set -a
    source "$ENV_FILE"
    set +a
else
    echo "Warning: No environment file found at $ENV_FILE"
    exit 1
fi


FULL_COMMAND="ENV_NAME=$ENV_NAME uvicorn app.main:app --reload --port $PORT"
echo "[Executing Command]: $FULL_COMMAND"

eval $FULL_COMMAND