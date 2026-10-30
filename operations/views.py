from django.db import connection
from django.db.utils import OperationalError
from django.http import JsonResponse
from rest_framework.decorators import api_view

from .models import Operation


@api_view(['GET'])
def health_check(request):
    return JsonResponse({
        "status": "healthy",
        "service": "apex-operations-api"
    })


@api_view(['GET'])
def readiness_check(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")

        return JsonResponse({
            "status": "ready",
            "database": "connected"
        })

    except OperationalError:
        return JsonResponse({
            "status": "not_ready",
            "database": "unavailable"
        }, status=503)


@api_view(['GET'])
def operations_list(request):
    operations = Operation.objects.all().order_by('-created_at')

    data = [
        {
            "id": operation.id,
            "name": operation.name,
            "description": operation.description,
            "status": operation.status,
            "created_at": operation.created_at.isoformat()
        }
        for operation in operations
    ]

    return JsonResponse({
        "count": len(data),
        "operations": data
    })


@api_view(['GET'])
def metrics(request):
    return JsonResponse({
        "requests_total": 0,
        "service": "apex-operations-api"
    })