from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *
from django.db import transaction


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True,max_length=100)
    password = serializers.CharField(required=True,max_length=100)

    def validate(self, attrs):
        validation_errors = {}
        if User.objects.filter(username=attrs['username']).exists():
            validation_errors['username'] = "Username already exists"
        if len(attrs['password']) < 8:
            validation_errors['password'] = "Password should be atleast 8 characters"
        if validation_errors.keys():
            raise serializers.ValidationError(validation_errors)
        return attrs
    
    def save(self, **kwargs):
        try:
            user=User.objects.create(username=self.validated_data['username'])
            user.set_password(self.validated_data['password'])
            user.save()
            response = {"result":"success","message":"user registered successfully"}
        except Exception as e:
            print("....",e)
            response = {"result":"failure","message":"something went wrong"}
        finally:
            return response


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=100,required=True,min_length=8,write_only=True)
    confirm_password = serializers.CharField(max_length=100,required=True,min_length=8,write_only=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password":"passwords not same"})
        return attrs

    def save(self, **kwargs):
        try:
            request = self.context['request']
            user = User.objects.get(id=request.user.id)
            user.set_password(self.validated_data['password'])
            user.save()
            response = {"result":"success","message":"Profile updated"}
        except:
            response = {"result":"failure","message":"Something went wrong"}
        finally:
            return response


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','first_name','last_name','email','is_staff']
    

class ProfileSerializer(serializers.Serializer):
    user = UserSerializer(many=False,read_only=True)
    picture = serializers.FileField(read_only=True)
    place = serializers.CharField(max_length=100,read_only=True)
    gender = serializers.CharField(max_length=100,read_only=True)
    date_of_birth = serializers.DateField(read_only=True)


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['wallet_id','balance']


class ProfileUpdateSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100,required=True)
    last_name = serializers.CharField(max_length=100,required=False)
    email = serializers.EmailField(required=True)
    picture = serializers.FileField(required=False)
    place = serializers.CharField(max_length=100,required=True)
    gender = serializers.CharField(max_length=100,required=True)
    date_of_birth = serializers.DateField(required=True)

    def validate(self, attrs):
        validation_errors = {}
        if attrs['gender'] not in['male','female','other']:
            validation_errors['gender'] = "Please select a valid choice, Choices are male,female and other"
        if 'picture' in attrs:
            picure = str(attrs['picture'])
            extension = picure.split('.')[-1]
            if extension not in ['jpg','png','jpeg']:
                validation_errors['picture'] = "Only upload image with extensions jpg,png and jpeg"
        if validation_errors.keys():
            raise serializers.ValidationError(validation_errors)
        return attrs

    def save(self, **kwargs):
        try:
            with transaction.atomic():
                request = self.context['request']
                user_conditions = { i:self.validated_data[i] for i in self.validated_data.keys() if i in['first_name','last_name','email'] }
                profile_conditions = { i:self.validated_data[i] for i in self.validated_data.keys() if i in['picture','place','gender','date_of_birth'] }
                Profile.objects.filter(user=request.user).update(**profile_conditions)
                User.objects.filter(id=request.user.id).update(**user_conditions)
                respons = {"result":"success","message":"Profile updated"}
        except:
            respons = {"result":"failue","message":"Something went wrong"}
        return respons
        

class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=100,required=True,min_length=8,write_only=True)
    confirm_password = serializers.CharField(max_length=100,required=True,min_length=8,write_only=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password":"passwords not same"})
        return attrs

    def save(self, **kwargs):
        try:
            request = self.context['request']
            user = User.objects.get(id=request.user.id)
            user.set_password(self.validated_data['password'])
            user.save()
            response = {"result":"success","message":"Profile updated"}
        except:
            response = {"result":"failure","message":"Something went wrong"}
        finally:
            return response

