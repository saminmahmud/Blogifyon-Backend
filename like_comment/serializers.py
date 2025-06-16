from os import read
from rest_framework import serializers
from .models import Like, Comment, CommentReply, User


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"


class CommentReplySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user', write_only=True)
    children = serializers.SerializerMethodField()

    class Meta:
        model = CommentReply
        fields = "__all__"
        read_only_fields = ['created_at', 'updated_at', 'user', 'children']

    def get_user(self, obj):
        request = self.context.get('request')
        
        profile_picture = None
        if obj.user.profile_picture and hasattr(obj.user.profile_picture, 'url'):
            profile_picture = request.build_absolute_uri(obj.user.profile_picture.url)

        return {
            'id': obj.user.id,
            'username': obj.user.username,
            'profile_picture': profile_picture
        }
    
    def get_children(self, obj):
        return CommentReplySerializer(obj.children.all(), many=True, context=self.context).data
    
    def create(self, validated_data):
        user = validated_data.pop('user')
        return CommentReply.objects.create(user=user, **validated_data)
    

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user', write_only=True)
    replies = CommentReplySerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ['created_at', 'updated_at', 'user']
    
    def get_user(self, obj):
        request = self.context.get('request')
        
        profile_picture = None
        if obj.user.profile_picture and hasattr(obj.user.profile_picture, 'url'):
            profile_picture = request.build_absolute_uri(obj.user.profile_picture.url)

        return {
            'id': obj.user.id,
            'username': obj.user.username,
            'profile_picture': profile_picture
        }
    
    def create(self, validated_data):
        user = validated_data.pop('user')
        return Comment.objects.create(user=user, **validated_data)
    
