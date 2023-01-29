from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .serializers import *
from .transaction_ser import *
from rest_framework import status
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken



class RegisterView(APIView):
    permission_classes = [AllowAny]    
    serializer_class = RegisterSerializer

    def post(self,request,*args, **kwargs):
        try:
            ser = self.serializer_class(data=request.data)
            if ser.is_valid():
                response = ser.save()
            else:
                response = {"result":"failure","errors":{ i:ser.errors[i][0] for i in ser.errors.keys()}}
        except Exception as e:
            print("...",e)
            response = {"result":"failure","message":"Something went wrong"}
        finally:
            return Response(response,status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]    
    serializer_class = ChangePasswordSerializer

    def post(self,request,*args, **kwargs):
        try:
            ser = self.serializer_class(data=request.data,context={'request':request})
            if ser.is_valid():
                response = ser.save()
            else:
                response = {"result":"failure","errors":{ i:ser.errors[i][0] for i in ser.errors.keys()}}
            return Response(response,status=status.HTTP_200_OK)
        except Exception as e:
            print("....",e)
            response = {"result":"failure","message":"Something went wrong"}
            return Response(response,status=status.HTTP_400_BAD_REQUEST)        


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message":"Logout success"},status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"message":"something went wrong"},status=status.HTTP_400_BAD_REQUEST)


class ProfileView(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        user_profile = {'get_user_profile':ProfileSerializer,'update_user_profile':ProfileUpdateSerializer,}
        if self.action in user_profile:
            return user_profile[self.action]

    def get_user_profile(self,request,*args, **kwargs):
        try:
            user = request.user
            queryset = Profile.objects.get(user=user)
            ser = self.get_serializer(queryset,many=False,context={'request':request})
            return Response({"result":"success","data":ser.data},status=status.HTTP_200_OK)
        except:
            return Response({"result":"failure","message":"Something went wrong"},status=status.HTTP_400_BAD_REQUEST)

    def update_user_profile(self,request,*args, **kwargs):
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


class WalletView(APIView):
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def get(self,request,*args, **kwargs):
        try:
            user = request.user
            queryset = Wallet.objects.get(user=user)
            ser = self.serializer_class(queryset,many=False,context={'request':request})
            return Response({"result":"success","data":ser.data},status=status.HTTP_200_OK)
        except:
            return Response({"result":"failure","message":"Invalid token or token blacklisted"},status=status.HTTP_400_BAD_REQUEST) 


class UserManagementView(ModelViewSet):
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        group_ser = {
            'user_list':ProfileSerializer,
            'user_details':ProfileSerializer,
            'transaction_list':TransactionSerializer,
            'transaction_details':TransactionSerializer,
            'request_list':RequestHistorySerializer,
            'request_details':RequestHistorySerializer,
        }
        if self.action in group_ser:
            return group_ser[self.action]
    
    def user_list(self,request,*args, **kwargs):
        try:
            queryset = Profile.objects.order_by("-id")
            ser = self.get_serializer(queryset,many=True,context={'request':request})
            return Response({"result":"success","data":ser.data},status=status.HTTP_200_OK)
        except:
            return Response({"result":"failure","message":"Something went wrong"},status=status.HTTP_400_BAD_REQUEST)

    def user_details(self,request,*args, **kwargs):
        try:
            user_id = kwargs.get('id')
            queryset = Profile.objects.get(user_id=user_id)
            ser = self.get_serializer(queryset,many=False,context={'request':request})
            return Response({"result":"success","data":ser.data},status=status.HTTP_200_OK)
        except:
            return Response({"result":"failure","message":"User not found"},status=status.HTTP_400_BAD_REQUEST)

    def transaction_list(self,request,*args, **kwargs):
        try:
            queryset = Transaction.objects.order_by("-id")
            ser = self.get_serializer(queryset,many=True,context={'request':request})
            return Response({"result":"success","data":ser.data},status=status.HTTP_200_OK)
        except:
            return Response({"result":"failure","message":"Something went wrong"},status=status.HTTP_400_BAD_REQUEST)

    def transaction_details(self,request,*args, **kwargs):
        try:
            transaction_id = kwargs.get('id')
            queryset = Transaction.objects.get(id=transaction_id)
            ser = self.get_serializer(queryset,many=False,context={'request':request})
            return Response({"result":"success","data":ser.data},status=status.HTTP_200_OK)
        except:
            return Response({"result":"failure","message":"Transaction not found"},status=status.HTTP_400_BAD_REQUEST)

    def request_list(self,request,*args, **kwargs):
        try:
            queryset = Request.objects.order_by("-id")
            ser = self.get_serializer(queryset,many=True,context={'request':request})
            return Response({"result":"success","data":ser.data},status=status.HTTP_200_OK)
        except:
            return Response({"result":"failure","message":"Something went wrong"},status=status.HTTP_400_BAD_REQUEST)

    def request_details(self,request,*args, **kwargs):
        try:
            request_id = kwargs.get('id')
            queryset = Request.objects.get(id=request_id)
            ser = self.get_serializer(queryset,many=False,context={'request':request})
            return Response({"result":"success","data":ser.data},status=status.HTTP_200_OK)
        except:
            return Response({"result":"failure","message":"Request not found"},status=status.HTTP_400_BAD_REQUEST)

    
    def make_staff(self,request,*args, **kwargs):
        try:
            user_id = kwargs.get('id')
            User.objects.filter(id=user_id).update(is_staff=True)
            return Response({"result":"success","message":"Successfully changed to admin user"},status=status.HTTP_200_OK)
        except:
            return Response({"result":"failure","message":"Something went wrong"},status=status.HTTP_400_BAD_REQUEST)
    
    def remove_staff(self,request,*args, **kwargs):
        try:
            user_id = kwargs.get('id')
            User.objects.filter(id=user_id).update(is_staff=False)
            return Response({"result":"success","message":"Successfully removed from admin user"},status=status.HTTP_200_OK)
        except:
            return Response({"result":"failure","message":"Something went wrong"},status=status.HTTP_400_BAD_REQUEST)
