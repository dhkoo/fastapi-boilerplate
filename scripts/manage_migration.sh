#!/bin/bash

set -e

cd "$(dirname "$0")"/..

usage() {
    echo "Usage: $0 <command> [options]"
    echo "Commands:"
    echo "  revision <message>  Create a new revision"
    echo "  upgrade [revision]  Upgrade to the latest revision or to a specific revision"
    echo "  downgrade <revision> Downgrade to a specific revision"
    echo "Options:"
    echo "  -h                  Display this help message"
    exit 1
}

if [ $# -eq 0 ]; then
    usage
fi

# Load environment variables
if [ -f ".env" ]; then
    export $(grep -v '^#' .env | xargs)
else
    echo "Error: .env file not found"
    exit 1
fi

case "$1" in
    revision)
        if [ -z "$2" ]; then
            echo "Error: Revision message is required"
            exit 1
        fi
        alembic revision --autogenerate -m "$2"
        ;;
    upgrade)
        if [ -z "$2" ]; then
            alembic upgrade head
        else
            alembic upgrade "$2"
        fi
        ;;
    downgrade)
        if [ -z "$2" ]; then
            echo "Error: Revision is required for downgrade"
            exit 1
        fi
        alembic downgrade "$2"
        ;;
    *)
        usage
        ;;
esac