from import_export import resources
from .models import Building, Device, Project, User


class ProjectResource(resources.ModelResource):
    class Meta:
        model = Project


class BuildingResource(resources.ModelResource):


    def after_import_row(self, row, row_result, row_number=None, **kwargs):
        return super().after_import_row(row, row_result, row_number, **kwargs)

    def before_import_row(self, row, row_number=None, **kwargs):
        return super().before_import_row(row, row_number, **kwargs)

    class Meta:
        model = Building
        fields = ('id', 'name', 'description', 'project_id')
        # import_id_fields - TRUONG DUY NHAT
        # exclude - TRUONG BI LOAI BO
        # skip_unchanged - TAT CA CAC TRUONG TRUNG -> LOAI BO
        # report_skipped - KT BAN GHI CO XUAT HIEN TRONG DOI TUONG NHAP

class DeviceResource(resources.ModelResource):
    class Meta:
        model = Device




    
