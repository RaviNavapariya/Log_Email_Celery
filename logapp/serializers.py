from rest_framework import serializers
from django.contrib.auth.models import User
from logapp.models import LogModel, FindindexModel


#############################################


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField()    
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password']

    def create(self, validated_data):
        user = User.objects.create(
        username=validated_data['username'],
        email=validated_data['email'],
        first_name=validated_data['first_name'],
        last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class LogCreateSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = LogModel
        fields = ['type', 'sub_type', 'shift_name', 'description', 'user']


class FindindexSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = FindindexModel
        fields = ['json_field', 'user']


class EmailSendSerializer(serializers.Serializer):
    sender_email = serializers.ListField()