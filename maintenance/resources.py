from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Building, Device, Project, User, Process



class ProjectResource(resources.ModelResource):
    class Meta:
        model = Project
        fields = ('id', 'name', 'code', 'starting_date', 'ending_date')



class BuildingResource(resources.ModelResource):

    project = fields.Field(column_name='project',attribute='project', widget=ForeignKeyWidget(Project, field='code'))

    def before_import_row(self, row, row_number=None, **kwargs):
        if row["project"]:
            project_code = row["project"]
            Project.objects.get_or_create(name=project_code, code = project_code, defaults={"name": project_code, "code": project_code})
            

    class Meta:
        model = Building
        fields = ('id', 'name', 'description', 'project')
        # import_id_fields - TRUONG DUY NHAT
        # exclude - TRUONG BI LOAI BO
        # skip_unchanged - TAT CA CAC TRUONG TRUNG -> LOAI BO
        # report_skipped - KT BAN GHI CO XUAT HIEN TRONG DOI TUONG NHAP

class DeviceResource(resources.ModelResource):

    # project = fields.Field(column_name='project',attribute='project', widget=ForeignKeyWidget(Project, field='code'))
    process = fields.Field(column_name='process',attribute='process', widget=ForeignKeyWidget(Process, field='process'))

    def before_import_row(self, row, row_number=None, **kwargs):
        # if row["project"]:
        #     project_code = row["project"]
        #     Project.objects.get_or_create(name=project_code, code=project_code, defaults={"name": project_code, "code": project_code})

        if row["process"]:
            process_name = row["process"]
            Process.objects.get_or_create(name=process_name, defaults={"name": process_name})


    class Meta:
        model = Device
        fields = ('id', 'name', 'model', 'code', 'process' )

    




    
