from django.urls import path, include
from rest_framework.routers import DefaultRouter

from projects import views


router = DefaultRouter()
router.register('organization', views.OrganizationViewSet)

app_name = 'projects'

urlpatterns = [
    path('', include(router.urls))
]