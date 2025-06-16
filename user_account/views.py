from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives, send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.authtoken.models import Token
from rest_framework.filters import SearchFilter
from django.utils.encoding import force_bytes
from rest_framework.views import APIView

from .models import RatingandReview
from .serializers import SendEmailSerializer, UserSerializer, UserRegistrationSerializer, UserLoginSerializer, RatingandReviewSerializer
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()

frontend_url = settings.FRONTEND_URL 
backend_url = settings.BACKEND_URL

class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [SearchFilter]
    search_fields = ['username', 'email']
    pagination_class = None

    def get_permissions(self):
        if self.request.method == 'GET':
            return [] 
        return [permissions.IsAuthenticated()]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [] 
        return [permissions.IsAuthenticated()]


class UserRegistrationApiView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    authentication_classes = [] 
    permission_classes = []

    def perform_create(self, serializer):
        user = serializer.save()
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        confirm_link = f'{backend_url}/user/activate/{uid}/{token}'

        email_subject = 'Confirm Your Email'
        email_body = render_to_string('confirm_email.html', {'confirm_link': confirm_link, 'frontend_url': frontend_url})
        email = EmailMultiAlternatives(email_subject, '', to=[user.email])
        email.attach_alternative(email_body, 'text/html')
        email.send()


def activate(request, uid, token):
    try:
        uid = urlsafe_base64_decode(uid).decode()
        user = User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user = None 
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponseRedirect(f'{frontend_url}/login?status=success')
    else:
        return HttpResponseRedirect(f'{frontend_url}/register?status=failed')
    


class UserLoginApiView(APIView):
    authentication_classes = []  
    permission_classes = []
    
    def post(self, request):
        serializer = UserLoginSerializer(data = self.request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(email= email, password=password)
            
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                # print(token)
                # print(_)
                login(request, user)
                userId = User.objects.filter(id=user.id).first().id

                return Response({'token' : token.key, 'user_id' : userId}, status=status.HTTP_200_OK)
            else:
                return Response({'error' : "Invalid Credential"}, status.HTTP_406_NOT_ACCEPTABLE)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserLogoutApiView(APIView):
    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        if token:
            token = token.replace('Token ', '')
            try:
                token_obj = Token.objects.get(key=token)
                token_obj.delete()
            except Token.DoesNotExist:
                pass 

        logout(request)
        return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)


class UserRatingandReviewListView(generics.ListCreateAPIView):
    queryset = RatingandReview.objects.all()
    serializer_class = RatingandReviewSerializer
    filter_backends = [SearchFilter]
    search_fields = ['user__id']
    pagination_class = None 

    def get_permissions(self):
        if self.request.method == 'GET':
            return [] 
        return [permissions.IsAuthenticated()]
    

class UserRatingandReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RatingandReview.objects.all()
    serializer_class = RatingandReviewSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [] 
        return [permissions.IsAuthenticated()]


class SendEmailView(APIView):
    def post(self, request):
        serializer = SendEmailSerializer(data = self.request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            sender_id = serializer.validated_data['sender_id']
            content = serializer.validated_data['content']

            user = get_object_or_404(User, id=user_id)
            sender = get_object_or_404(User, id=sender_id)

            user_email = user.email
            sender_name = sender.username
            sender_email = sender.email

            send_mail(
                subject=f'"{sender_name}" sent you an email.',
                message=f"Sender: {sender_email}\n\n{content}",
                from_email=sender_email,  
                recipient_list=[user_email],  
                fail_silently=False,
            )
            return Response({"message": "Email sent"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
