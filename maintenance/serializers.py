from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import MaintenanceDevice, Building, BuildingDetail, MaintenanceArea, MaintenanceAreaDetail, MaintenanceTask, MaintenanceTaskDocument, User, Project, Process, CheckingWay, ProcessSection, ProcessStep, DeviceDocument, Device
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class ReadUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "email"]


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "name", "email",
                  "username", "password", "date_joined", "device_token"]
        extra_kwargs = {
            'password': {'write_only': 'true'}
        }

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

# USER

class ReadProjectSerializer(ModelSerializer):

    members = ReadUserSerializer(many=True)
    manager_id = ReadUserSerializer()

    class Meta:
        model = Project
        fields = '__all__'


class WriteProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

# Building Detail


class ReadBuildingDetailSerializer(ModelSerializer):
    class Meta:
        model = BuildingDetail
        fields = ['id','name','description']


class WriteBuildingDetailSerializer(ModelSerializer):
    class Meta:
        model = BuildingDetail
        fields = '__all__'


# Building

class ReadBuildingSerializer(ModelSerializer):

    building_detail_ids = ReadBuildingDetailSerializer(many=True)

    class Meta:
        model = Building
        fields =  ['id','name','description','project_id','building_detail_ids']

class WriteBuildingSerializer(ModelSerializer):
    class Meta:
        model = Building
        fields = '__all__'


# Maintenance Area Detail

class ReadMaintenanceAreaDetailSerializer(ModelSerializer):
    class Meta:
        model = MaintenanceAreaDetail
        fields = '__all__'

class WriteMaintenanceAreaDetailSerializer(ModelSerializer):
    class Meta:
        model = MaintenanceAreaDetail
        fields = '__all__'

# Maintenance Area

class ReadMaintenanceAreaSerializer(ModelSerializer):
    area_detail_ids = ReadMaintenanceAreaDetailSerializer(many=True)
    class Meta:
        model = MaintenanceArea
        fields = ['id','name','description','area_detail_ids']


class WriteMaintenanceAreaSerializer(ModelSerializer):
    class Meta:
        model = MaintenanceArea
        fields = '__all__'

# Process

class ProcessSerializer(ModelSerializer):
    class Meta:
        model = Process
        fields = '__all__'


# CheckingWay

class CheckingWaySerializer(ModelSerializer):
    class Meta:
        model = CheckingWay
        fields = ['id','name']


# Step

class ReadProcessStepSerializer(ModelSerializer):
    checking_way_id = CheckingWaySerializer()
    class Meta:
        model = ProcessStep
        fields = ['id','name','checking_way_id']


class WriteProcessStepSerializer(ModelSerializer):
    class Meta:
        model = ProcessStep
        fields = '__all__'


# Section

class ReadProcessSectionSerializer(ModelSerializer):
    step_ids = ReadProcessStepSerializer(many=True)

    class Meta:
        model = ProcessSection
        fields = ['id','name', 'sequence', 'step_ids']


class WriteProcessSectionSerializer(ModelSerializer):
    class Meta:
        model = ProcessSection
        fields = '__all__'

# Device Document

class DeviceDocumentSerializer(ModelSerializer):
    class Meta:
        model = DeviceDocument
        fields = ['id', 'name', 'path', 'process_id']

# Maintenance Task Document

class MaintenanceTaskDocumentSerializer(ModelSerializer):
    class Meta:
        model = MaintenanceTaskDocument
        fields = ['id', 'name', 'path', 'maintenance_task_document_id']

# Device 

class ReadDeviceSerializer(ModelSerializer):
    device_document_ids = DeviceDocumentSerializer(many=True)
    process_id = ProcessSerializer()

    class Meta:
        model = Device
        fields = ['id','name','model','code','project_id','device_document_ids','process_id']


class WriteDeviceSerializer(ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'


# Maintenance Device

class ReadMaintenanceDeviceSerializer(ModelSerializer):
    members = ReadUserSerializer(many=True)
    device_name = serializers.CharField(source="device_id.name")
    section_name = serializers.CharField(source="section_id.name")


    class Meta:
        model = MaintenanceDevice
        fields = ["id","name","description","starting_date","ending_date","device_id","device_name","maintenance_area_detail_id","section_id","section_name","members"]


class WriteMaintenanceDeviceSerializer(ModelSerializer):
    class Meta:
        model = MaintenanceDevice
        fields = '__all__'

# maintenance task

class ReadMaintenanceTaskSerializer(ModelSerializer):
    employee_id = ReadUserSerializer()
    maintenance_task_document_ids = MaintenanceTaskDocumentSerializer(many=True)
    class Meta:
        model = MaintenanceTask
        fields = ["id","name","sequence","maintenance_device_id","is_qualified","note","employee_id","maintenance_task_document_ids"]

class WriteMaintenanceTaskSerializer(ModelSerializer):
    class Meta:
        model = MaintenanceTask
        fields = '__all__'

