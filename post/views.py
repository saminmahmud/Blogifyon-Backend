from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import default_storage
from django.conf import settings
from .models import Post, SavedPost, Category
from rest_framework.response import Response
from rest_framework import status
from .serializers import PostSerializer, CategorySerializer, SavedPostSerializer, TopPostSerializer
import os


class PostListView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'categories__name']
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [] 
        return [permissions.IsAuthenticated()]
    
    def perform_create(self, serializer):
        user = self.request.user
        print("User creating post:", user, "Authenticated:", user.is_authenticated)
        serializer.save(user=user)

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [] 
        return [permissions.IsAuthenticated()]


class PostListForUserView(generics.ListAPIView):
    serializer_class = PostSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    ordering_fields = ['created_at']
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [] 
        return [permissions.IsAuthenticated()]
    
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return Post.objects.filter(user__id=user_id)


class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']
    pagination_class = None 

    def get_permissions(self):
        if self.request.method == 'GET':
            return [] 
        return [permissions.IsAuthenticated()]
    

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [] 
        return [permissions.IsAuthenticated()]
    

class SavedPostListView(generics.ListCreateAPIView):
    queryset = SavedPost.objects.all()
    serializer_class = SavedPostSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['user__id']
    ordering_fields = ['created_at']

    def get_permissions(self):
        if self.request.method == 'GET':
            return [] 
        return [permissions.IsAuthenticated()]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    
class SavedPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SavedPost.objects.all()
    serializer_class = SavedPostSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [] 
        return [permissions.IsAuthenticated()]
    
    def get_queryset(self):
        return SavedPost.objects.filter(user=self.request.user)

    
class TopPostView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        posts = Post.objects.all()
        sorted_posts = sorted(
            posts,
            key=lambda post: len(post.total_likes()) + post.total_comments(),
            reverse=True
        )
        top_five = sorted_posts[:5]
        serializer = TopPostSerializer(top_five, many=True, context={'request': request})
        return Response(serializer.data)


class ImageUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.AllowAny]  # ✅ THIS LINE FIXES 403

    def post(self, request):
        
        image = request.FILES.get('upload')

        if not image:
            return Response({'uploaded': False, 'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        save_path = os.path.join('post_body_images', image.name)
        filename = default_storage.save(save_path, image)
        image_url = request.build_absolute_uri(settings.MEDIA_URL + filename)

        return Response({
            'uploaded': True,
            'url': image_url
        }, status=status.HTTP_201_CREATED)