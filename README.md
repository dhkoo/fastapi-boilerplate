## 🌐 Overview

fastapi-boilerplate is a boilerplate that can serve as a base for FastAPI with PostgreSQL.

## 🚀 Getting Started

### Setting Local Environment

```bash
$ python -m venv .venv
$ source source .venv/bin/activate
```

### Install package and set environment variables

```bash
$ poetry install
$ mv .env.template .env
$ vim .env
```

### Setting postgreSQL container

NOTE. Docker must be running before executing the script.

```bash
$ cd ./scripts
$ ./run_docker_compose.sh
```

### Database Migration and run the API server

```bash
$ ./run_server.sh -m
```
