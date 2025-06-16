from django.shortcuts import render
from rest_framework.filters import SearchFilter
from .models import Like, Comment, CommentReply
from .serializers import LikeSerializer, CommentSerializer, CommentReplySerializer
from rest_framework import generics, permissions, serializers
from rest_framework.response import Response
from rest_framework import status

class LikeListView(generics.ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    filter_backends = [SearchFilter]
    search_fields = ['post__id']
    pagination_class = None

    def get_permissions(self):
        if self.request.method == 'GET':
            return [] 
        return [permissions.IsAuthenticated()]
    

class LikeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [] 
        return [permissions.IsAuthenticated()]
    

class CommentListView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [SearchFilter]
    search_fields = ['post__id']
    pagination_class = None

    def get_permissions(self):
        if self.request.method == 'GET':
            return [] 
        return [permissions.IsAuthenticated()]


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [] 
        return [permissions.IsAuthenticated()]


class CommentReplyListView(generics.ListCreateAPIView):
    queryset = CommentReply.objects.all()
    serializer_class = CommentReplySerializer
    filter_backends = [SearchFilter]
    search_fields = ['comment__id']
    pagination_class = None

    def get_permissions(self):
        if self.request.method == 'GET':
            return [] 
        return [permissions.IsAuthenticated()]


class CommentReplyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CommentReply.objects.all()
    serializer_class = CommentReplySerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [] 
        return [permissions.IsAuthenticated()]







