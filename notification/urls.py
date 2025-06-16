
from django.urls import path
from . import views

urlpatterns = [
    path('notification/', views.NotificationListCreateView.as_view(), name='notification-list-create'),
    path('notification/<int:pk>/', views.NotificationDetailView.as_view(), name='notification-detail'),
]