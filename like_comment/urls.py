from django.urls import path
from . import views

urlpatterns = [
    path('like/', views.LikeListView.as_view(), name='like'),
    path('like/<int:pk>/', views.LikeDetailView.as_view(), name='like-detail'),
    
    path('comment/', views.CommentListView.as_view(), name='comment'),
    path('comment/<int:pk>/', views.CommentDetailView.as_view(), name='comment-detail'),

    path('comment-reply/', views.CommentReplyListView.as_view(), name='comment-reply'),
    path('comment-reply/<int:pk>/', views.CommentReplyDetailView.as_view(), name='comment-reply-detail'),
]
