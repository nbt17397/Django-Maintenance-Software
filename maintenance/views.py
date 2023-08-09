from rest_framework import viewsets, permissions, status, generics
from .permissions import ( IsUserManager, IsSuperUser )
from .serializers import ( ReadDeviceDocumentSerializer, ReadMaintenanceDeviceItemSerializer, ReadMaintenanceTaskDocumentSerializer, ReadProcessSerializer, WriteDeviceDocumentSerializer, ReadMaintenanceAreaDetailSerializer, ReadMaintenanceDeviceSerializer, ReadMaintenanceTaskSerializer, ReadProcessStepSerializer, WriteMaintenanceAreaDetailSerializer, ReadMaintenanceAreaSerializer, 
                          WriteMaintenanceAreaSerializer, UserSerializer, ReadProjectSerializer, 
                           WriteMaintenanceDeviceItemSerializer, WriteMaintenanceDeviceSerializer, WriteMaintenanceTaskDocumentSerializer, WriteMaintenanceTaskSerializer, WriteProcessSerializer, WriteProcessStepSerializer, WriteProjectSerializer, CheckingWaySerializer, 
                          ReadProcessSectionSerializer, WriteProcessSectionSerializer, ReadDeviceSerializer, WriteDeviceSerializer)
from .models import ( MaintenanceArea, MaintenanceAreaDetail, MaintenanceDevice, MaintenanceDeviceItem, MaintenanceTask, MaintenanceTaskDocument, User, Project, Process, CheckingWay, ProcessSection, ProcessStep, Device, DeviceDocument)
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
    # parser_classes = [MultiPartParser]
    permission_classes = [permissions.IsAuthenticated]



    def list(self, request):
        users = User.objects.filter(is_active=True)

        serializer = UserSerializer(users, many=True)
        return Response(data={"users": serializer.data}, status=status.HTTP_200_OK)
    
    @action(methods=['get'], detail=True, url_path='get-task-by-user')
    def get_task_by_user(self, request, pk):
        maintenance_tasks= self.get_object().maintenance_task_ids.filter(active=True)

        serializer = ReadMaintenanceTaskSerializer(maintenance_tasks, many=True)
        return Response(data={"maintenance_tasks": serializer.data}, status=status.HTTP_200_OK)
    
    @action(methods=['get'], detail=True, url_path='get-project-by-user')
    def get_project_by_user(self, request, pk):
        projects= self.get_object().project_user_rel.filter(active=True)

        serializer = WriteProjectSerializer(projects, many=True)
        return Response(data={"projects": serializer.data}, status=status.HTTP_200_OK)
    
    @action(methods=['get'], detail=True, url_path='get-maintenance-device-by-user')
    def get_maintenance_device_by_user(self, request, pk):
        projects= self.get_object().maintenance_device_user_rel.filter(active=True)

        serializer = ReadMaintenanceDeviceSerializer(projects, many=True)
        return Response(data={"projects": serializer.data}, status=status.HTTP_200_OK)
    

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.filter(active=True)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, IsSuperUser]
        elif self.action in ['list']:
            permission_classes = [permissions.IsAuthenticated, IsUserManager]
        else:
            permission_classes = [permissions.AllowAny]

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return WriteProjectSerializer

        return ReadProjectSerializer
    
    @action(methods=['get'], detail=True, url_path='get-areas')
    def get_areas(self, request, pk):
        areas= self.get_object().area_ids.filter(active=True)
        
        serializer = ReadMaintenanceAreaSerializer(areas, many=True)
        return Response(data={"results": serializer.data}, status=status.HTTP_200_OK)
    
    
    

# class BuildingViewSet(viewsets.ModelViewSet):
#     queryset = Building.objects.filter(active=True)
#     permission_classes = [permissions.IsAuthenticated]

#     def get_permissions(self):
#         if self.action in ('create', 'update', 'partial_update', 'destroy'):
#             permission_classes = [permissions.IsAuthenticated, IsSuperUser]
#         elif self.action == 'list':
#             permission_classes = [permissions.IsAuthenticated, IsUserManager]
#         else:
#             permission_classes = [permissions.AllowAny]
#         return [permission() for permission in permission_classes]

#     def get_serializer_class(self):
#         if self.action in ('create', 'update', 'partial_update', 'destroy'):
#             return WriteBuildingSerializer

#         return ReadBuildingSerializer


# class BuildingDetailViewSet(viewsets.ModelViewSet):
#     queryset = BuildingDetail.objects.filter(active=True)
#     permission_classes = [permissions.IsAuthenticated]

#     def get_serializer_class(self):
#         if self.action in ('create', 'update', 'partial_update', 'destroy'):
#             return WriteBuildingDetailSerializer

#         return ReadBuildingDetailSerializer
    
#     @action(methods=['get'], detail=True, url_path='get-maintenance-area')
#     def get_maintenance_area(self, request, pk):
#         maintenance_area= self.get_object().area_ids.filter(active=True)
        
