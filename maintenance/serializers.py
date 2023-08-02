from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import MaintenanceDevice, Building, BuildingDetail, MaintenanceArea, MaintenanceAreaDetail, MaintenanceDeviceItem, MaintenanceTask, MaintenanceTaskDocument, User, Project, Process, CheckingWay, ProcessSection, ProcessStep, DeviceDocument, Device
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
                  "username", "password", "date_joined", "device_token","position", "level", "birth_date"]
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


# Building Detail


class ReadBuildingDetailSerializer(ModelSerializer):
    class Meta:
        model = BuildingDetail
        fields = ['id','name','description','building']


class WriteBuildingDetailSerializer(ModelSerializer):
    class Meta:
        model = BuildingDetail
        fields = '__all__'


# Building

class ReadBuildingSerializer(ModelSerializer):

    building_detail_ids = ReadBuildingDetailSerializer(many=True)

    class Meta:
        model = Building
        fields =  ['id','name','description','project','building_detail_ids']

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
        fields = ['id','name','description','area_detail_ids','building_detail']


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
    checking_way = CheckingWaySerializer()
    class Meta:
        model = ProcessStep
        fields = ['id','name','checking_way','section']


class WriteProcessStepSerializer(ModelSerializer):
    class Meta:
        model = ProcessStep
        fields = '__all__'


# Section

class ReadProcessSectionSerializer(ModelSerializer):
    step_ids = ReadProcessStepSerializer(many=True)

    class Meta:
        model = ProcessSection
        fields = ['id','name', 'sequence', 'step_ids', "process"]


class WriteProcessSectionSerializer(ModelSerializer):
    class Meta:
        model = ProcessSection
        fields = '__all__'

# Device Document

class ReadDeviceDocumentSerializer(ModelSerializer):
    path = SerializerMethodField()

    class Meta:
        model = DeviceDocument
        fields = ['id', 'name', 'path', 'device']

    def get_path(self, device_document):
        request = self.context.get('request')
        if request:
            filename = device_document.path.name
            if filename.startswith("static/"):
                path = '/%s' % filename
            else:
                path = '/static/%s' % filename
            return request.build_absolute_uri(path)
        return device_document.path.name

    

class WriteDeviceDocumentSerializer(ModelSerializer):

    class Meta:
        model = DeviceDocument
        fields = '__all__'



# Maintenance Task Document

class MaintenanceTaskDocumentSerializer(ModelSerializer):
    class Meta:
        model = MaintenanceTaskDocument
        fields = ['id', 'name', 'path', 'maintenance_task']

# Device 

class ReadDeviceSerializer(ModelSerializer):
    process = ProcessSerializer()

    class Meta:
        model = Device
        fields = ['id','name','model','code','device_document_ids','process', 'is_part']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['device_document_ids'] = ReadDeviceDocumentSerializer(many=True, context=self.context, instance=instance.device_document_ids.all()).data
        return data



class WriteDeviceSerializer(ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'




# Maintenance Device Item

class ReadMaintenanceDeviceItemSerializer(ModelSerializer):
    members = ReadUserSerializer(many=True)
    device_name = serializers.CharField(source="device.name")
    process_id = serializers.IntegerField(source="device.process.id")
    

    class Meta:
        model = MaintenanceDeviceItem
        fields = ["id","name","description","starting_date","ending_date","device","device_name","process_id","members"]


class WriteMaintenanceDeviceItemSerializer(ModelSerializer):
    class Meta:
        model = MaintenanceDeviceItem
        fields = '__all__'

# Maintenance Device

class ReadMaintenanceDeviceSerializer(ModelSerializer):
    members = ReadUserSerializer(many=True)
    device = WriteDeviceSerializer()
    maintenance_device_item_ids = ReadMaintenanceDeviceItemSerializer(many=True)
    

    class Meta:
        model = MaintenanceDevice
        fields = ["id","name","description","starting_date","ending_date","device","maintenance_area_detail","members","maintenance_device_item_ids"]


class WriteMaintenanceDeviceSerializer(ModelSerializer):
    class Meta:
        model = MaintenanceDevice
        fields = '__all__'

# maintenance task

class ReadMaintenanceTaskSerializer(ModelSerializer):
    employee = ReadUserSerializer()
    maintenance_task_document_ids = MaintenanceTaskDocumentSerializer(many=True)
    class Meta:
        model = MaintenanceTask
        fields = ["id","name","sequence","maintenance_device_item","is_qualified","note","employee","maintenance_task_document_ids"]

class WriteMaintenanceTaskSerializer(ModelSerializer):
    class Meta:
        model = MaintenanceTask
        fields = '__all__'


# Project

class ReadProjectSerializer(ModelSerializer):

    members = ReadUserSerializer(many=True)
    devices = ReadDeviceSerializer(many=True)
    manager = ReadUserSerializer()

    class Meta:
        model = Project
        fields = '__all__'


class WriteProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'