from django.shortcuts import render
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework import generics, permissions
from rest_framework.filters import SearchFilter


class NotificationListCreateView(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    filter_backends = [SearchFilter]
    search_fields = ['user__id']
    pagination_class = None

    def get_permissions(self):
        if self.request.method == 'GET':
            return [] 
        return [permissions.IsAuthenticated()]
    

class NotificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [] 
        return [permissions.IsAuthenticated()]