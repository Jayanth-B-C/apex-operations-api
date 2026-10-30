from django.urls import path

from . import views

urlpatterns = [
    path('health/', views.health_check),
    path('ready/', views.readiness_check),
    path('operations/', views.operations_list),
    path('metrics/', views.metrics),
]