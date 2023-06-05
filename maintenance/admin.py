from django.contrib import admin
from .models import ( MaintenanceDevice, Building, BuildingDetail, MaintenanceArea, MaintenanceAreaDetail, MaintenanceTask, MaintenanceTaskDocument, 
                     User, Project, Process, CheckingWay, ProcessSection, ProcessStep, DeviceDocument, Device)
from .resources import BuildingResource, ProjectResource, DeviceResource
from import_export.admin import ImportExportModelAdmin

admin.site.register(User)

@admin.register(Project)
class ProjectAdmin(ImportExportModelAdmin):
    list_display = ["name", "code", "starting_date", "ending_date"]
    resource_class= ProjectResource

@admin.register(Building)
class BuildingAdmin(ImportExportModelAdmin):
    list_display = ["name", "description", "project_id"]
    resource_class = BuildingResource

admin.site.register(BuildingDetail)
admin.site.register(MaintenanceArea)
admin.site.register(MaintenanceAreaDetail)
admin.site.register(Process)
admin.site.register(ProcessSection)
admin.site.register(CheckingWay)
admin.site.register(ProcessStep)
admin.site.register(DeviceDocument)

@admin.register(Device)
class DeviceAdmin(ImportExportModelAdmin):
    list_display = ["name","model", "code", "process", "project"]
    resource_class = DeviceResource
    
admin.site.register(MaintenanceDevice)
admin.site.register(MaintenanceTask)
admin.site.register(MaintenanceTaskDocument)
