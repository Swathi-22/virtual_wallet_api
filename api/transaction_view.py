from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .transaction_ser import *
from rest_framework import status
from .models import *
from django.db.models import Q


class TransactionView(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        group_ser = {
            'send_money':SendMoneySerializer,
            'add_money':AddMoneySerializer,
            'history':TransactionSerializer,
        }
        if self.action in group_ser:
            return group_ser[self.action]
            
    def send_money(self,request,*args, **kwargs):
        try:
            ser = self.get_serializer(data=request.data,context={'request':request})
            if ser.is_valid():
                response = ser.save()
            else:
                response = {"result":"failure","errors":{ i:ser.errors[i][0] for i in ser.errors.keys()}}
            return Response(response,status=status.HTTP_200_OK)
        except Exception as e:
            print("####",e)
            response = {"result":"failure","message":"Something went wrong"}
            return Response(response,status=status.HTTP_400_BAD_REQUEST)

    def add_money(self,request,*args, **kwargs):
        try:
            ser = self.get_serializer(data=request.data,context={'request':request})
            if ser.is_valid():
                response = ser.save()
            else:
                response = {"result":"failure","errors":{ i:ser.errors[i][0] for i in ser.errors.keys()}}
            return Response(response,status=status.HTTP_200_OK)
        except Exception as e:
            print("####",e)
            response = {"result":"failure","message":"Something went wrong"}
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
    
    def history(self,request,*args, **kwargs):
        try:
            user = request.user
            queryset = Transaction.objects.filter(Q(from_user=user)|Q(to_user=user)).order_by("-id")
            ser = self.get_serializer(queryset,many=True,context={'request':request})
            return Response({"result":"success","data":ser.data},status=status.HTTP_200_OK)
        except Exception as e:
            print("###",e)
            return Response({"result":"failure","message":"Something went wrong"},status=status.HTTP_400_BAD_REQUEST) 


class RequestView(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        group_ser = {
            'request_money':RequestMoneySerializer,
            'history':RequestHistorySerializer
        }
        if self.action in group_ser:
            return group_ser[self.action]

    def request_money(self,request,*args, **kwargs):
        try:
            ser = self.get_serializer(data=request.data,context={'request':request})
            if ser.is_valid():
                response = ser.save()
            else:
                response = {"result":"failure","errors":{ i:ser.errors[i][0] for i in ser.errors.keys()}}
            return Response(response,status=status.HTTP_200_OK)
        except Exception as e:
            print("###",e)
            response = {"result":"failure","message":"Something went wrong"}
            return Response(response,status=status.HTTP_400_BAD_REQUEST)

    def history(self,request,*args, **kwargs):
        try:
            user = request.user
            queryset = Request.objects.filter(Q(from_user=user)|Q(to_user=user)).order_by("-id")
            ser = self.get_serializer(queryset,many=True,context={'request':request})
            return Response({"result":"success","data":ser.data},status=status.HTTP_200_OK)
        except Exception as e:
            print("###",e)
            return Response({"result":"failure","message":"Something went wrong"},status=status.HTTP_400_BAD_REQUEST) 
    
    def accept_request(self,request,*args, **kwargs):
        try:
            with transaction.atomic():
                request_id = kwargs.get("id")
                request_obj = Request.objects.get(id=request_id)
                if request_obj.to_user == request.user:
                    from_user = request.user
                    to_user = request_obj.from_user
                    amount = request_obj.amount
                    Transaction.objects.create(from_user=from_user,to_user=to_user,amount=amount,status=2)

                    from_user_wallet = Wallet.objects.get(user=from_user)
                    if from_user_wallet.balance < amount:
                        return Response({"result":"success","error":{"amount":"No Enough Balance to send money, Please add money to wallet"}},status=status.HTTP_200_OK)
                    old_balance = from_user_wallet.balance
                    new_balance = old_balance - amount
                    from_user_wallet.balance = new_balance
                    from_user_wallet.save()

                    to_user_wallet = Wallet.objects.get(user=to_user)
                    old_balance = to_user_wallet.balance
                    new_balance = old_balance + amount
                    to_user_wallet.balance = new_balance
                    to_user_wallet.save()
                    request_obj.status = 2
                    request_obj.save()
                    return Response({"result":"success","data":"Payment success"},status=status.HTTP_200_OK)
                else:
                    return Response({"result":"failure","message":"Request is not to you"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("###",e)
            return Response({"result":"failure","message":"Something went wrong"},status=status.HTTP_400_BAD_REQUEST) 

    def reject_request(self,request,*args, **kwargs):
        try:
            with transaction.atomic():
                request_id = kwargs.get("id")
                request_obj = Request.objects.get(id=request_id)
                if request_obj.to_user == request.user:
                    request_obj.status = 3
                    request_obj.save()
                    return Response({"result":"success","data":"Request rejected"},status=status.HTTP_200_OK)
                else:
                    return Response({"result":"failure","message":"Request is not to you"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("###",e)
            return Response({"result":"failure","message":"Something went wrong"},status=status.HTTP_400_BAD_REQUEST) 
