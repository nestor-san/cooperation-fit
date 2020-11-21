from django.urls import path, include
from rest_framework.routers import DefaultRouter

from projects import views


router = DefaultRouter()
router.register('organization', views.OrganizationViewSet)
router.register('cooperators', views.CooperatorProfileViewSet)
router.register('projects', views.ProjectViewSet)
router.register('portfolio', views.PortfolioItemViewSet)
router.register('cooperation', views.CooperationViewSet)

app_name = 'projects'

urlpatterns = [
    path('', include(router.urls))
]
