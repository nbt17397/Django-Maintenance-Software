from rest_framework import viewsets, permissions, status, generics
from .permissions import ( IsUserManager )
from .serializers import ( ReadDeviceDocumentSerializer, WriteDeviceDocumentSerializer, MaintenanceTaskDocumentSerializer, ReadMaintenanceAreaDetailSerializer, ReadMaintenanceDeviceSerializer, ReadMaintenanceTaskSerializer, ReadProcessStepSerializer, WriteMaintenanceAreaDetailSerializer, ReadMaintenanceAreaSerializer, 
                          WriteMaintenanceAreaSerializer, ReadBuildingDetailSerializer, ReadBuildingSerializer, UserSerializer, ReadProjectSerializer, 
                          WriteBuildingSerializer, WriteMaintenanceDeviceSerializer, WriteMaintenanceTaskSerializer, WriteProcessStepSerializer, WriteProjectSerializer, WriteBuildingDetailSerializer, ProcessSerializer, CheckingWaySerializer, 
                          ReadProcessSectionSerializer, WriteProcessSectionSerializer, ReadDeviceSerializer, WriteDeviceSerializer)
from .models import ( Building, BuildingDetail, MaintenanceArea, MaintenanceAreaDetail, MaintenanceDevice, MaintenanceTask, MaintenanceTaskDocument, User, Project, Process, CheckingWay, ProcessSection, ProcessStep, Device, DeviceDocument)
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken
from .paginator import LargeResultsSetPagination, StandardResultsSetPagination
from datetime import datetime




@api_view(['POST'])
def login_api(request):
    permission_classes = [permissions.AllowAny]
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']

    user.auth_token_set.all().delete()
    _, token = AuthToken.objects.create(user)

    device_token = request.data.get('device_token')
    if device_token is not None:
        user.device_token = device_token
        user.save()
    return Response({
        'user_info': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'device_token': user.device_token,
            'name': user.name,
            'is_manager': user.is_manager,
            'is_superuser': user.is_superuser,
        },
        'token': token
    })


@api_view(['GET'])
def get_user_data(request):
    user = request.user

    if user is not None:
        return Response(data={'user_info': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }})
    return Response(data={'error': 'not authenticated'}, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView, generics.UpdateAPIView, generics.RetrieveAPIView, generics.DestroyAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser]
    permission_classes = [permissions.IsAuthenticated]



    def list(self, request):
        users = User.objects.filter(is_active=True)

        serializer = UserSerializer(users, many=True)
        return Response(data={"users": serializer.data}, status=status.HTTP_200_OK)
    
    @action(methods=['get'], detail=True, url_path='get_task_by_user')
    def get_task_by_user(self, request, pk):
        maintenance_tasks= self.get_object().maintenance_task_ids.filter(active=True)

        serializer = ReadMaintenanceTaskSerializer(maintenance_tasks, many=True)
        return Response(data={"maintenance_tasks": serializer.data}, status=status.HTTP_200_OK)
    
    @action(methods=['get'], detail=True, url_path='get_project_by_user')
    def get_project_by_user(self, request, pk):
        projects= self.get_object().project_user_rel.filter(active=True)

        serializer = ReadProjectSerializer(projects, many=True)
        return Response(data={"projects": serializer.data}, status=status.HTTP_200_OK)
    
    @action(methods=['get'], detail=True, url_path='get_maintenance_device_by_user')
    def get_maintenance_device_by_user(self, request, pk):
        projects= self.get_object().maintenance_device_user_rel.filter(active=True)

        serializer = ReadMaintenanceDeviceSerializer(projects, many=True)
        return Response(data={"projects": serializer.data}, status=status.HTTP_200_OK)
    

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.filter(active=True)
    permission_classes = [permissions.IsAuthenticated, IsUserManager]

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return WriteProjectSerializer

        return ReadProjectSerializer
    
    @action(methods=['get'], detail=True, url_path='get_building_by_project')
    def get_building_by_project(self, request, pk):
        buildings= self.get_object().building_ids.filter(active=True)
        
        serializer = ReadBuildingSerializer(buildings, many=True)
        return Response(data={"buildings": serializer.data}, status=status.HTTP_200_OK)
  
    
    

class BuildingViewSet(viewsets.ModelViewSet):
    queryset = Building.objects.filter(active=True)
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return WriteBuildingSerializer

        return ReadBuildingSerializer


class BuildingDetailViewSet(viewsets.ModelViewSet):
    queryset = BuildingDetail.objects.filter(active=True)
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return WriteBuildingDetailSerializer

        return ReadBuildingDetailSerializer


class MaintenanceAreaViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceArea.objects.filter(active=True)
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return WriteMaintenanceAreaSerializer

        return ReadMaintenanceAreaSerializer


class MaintenanceAreaDetailViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceAreaDetail.objects.filter(active=True)
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return WriteMaintenanceAreaDetailSerializer

        return ReadMaintenanceAreaDetailSerializer
    

class ProcessViewSet(viewsets.ModelViewSet):
    queryset = Process.objects.filter(active=True)
    serializer_class = ProcessSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['get'], detail=True, url_path='get_section_by_process')
    def get_section_by_process(self, request, pk):
        sections= self.get_object().section_ids.filter(active=True)

        serializer = ReadProcessSectionSerializer(sections, many=True)
        return Response(data={"sections": serializer.data}, status=status.HTTP_200_OK)


class CheckingWayViewSet(viewsets.ModelViewSet):
    queryset = CheckingWay.objects.filter(active=True)
    serializer_class = CheckingWaySerializer
    permission_classes = [permissions.IsAuthenticated]


class ProcessSectionViewSet(viewsets.ModelViewSet):
    queryset = ProcessSection.objects.filter(active=True)
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return WriteProcessSectionSerializer

        return ReadProcessSectionSerializer
    
    @action(methods=['get'], detail=True, url_path='get_step_by_section')
    def get_step_by_section(self, request, pk):
        steps= self.get_object().step_ids.filter(active=True)

        serializer = ReadProcessStepSerializer(steps, many=True)
        return Response(data={"steps": serializer.data}, status=status.HTTP_200_OK)


class ProcessStepViewSet(viewsets.ModelViewSet):
    queryset = ProcessStep.objects.filter(active=True)
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return WriteProcessStepSerializer

        return ReadProcessStepSerializer
    

class DeviceDocumentViewSet(viewsets.ModelViewSet):
    queryset = DeviceDocument.objects.filter(active=True)
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return WriteDeviceDocumentSerializer

        return ReadDeviceDocumentSerializer



class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.filter(active=True)
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return WriteDeviceSerializer

        return ReadDeviceSerializer
    

class MaintenanceDeviceViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceDevice.objects.filter(active=True)
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return WriteMaintenanceDeviceSerializer

        return ReadMaintenanceDeviceSerializer
    

class MaintenanceTaskDocumentViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceTaskDocument.objects.filter(active=True)
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return MaintenanceTaskDocumentSerializer

        return MaintenanceTaskDocumentSerializer
    

class MaintenanceTaskViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceTask.objects.filter(active=True)
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return WriteMaintenanceTaskSerializer

        return ReadMaintenanceTaskSerializer
