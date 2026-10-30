# Technical Decision Memo – Apex Operations API

**Author:** Jayanth B C
**Date:** 31 October 2026
**Repository:** `apex-operations-api` (GitHub: Jayanth-B-C)

## Objective

Build a small, reproducible application deployment environment demonstrating essential DevOps practices within the assessment scope.

## Key Decisions

1. **Django REST Framework:** Selected because it provides a familiar and straightforward way to implement API endpoints.
2. **PostgreSQL:** Used as the application database, running in a separate Docker container.
3. **Docker Compose:** Used to run the API and database locally with persistent database storage.
4. **Non-root execution:** The API runs as the dedicated Linux user `appuser`.
5. **GitHub Actions:** Automates linting, tests, Docker image building and vulnerability scanning.
6. **Versioned images:** Separate image tags allow deployment of a new version and rollback to a previously built version.

## Security Decisions

- Configuration is supplied through environment variables.
- The local `.env` file is excluded from Git.
- `.env.example` provides a configuration template.
- The application runs as a non-root user.
- Trivy is included in the CI workflow for image vulnerability scanning.
- `pip`, `setuptools` and `wheel` are removed from the final runtime image to reduce its attack surface.

## CI Issues Encountered and Resolved

| Run | Problem | Resolution |
|-----|---------|------------|
| #1 | The pinned Trivy action tag (`0.28.0`) no longer existed, because upstream tags were removed after a security incident in March 2026. | Updated the workflow to a current, maintained version of the action. |
| #2 | Trivy reported 5 HIGH-severity findings in the image (`msgpack`, `setuptools`, `urllib3`), none of them from the project's own dependencies. | Removed `pip`, `setuptools` and `wheel` from the runtime image in the Dockerfile. |
| #3 | None. | All steps passed: checkout, Python setup, dependency install, Ruff lint, Django tests, Docker build and Trivy scan. |

Screenshots of the failed and successful runs are saved in `docs/evidence/`.

## Assumptions and Trade-offs

- Deployment is demonstrated locally using Docker Compose rather than a paid cloud environment.
- Versioned images are local demonstration images; a production release would publish them to a secured container registry.
- The metrics endpoint is currently a placeholder, not a real monitoring system.
- Production deployment would require managed secrets, centralized monitoring, access controls and a managed database.

## Future Cloud Deployment Path

The application could be deployed using a managed container platform, a managed PostgreSQL database, a container registry and a secrets manager. Monitoring and alerting could be implemented using Prometheus and Grafana or equivalent cloud services.

## AI Assistance Disclosure

AI tools, including ChatGPT and Claude, were used to assist with understanding requirements, implementation guidance, troubleshooting, documentation and reviewing configuration.

The project was executed and tested by the author in a local development environment. The implementation, commands, test results and design decisions can be explained and demonstrated by the author during the review.