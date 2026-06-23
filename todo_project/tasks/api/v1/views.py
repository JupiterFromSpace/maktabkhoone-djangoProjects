from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TaskSerializer
from ...models import Task
from tasks.tasks import fetch_weather



class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
        

class WeatherView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = cache.get('weather_data')
        if not data:
            data = fetch_weather()
        if not data:
            return Response({'error': 'اطلاعات آب و هوا در دسترس نیست.'}, status=503)
        return Response(data)