#         serializer = ReadMaintenanceAreaSerializer(maintenance_area, many=True)
#         return Response(data={"results": serializer.data}, status=status.HTTP_200_OK)


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
    
    @action(methods=['get'], detail=True, url_path='get-maintenance-device')
    def get_maintenance_device(self, request, pk):
        maintenance_devices= self.get_object().maintenance_device_ids.filter(active=True)
        
        serializer = ReadMaintenanceDeviceSerializer(maintenance_devices, many=True)
        return Response(data={"results": serializer.data}, status=status.HTTP_200_OK)
    

class ProcessViewSet(viewsets.ModelViewSet):
    queryset = Process.objects.filter(active=True)
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return WriteProcessSerializer

        return ReadProcessSerializer

    @action(methods=['get'], detail=True, url_path='get-section-by-process')
    def get_section_by_process(self, request, pk):
        sections= self.get_object().section_ids.filter(active=True)
        context = {'request': request}
        serializer = ReadProcessSectionSerializer(sections, context=context, many=True)
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
    
    @action(methods=['get'], detail=True, url_path='get-step-by-section')
    def get_step_by_section(self, request, pk):
        steps= self.get_object().step_ids.filter(active=True)

        serializer = ReadProcessStepSerializer(steps, many=True)
        return Response(data={"steps": serializer.data}, status=status.HTTP_200_OK)
    
    @action(methods=['post'], detail=True, url_path='generate-maintenance-tasks')
    def generate_maintenance_tasks(self, request, pk):
        try:
            steps = self.get_object().step_ids.filter(active=True)

            maintenance_device_id = request.data.get('maintenance_device_id')

            if steps.exists() and maintenance_device_id:
                [MaintenanceTask.objects.create(name=step.name, sequence=step.sequence, maintenance_device_id=maintenance_device_id, step=step, checking_way=step.checking_way) for step in steps]
                return Response(data={"result": "Generated steps successfully"}, status=status.HTTP_200_OK)
            else:
                return Response(data={"result": "Step or maintenance device is empty"}, status=status.HTTP_400_BAD_REQUEST) 
            
        except Exception  as e:
            return Response(data={"result": str(e)}, status=status.HTTP_400_BAD_REQUEST)



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
    

    def list(self, request):
        devices = Device.objects.filter(active=True)
        is_part = request.query_params.get('is_part')
        if is_part is not None:
            devices = devices.filter(is_part=is_part)
        context = {'request': request}
        serializer = ReadDeviceSerializer(devices, context=context, many=True)
        return Response(data={"results": serializer.data}, status=status.HTTP_200_OK)
    

    @action(methods=['get'], detail=True, url_path='get-project-by-device')
    def get_project_by_device(self, request, pk):
        projects= self.get_object().project_device_rel.filter(active=True)

        serializer = WriteProjectSerializer(projects, many=True)
        return Response(data={"projects": serializer.data}, status=status.HTTP_200_OK)
    

    @action(methods=['get'], detail=True, url_path='get-documents')
    def get_documents(self, request, pk):
        documents= self.get_object().device_document_ids.filter(active=True)
        context = {'request': request}
        serializer = ReadDeviceDocumentSerializer(documents,context=context, many=True)
        return Response(data={"results": serializer.data}, status=status.HTTP_200_OK)
    
    
    

class MaintenanceDeviceViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceDevice.objects.filter(active=True)
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return WriteMaintenanceDeviceSerializer

        return ReadMaintenanceDeviceSerializer
    
    @action(methods=['get'], detail=True, url_path='get-maintenance-device-items')
    def get_maintenance_device_items(self, request, pk):
        items= self.get_object().maintenance_device_item_ids.filter(active=True)
        context = {'request': request}
        serializer = ReadMaintenanceDeviceItemSerializer(items, context=context, many=True)
        return Response(data={"results": serializer.data}, status=status.HTTP_200_OK)
    

class MaintenanceDeviceItemViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceDeviceItem.objects.filter(active=True)
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return WriteMaintenanceDeviceItemSerializer

        return ReadMaintenanceDeviceItemSerializer
    
    @action(methods=['get'], detail=True, url_path='get-maintenance-tasks')
    def get_maintenance_tasks(self, request, pk):
        items= self.get_object().maintenance_task_ids.filter(active=True)
        context = {'request': request}
        serializer = ReadMaintenanceTaskSerializer(items, context=context, many=True)
        return Response(data={"results": serializer.data}, status=status.HTTP_200_OK)

class MaintenanceTaskDocumentViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceTaskDocument.objects.filter(active=True)
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return WriteMaintenanceTaskDocumentSerializer

        return ReadMaintenanceTaskDocumentSerializer
    

class MaintenanceTaskViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceTask.objects.filter(active=True)
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return WriteMaintenanceTaskSerializer

        return ReadMaintenanceTaskSerializer
