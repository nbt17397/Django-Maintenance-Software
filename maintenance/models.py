from django.utils.functional import cached_property
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class User(AbstractUser):
    first_name = None
    last_name = None


    name = models.CharField(max_length=150, null=False)
    device_token = models.CharField(max_length=50, null=True)
    is_manager = models.BooleanField(default=True)
    position = models.CharField(max_length=100, null=True)
    level = models.CharField(max_length=100, null=True)
    birth_date = models.DateTimeField(null=True)


class ItemBase(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(max_length=150, null=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name

class CheckingWay(ItemBase):
    class Meta:
        unique_together = ('name',)


class Process(ItemBase):
    class Meta:
        unique_together = ('name',)


class ProcessSection(ItemBase):
    class Meta:
        unique_together = ('name',)
        ordering = ('sequence', )
    
    sequence = models.IntegerField(default=1)
    process = models.ForeignKey(Process, related_name="section_ids", null=False, on_delete=models.CASCADE)

class ProcessStep(ItemBase):
    class Meta:
        unique_together = ('name',)
        ordering = ('sequence', )

    sequence = models.IntegerField(default=1)
    section = models.ForeignKey(ProcessSection, related_name="step_ids", null=False, on_delete=models.CASCADE)
    checking_way = models.ForeignKey(CheckingWay, related_name="step_ids", null=False, on_delete=models.CASCADE)


class DeviceDocument(ItemBase):
    class Meta:
        unique_together = ('name',)

    path = models.FileField(upload_to='documents/path/%Y/%m', null=True)
    device = models.ForeignKey("Device", related_name="device_document_ids",null=True,on_delete=models.SET_NULL)


class Device(ItemBase):
    class Meta:
        unique_together = ('name','model')

    Stock, Ready, Running, Replaced, Removed = range(5)
    STATE = [
        (Stock, 'stock'),
        (Ready, 'ready'),
        (Running, 'running'),
        (Replaced, 'replaced'),
        (Removed, 'removed')
    ]

    model = models.CharField(max_length=50)
    code = models.CharField(max_length=50)
    state = models.PositiveSmallIntegerField(choices=STATE, default=Stock)
    process = models.ForeignKey(Process, related_name="process_ids",null=True,on_delete=models.SET_NULL)
    
class Project(ItemBase):
    class Meta:
        unique_together = ('name',)

    Draft, In_Process, Delayed, Finished = range(4)
    STATE = [
        (Draft, 'Draft'),
        (In_Process, 'In_Process'),
        (Delayed, 'Delayed'),
        (Finished, 'Finished')
    ]

    code = models.CharField(max_length=50)
    state = models.PositiveSmallIntegerField(choices=STATE, default=Draft)
    starting_date = models.DateTimeField(null=True)
    ending_date = models.DateTimeField(null=True)
    manager = models.ForeignKey(
        User, related_name="project_ids", null=True, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name="project_user_rel", blank=True)
    devices = models.ManyToManyField(Device, related_name="project_device_rel", blank=True)

class Building(ItemBase):

    class Meta:
        unique_together = ('name',)

    description = models.TextField()
    project = models.ForeignKey(Project, related_name="building_ids",null=False,on_delete=models.CASCADE)


class BuildingDetail(ItemBase):
    class Meta:
        unique_together = ('name',)

    description = models.TextField()
    building = models.ForeignKey(Building, related_name="building_detail_ids", null=False,on_delete=models.CASCADE)


class MaintenanceArea(ItemBase):

    class Meta:
        unique_together = ('name',)

    description = models.TextField()
    building_detail = models.ForeignKey(BuildingDetail, related_name="area_ids",null=False,on_delete=models.CASCADE)


class MaintenanceAreaDetail(ItemBase):
  
    class Meta:
        unique_together = ('name',)

    description = models.TextField()
    maintenance_area = models.ForeignKey(MaintenanceArea, related_name="area_detail_ids",null=False,on_delete=models.CASCADE)





class MaintenanceDevice(ItemBase):
    class Meta:
        ordering = ('starting_date', )

    Ready, Running, Stopped = range(3)
    STATE = [
        (Ready, 'ready'),
        (Running, 'running'),
        (Stopped, 'stopped')
    ]

    description = models.TextField()
    device = models.ForeignKey(Device, related_name="maintenance_device_ids", null=True, on_delete=models.SET_NULL)
    members = models.ManyToManyField(User, related_name="maintenance_device_user_rel", blank=True)
    starting_date = models.DateTimeField(null=False)
    ending_date = models.DateTimeField(null=False)
    maintenance_area_detail = models.ForeignKey(MaintenanceAreaDetail, related_name="maintenance_device_ids", null=True, on_delete=models.SET_NULL)
    section = models.ForeignKey(ProcessSection, related_name="maintenance_device_ids", null=True, on_delete=models.SET_NULL)
    parent_maintenance_detail = models.ForeignKey('MaintenanceDevice', related_name="children_maintenance_device_ids", null=True, on_delete=models.SET_NULL)
    is_part = models.BooleanField(default=False)

class MaintenanceTask(ItemBase):
    class Meta:
        unique_together = ('name','maintenance_device')
        ordering = ('sequence', )

    
    sequence = models.IntegerField(default=1)
    maintenance_device = models.ForeignKey(MaintenanceDevice, related_name="maintenance_task_ids",null=True,on_delete=models.SET_NULL)
    is_qualified = models.BooleanField(default=False)
    note = models.TextField(null=True)
    starting_date = models.DateTimeField(null=True)
    ending_date = models.DateTimeField(null=True)
    employee = models.ForeignKey(User, related_name="maintenance_task_ids",null=True,on_delete=models.SET_NULL)
    step = models.ForeignKey(ProcessStep, related_name="maintenance_task_ids",null=True,on_delete=models.SET_NULL)
    checking_way = models.ForeignKey(CheckingWay, related_name="maintenance_task_ids",null=True,on_delete=models.SET_NULL)


class MaintenanceTaskDocument(ItemBase):
    class Meta:
        unique_together = ('name',)

    path = models.FileField(upload_to='documents/path/%Y/%m', null=True)
    maintenance_task_document = models.ForeignKey(MaintenanceTask, related_name="maintenance_task_document_ids",null=True,on_delete=models.SET_NULL)


    





