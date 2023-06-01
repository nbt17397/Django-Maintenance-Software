from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('user', views.UserViewSet)
router.register('project', views.ProjectViewSet)
router.register('building', views.BuildingViewSet)
router.register('building_detail', views.BuildingDetailViewSet)
router.register('maintenance_area', views.MaintenanceAreaViewSet)
router.register('maintenance_area_detail', views.MaintenanceAreaDetailViewSet)
router.register('process', views.ProcessViewSet)
router.register('checking_way', views.CheckingWayViewSet)
router.register('process_section', views.ProcessSectionViewSet)
router.register('process_step', views.ProcessStepViewSet)
router.register('device_document', views.DeviceDocumentViewSet)
router.register('device', views.DeviceViewSet)
router.register('maintenance_device', views.MaintenanceDeviceViewSet)
router.register('maintenance_task', views.MaintenanceTaskViewSet)
router.register('maintenance_task_document', views.MaintenanceTaskDocumentViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api/login/', views.login_api),
    path('api/user/', views.get_user_data)
]
