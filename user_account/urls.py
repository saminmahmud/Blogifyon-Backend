from django.urls import path
from . import views

urlpatterns = [
    path('user/', views.UserListView.as_view(), name='user-list'),
    path('user/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    path('user/register/', views.UserRegistrationApiView.as_view(), name='user-register'),
    path('user/activate/<uid>/<token>/', views.activate, name='activate'),
    path('user/login/', views.UserLoginApiView.as_view(), name='user-login'),
    path('user/logout/', views.UserLogoutApiView.as_view(), name='user-logout'),
    path('user/review/', views.UserRatingandReviewListView.as_view(), name='review-list'),
    path('user/review/<int:pk>/', views.UserRatingandReviewDetailView.as_view(), name='review-detail'),
    path('send_email/', views.SendEmailView.as_view(), name='send-email'),
]