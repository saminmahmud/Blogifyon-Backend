from django.urls import path
from post import views

urlpatterns = [
    path('post/', views.PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('category/', views.CategoryListView.as_view(), name='category-list'),
    path('category/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('saved-post/', views.SavedPostListView.as_view(), name='saved-posts'),    
    path('saved-post/<int:pk>/', views.SavedPostDetailView.as_view(), name='saved-post-detail'),
    path('top-post/', views.TopPostView.as_view(), name='top-posts'),
    path('user-post/<int:user_id>/', views.PostListForUserView.as_view(), name='user-posts'),
    path('upload-image/', views.ImageUploadView.as_view(), name='ckeditor-upload'),
]
