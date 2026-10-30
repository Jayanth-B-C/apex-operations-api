# Apex Operations API

A containerized Django REST API demonstrating basic DevOps practices, including Docker, PostgreSQL, automated testing, CI, image scanning, health checks, versioned deployment and rollback.

## Technology Stack

- Python and Django REST Framework
- PostgreSQL 17
- Docker and Docker Compose
- Gunicorn
- GitHub Actions
- Ruff for linting
- Trivy for container vulnerability scanning

## Prerequisites

- Git
- Docker Desktop with Docker Compose
- Python (optional, for local development)

## Setup and Run

1. Clone the repository:

   ```cmd
   git clone https://github.com/Jayanth-B-C/apex-operations-api.git
   cd apex-operations-api
   ```

2. Create your local environment file:

   ```cmd
   copy .env.example .env
   ```

3. Update `.env` with a local database password.

4. Build and start the application:

   ```cmd
   docker compose up -d --build
   ```

   Docker Compose starts PostgreSQL and the API. Database migrations run when the application starts.

5. Check running containers:

   ```cmd
   docker compose ps
   ```

## API Endpoints

| Endpoint           | Purpose               |
| ------------------ | --------------------- |
| `/api/health/`     | Application health    |
| `/api/ready/`      | Database readiness    |
| `/api/version/`    | Application version   |
| `/api/operations/` | List operations       |
| `/api/metrics/`    | Demo metrics response |

Example:

```cmd
curl http://localhost:8000/api/health/
```

## Run Automated Tests

```cmd
docker compose exec web python manage.py test
```

Run lint checks locally:

```cmd
ruff check config operations manage.py
```

The intentional failure demonstration is kept separate from the normal test suite:

```cmd
docker compose exec web python manage.py test operations.failure_demo.IntentionalFailureDemo.test_intentional_failure_example
```

This test is expected to fail and is used to demonstrate failure detection.

## Versioned Deployment and Rollback

Build a versioned image:

```cmd
set APP_IMAGE=apex-operations-api:v1.1.0
set APP_VERSION=v1.1.0
docker compose build web
```

Deploy the image:

```cmd
scripts\deploy.bat v1.1.0
```

Roll back to a previous image:

```cmd
scripts\rollback.bat v1.0.0
```

Verify the deployed version:

```cmd
curl http://localhost:8000/api/version/
```

These scripts use previously built local images.

## Stop the Application

```cmd
docker compose down
```

To preserve the PostgreSQL data volume, do not use the `-v` option.

## CI Pipeline

The GitHub Actions workflow performs:

1. Dependency installation
2. Ruff lint checks
3. Django automated tests
4. Docker image build
5. Trivy vulnerability scanning

The pipeline blocks later steps when an earlier check fails. It does not automatically deploy the application.

## Security Notes

- Application runs as a non-root Linux user.
- Database configuration is supplied through environment variables.
- The local `.env` file is excluded from Git.
- The repository uses a separate `.env.example` template.
- Trivy scans the container image for high and critical vulnerabilities.

## Limitations and Future Improvements

- The metrics endpoint currently returns demonstration data, not live request metrics.
- Production monitoring and alerting could be added using Prometheus and Grafana.
- A cloud deployment could use a managed PostgreSQL database and a container hosting service.
- Production secrets should be managed using a dedicated secrets manager.

## Assessment Scope

This project uses synthetic demonstration data and local Docker resources. It is intended to demonstrate fundamental application deployment, CI, security, observability and rollback practices.
