from django.utils.functional import cached_property
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class User(AbstractUser):

    name = models.CharField(max_length=150, null=False)
    device_token = models.CharField(max_length=50, null=True)


class ItemBase(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(max_length=150, null=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name


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
    starting_date = models.DateTimeField(null=False)
    ending_date = models.DateTimeField(null=False)
    manager_id = models.ForeignKey(
        User, related_name="project_ids", null=False, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name="project_user_rel")

class Building(ItemBase):

    class Meta:
        unique_together = ('name',)

    description = models.TextField()
    project_id = models.ForeignKey(Project, related_name="building_ids",null=False,on_delete=models.CASCADE)


class BuildingDetail(ItemBase):
    class Meta:
        unique_together = ('name',)

    description = models.TextField()
    building_id = models.ForeignKey(Building, related_name="building_detail_ids", null=False,on_delete=models.CASCADE)


class MaintenanceArea(ItemBase):

    class Meta:
        unique_together = ('name',)

    description = models.TextField()
    building_detail_id = models.ForeignKey(BuildingDetail, related_name="area_ids",null=False,on_delete=models.CASCADE)


class MaintenanceAreaDetail(ItemBase):
  
    class Meta:
        unique_together = ('name',)

    description = models.TextField()
    maintenance_area_id = models.ForeignKey(MaintenanceArea, related_name="area_detail_ids",null=False,on_delete=models.CASCADE)


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
    process_id = models.ForeignKey(Process, related_name="section_ids", null=False, on_delete=models.CASCADE)

class ProcessStep(ItemBase):
    class Meta:
        unique_together = ('name',)
        ordering = ('sequence', )

    sequence = models.IntegerField(default=1)
    section_id = models.ForeignKey(ProcessSection, related_name="step_ids", null=False, on_delete=models.CASCADE)
    checking_way_id = models.ForeignKey(CheckingWay, related_name="step_ids", null=False, on_delete=models.CASCADE)


class DeviceDocument(ItemBase):
    class Meta:
        unique_together = ('name',)

    path = models.FileField(upload_to='uploads/path/%Y/%m', null=True)
    process_id = models.ForeignKey("Device", related_name="device_document_ids",null=True,on_delete=models.SET_NULL)


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
    project_id = models.ForeignKey(Project, related_name="device_ids",null=False,on_delete=models.CASCADE)
    process_id = models.ForeignKey(Process, related_name="process_ids",null=True,on_delete=models.SET_NULL) #warning related_name



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
    device_id = models.ForeignKey(Device, related_name="maintenance_device_ids", null=True, on_delete=models.SET_NULL)
    members = models.ManyToManyField(User, related_name="maintenance_device_user_rel")
    starting_date = models.DateTimeField(null=False)
    ending_date = models.DateTimeField(null=False)
    maintenance_area_detail_id = models.ForeignKey(MaintenanceAreaDetail, related_name="maintenance_device_ids", null=True, on_delete=models.SET_NULL)
    section_id = models.ForeignKey(ProcessSection, related_name="maintenance_device_ids", null=True, on_delete=models.SET_NULL)


class MaintenanceTask(ItemBase):
    class Meta:
        ordering = ('sequence', )

    
    sequence = models.IntegerField(default=1)
    maintenance_device_id = models.ForeignKey(MaintenanceDevice, related_name="maintenance_task_ids",null=True,on_delete=models.SET_NULL)
    is_qualified = models.BooleanField(default=False)
    note = models.TextField(null=True)
    starting_date = models.DateTimeField(null=False)
    ending_date = models.DateTimeField(null=False)
    employee_id = models.ForeignKey(User, related_name="maintenance_task_ids",null=True,on_delete=models.SET_NULL)
    step_id = models.ForeignKey(ProcessStep, related_name="maintenance_task_ids",null=True,on_delete=models.SET_NULL)
    checking_way_id = models.ForeignKey(CheckingWay, related_name="maintenance_task_ids",null=True,on_delete=models.SET_NULL)


class MaintenanceTaskDocument(ItemBase):
    class Meta:
        unique_together = ('name',)

    path = models.FileField(upload_to='uploads/path/%Y/%m', null=True)
    maintenance_task_document_id = models.ForeignKey(MaintenanceTask, related_name="maintenance_task_document_ids",null=True,on_delete=models.SET_NULL)


    





