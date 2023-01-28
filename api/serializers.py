from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *
from django.db import transaction


class ResgistrationSerializer(serializers.Serializer):
    username = serializers.CharField(required=True,max_length=100)
    password = serializers.CharField(required=True,max_length=100)

    def validate(self, data):
        validation_errors = {}
        if User.objects.filter(username=data['username']).exists():
            validation_errors['username'] = "Username already exists"
        if len(data['password']) < 8:
            validation_errors['password'] = "Password should be atleast 8 characters"
        if validation_errors.keys():
            raise serializers.ValidationError(validation_errors)
        return data


    def save(self, **kwargs):
        try:
            user=User.objects.create(username=self.validated_data['username'])
            user.set_password(self.validated_data['password'])
            user.save()
            response = {"result":"success","message":"user registered successfully"}
        except Exception as e:
            print("####",e)
            response = {"result":"failure","message":"something went wrong"}
        finally:
            return response