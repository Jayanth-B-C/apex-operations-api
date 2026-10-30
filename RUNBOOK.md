# Operations Runbook – Apex Operations API

## 1. Start the Application

From the project directory:

```cmd
docker compose up -d --build
```

Check container status:

```cmd
docker compose ps
```

## 2. Verify Application Health

```cmd
curl http://localhost:8000/api/health/
curl http://localhost:8000/api/ready/
curl http://localhost:8000/api/version/
```

Expected results:
- Health endpoint returns `healthy`.
- Readiness endpoint returns `ready` with database connected.
- Version endpoint displays the deployed image version.

## 3. Deploy a New Version

Deploy an already-built image:

```cmd
scripts\deploy.bat v1.1.0
```

Verify the deployment:

```cmd
curl http://localhost:8000/api/version/
docker compose ps
```

## 4. Rollback

If a release causes problems, deploy the previous available image:

```cmd
scripts\rollback.bat v1.0.0
```

Verify the version:

```cmd
curl http://localhost:8000/api/version/
```

## 5. Incident Investigation – Database Failure

Simulate a database outage:

```cmd
docker compose stop db
```

Check application readiness:

```cmd
curl -i http://localhost:8000/api/ready/
```

The expected result is HTTP 503 because the database is unavailable.

Investigate:

```cmd
docker compose ps
docker compose logs --tail=50 web
docker compose logs --tail=50 db
```

## 6. Recovery

Restart the database:

```cmd
docker compose start db
```

Wait until PostgreSQL becomes healthy:

```cmd
docker compose ps
```

Check readiness again:

```cmd
curl http://localhost:8000/api/ready/
```

Expected result: database connected.

## 7. Troubleshooting

| Problem | Investigation |
|---|---|
| API unavailable | Check `docker compose ps` and web logs |
| Database connection failure | Check database status and logs |
| Incorrect application version | Check `/api/version/` |
| Container startup failure | Check Compose logs and environment configuration |
| Test failure | Run Django tests and inspect the failure |

## 8. Observability and Alerting

The application provides health and readiness endpoints. The metrics endpoint currently returns demonstration data only.

Recommended production monitoring:
- API availability and response time.
- HTTP 5xx error rate.
- Database connectivity.
- Container CPU and memory usage.
- Alerts for repeated health-check failures.

Prometheus and Grafana could be introduced for metrics and dashboards.

## 9. Safe Shutdown

```cmd
docker compose down
```

Do not use `docker compose down -v` unless database volume deletion is intended.