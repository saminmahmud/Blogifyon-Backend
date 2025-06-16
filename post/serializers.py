from os import read
from django.contrib.gis.gdal.raster import source
from rest_framework import serializers
from .models import Post, Category, SavedPost

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class RelatedPostSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'post_image_url', 'created_at', 'user']

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


class PostSerializer(serializers.ModelSerializer):
    total_likes = serializers.SerializerMethodField()
    total_comments = serializers.SerializerMethodField()
    related_posts = serializers.SerializerMethodField()
    categories = CategorySerializer(many=True, read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        many=True,
        write_only=True,
        required=True
    )
    user = serializers.SerializerMethodField()
    total_saved = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['total_likes', 'total_comments', 'total_saved', 'user', 'related_posts']

    def get_total_likes(self, obj):
        return obj.total_likes()

    def get_total_comments(self, obj):
        return obj.total_comments()
    
    def get_total_saved(self, obj):
        return obj.total_saved()

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
        category_ids = validated_data.pop('category_ids', [])
        post = Post.objects.create(**validated_data)
        post.categories.set(category_ids)
        return post
    
    def get_related_posts(self, obj):
        related_posts = (
            Post.objects
            .filter(categories__in=obj.categories.all())
            .exclude(id=obj.id)
            .distinct()[:2]
        )
        return RelatedPostSerializer(related_posts, many=True, context=self.context).data
    

class SavedPostSerializer(serializers.ModelSerializer):
    post = PostSerializer(read_only=True)
    post_id = serializers.PrimaryKeyRelatedField(
        queryset=Post.objects.all(),
        write_only=True,
        source='post'
    )

    class Meta:
        model = SavedPost
        fields = ['id', 'user', 'post', 'post_id', 'created_at']
        read_only_fields = ['id', 'user', 'post', 'created_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return SavedPost.objects.create(**validated_data)


class TopPostSerializer(serializers.ModelSerializer):
    score = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    post_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['score']

    def get_score(self, obj):
        return len(obj.total_likes()) + obj.total_comments()
    
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
    
    def get_post_image_url(self, obj):
        request = self.context.get('request')
        if obj.post_image_url and hasattr(obj.post_image_url, 'url'):
            return request.build_absolute_uri(obj.post_image_url.url)
        return None

