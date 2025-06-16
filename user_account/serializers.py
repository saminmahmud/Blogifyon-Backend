from os import read
from re import U
import requests
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.conf import settings
from post.serializers import PostSerializer, SavedPostSerializer
from .models import RatingandReview

User = get_user_model()


class RatingandReviewSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    reviewer = serializers.PrimaryKeyRelatedField(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user', write_only=True)
    reviewer_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='reviewer', write_only=True)

    class Meta:
        model = RatingandReview
        fields = ['id', 'user', 'user_id', 'reviewer', 'reviewer_id', 'rating', 'body', 'created_at']
        read_only_fields = ['id', 'user', 'reviewer', 'created_at']

    def to_representation(self, instance):
        request = self.context.get('request')
        rep = super().to_representation(instance)

        def build_profile_data(user):
            return {
                "id": user.id,
                "username": user.username,
                "profile_picture_url": (
                    request.build_absolute_uri(user.profile_picture.url)
                    if user.profile_picture and request else ""
                )
            }

        rep['user'] = build_profile_data(instance.user)
        rep['reviewer'] = build_profile_data(instance.reviewer)
        return rep
    
    def create(self, validated_data):
            user = validated_data.pop('user')
            reviewer = validated_data.pop('reviewer')
            return RatingandReview.objects.create(user=user, reviewer=reviewer, **validated_data)



class UserSerializer(serializers.ModelSerializer):
    total_posts = serializers.SerializerMethodField()
    total_saved_posts = serializers.SerializerMethodField()
    total_review_and_rating = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile_picture', 'bio', 'address', 'twitter', 'facebook', 'linkedin', 'join_date', 'followers', 'following', 'total_posts', 'total_saved_posts', 'total_review_and_rating']

    def get_total_posts(self, obj):
        return obj.total_posts()

    def get_total_saved_posts(self, obj):
        return obj.total_saved_posts()
    
    def get_total_review_and_rating(self, obj):
        return obj.reviews.count()
    
    def get_rating_and_reviews(self, obj):
        reviews = obj.reviews.all()
        request = self.context.get('request')
        return RatingandReviewSerializer(reviews, many=True, context={'request': request}).data


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)
    recaptcha_token = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 'recaptcha_token']


    def validate(self, data):
        # Verify the reCAPTCHA token
        recaptcha_token = data.get('recaptcha_token')
        recaptcha_response = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data={
                'secret': settings.RECAPTCHA_SECRET_KEY,
                'response': recaptcha_token
            }
        )
        recaptcha_result = recaptcha_response.json()
        if not recaptcha_result.get('success'):
            raise serializers.ValidationError("reCAPTCHA validation failed.")

        # check password and confirm password 
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords must match.")
        
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=False,
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required = True)
    password = serializers.CharField(required = True)
    recaptcha_token = serializers.CharField(required=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        recaptcha_token = data.get('recaptcha_token')
        
        # Verify the reCAPTCHA token
        recaptcha_response = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data={
                'secret': settings.RECAPTCHA_SECRET_KEY,
                'response': recaptcha_token
            }
        )
        recaptcha_result = recaptcha_response.json()
        if not recaptcha_result.get('success'):
            raise serializers.ValidationError("reCAPTCHA validation failed.")

        # Authenticate user
        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise serializers.ValidationError("Invalid email or password.")
            if not user.is_active:
                raise serializers.ValidationError("This account is inactive.")
        else:
            raise serializers.ValidationError("Must include 'email' and 'password'.")

        return data
    


class SendEmailSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required = True)
    sender_id = serializers.IntegerField(required = True)
    content = serializers.CharField(max_length=1000)

    def validate(self, data):
        user_id = data.get('user_id')
        sender_id = data.get('sender_id')
        content = data.get('content')

        if user_id == sender_id:
            raise serializers.ValidationError("A user and sender cannot be the same.")
        if not content.strip():
            raise serializers.ValidationError("Content cannot be empty.")
        
        return data