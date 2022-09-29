from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer, LogCreateSerializer, FindindexSerializer, EmailSendSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login
from rest_framework.permissions import IsAuthenticated
from .models import LogModel, FindindexModel
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status
from django.template.loader import render_to_string
from rest_framework import generics
from logapp.tasks import send_feedback_email_task


####################################################


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class LoginAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user_data = User.objects.filter(email=email).first()
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=user_data, password=password)
            if user:
                login(request, user)
                data = {
                    'user':user.email,
                    'token':get_tokens_for_user(user)
                }
                return Response(data)            
        return Response(serializer.errors)


class LogCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        model = LogModel.objects.all()
        serializer = LogCreateSerializer(model, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LogCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data)


class NewLogLogCreatePost(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = LogModel.objects.all()
    serializer_class = LogCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = LogCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)


class FindindexAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_data = FindindexModel.objects.filter(user=request.user).first()
        if user_data:
            serializer = FindindexSerializer(user_data, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"Message":"Updated Successfully!!!!!!!!!!!"})
        serializer = FindindexSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data)


class EmailSendAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        findindex_data = FindindexModel.objects.filter(user=request.user).first()
        if findindex_data is None:
            serializer = EmailSendSerializer(data=request.data)
            if serializer.is_valid():
                log_data = LogModel.objects.filter(user=request.user).values()
                user_id = request.data.get('sender_email')
                user_email = User.objects.filter(id__in=user_id).values_list('email',flat=True)
                subject = 'Welcome to Findindex Project.'
                message = f'See below list of your findindex data.'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = user_email
                send_feedback_email_task.delay(subject, message, email_from, recipient_list, data_list)
                return Response({"message":"Email Send Successfully!!!"}, status=status.HTTP_200_OK)
            return Response(serializer.errors)
        else:
            log_data = LogModel.objects.filter(user=request.user)
            data_list = []  
            for i in findindex_data.json_field:
                for j in log_data.values(i):
                    data_list.append(j)
            user_id = request.data.get('sender_email')
            user_email = User.objects.filter(id__in=user_id).values_list('email',flat=True)
            subject = 'Welcome to Findindex Project.'
            message = f'See below list of your findindex data.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = list(user_email)
            send_feedback_email_task.delay(subject, message, email_from, recipient_list, data_list)
            return Response({"message":"Email Send Successfully!!!"}, status=status.HTTP_200_OK)
