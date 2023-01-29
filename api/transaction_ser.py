from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *
from django.db import transaction
from .serializers import UserSerializer


class SendMoneySerializer(serializers.Serializer):
    to_user_id = serializers.IntegerField(required=True)
    amount = serializers.DecimalField(required=True,max_digits=15,decimal_places=2)

    def validate(self, attrs):
        request = self.context['request']
        if attrs['amount'] < 1:
            raise serializers.ValidationError({'amount':"Minimum 1 Rupees needed"})
        if request.user.id == attrs['to_user_id']:
            raise serializers.ValidationError({'to_user_id':"You cant't tranfer money to your wallet"})
        wallet = Wallet.objects.get(user=request.user)
        if wallet.balance < attrs['amount']:
           raise serializers.ValidationError({'amount':"No Enough Balance to send money, Please add money to wallet"})
        return attrs
    
    def save(self, **kwargs):
        request = self.context['request']
        try:
            amount = self.validated_data['amount']
            with transaction.atomic():
                Transaction.objects.create(from_user_id=request.user.id,to_user_id=self.validated_data['to_user_id'],amount=amount,status=2)

                from_user_wallet = Wallet.objects.get(user=request.user)
                old_balance = from_user_wallet.balance
                new_balance = old_balance - amount
                from_user_wallet.balance = new_balance
                from_user_wallet.save()

                to_user_wallet = Wallet.objects.get(user=self.validated_data['to_user_id'])
                old_balance = to_user_wallet.balance
                new_balance = old_balance + amount
                to_user_wallet.balance = new_balance
                to_user_wallet.save()
                response = {"result":"success","message":"Payment Success"}
        except:
            response = {"result":"failure","message":"Something went wrong"}
        return response


class AddMoneySerializer(serializers.Serializer):
    amount = serializers.DecimalField(required=True,max_digits=15,decimal_places=2)

    def save(self, **kwargs):
        request = self.context['request']
        try:
            wallet = Wallet.objects.get(user=request.user)
            old = wallet.balance
            new = old + self.validated_data['amount']
            wallet.balance = new
            wallet.save()
            response = {"result":"success","message":"Recharge Success"}
        except:
            response = {"result":"failure","message":"Something went wrong"}
        return response


class TransactionSerializer(serializers.ModelSerializer):
    from_user = UserSerializer(many=False,read_only=True)
    to_user = UserSerializer(many=False,read_only=True)
    status = serializers.SerializerMethodField()

    def get_status(self,obj):
        statuses = {
            "Pending":"Pending",
            "Completed":"Completed",
            "Failed":"Failed",
        }
        if obj.status in statuses:
            return statuses[obj.status]
    
    class Meta:
        model = Transaction
        fields = ['id','from_user','to_user','amount','status','created_at']


class RequestMoneySerializer(serializers.Serializer):
    to_user_id = serializers.IntegerField(required=True)
    amount = serializers.DecimalField(required=True,max_digits=15,decimal_places=2)

    def validate(self, attrs):
        request = self.context['request']
        if attrs['amount'] < 1:
            raise serializers.ValidationError({'amount':"Minimum 1 Rupees needed"})
        if request.user.id == attrs['to_user_id']:
            raise serializers.ValidationError({'to_user_id':"You cant't request money to your wallet"})
        return attrs
    
    def save(self, **kwargs):
        request = self.context['request']
        try:
            amount = self.validated_data['amount']
            with transaction.atomic():
                Request.objects.create(from_user_id=request.user.id,to_user_id=self.validated_data['to_user_id'],amount=amount,status=1)
                response = {"result":"success","message":"Request was Success"}
        except:
            response = {"result":"failure","message":"Something went wrong"}
        return response


class RequestHistorySerializer(serializers.ModelSerializer):
    from_user = UserSerializer(many=False,read_only=True)
    to_user = UserSerializer(many=False,read_only=True)
    status = serializers.SerializerMethodField()

    def get_status(self,obj):
        statuses = {
            "Pending":"Pending",
            "Accepted":"Accepted",
            "Rejected":"Rejected",
        }
        if obj.status in statuses:
            return statuses[obj.status]
    
    class Meta:
        model = Request
        fields = ['id','from_user','to_user','amount','status','created_at']
