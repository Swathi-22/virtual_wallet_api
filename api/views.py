from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .serializers import ResgistrationSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]    
    serializer_class = ResgistrationSerializer

    def post(self,request,*args, **kwargs):
        try:
            ser = self.serializer_class(data=request.data)
            if ser.is_valid():
                response = ser.save()
            else:
                response = {"result":"failure","errors":{ i:ser.errors[i][0] for i in ser.errors.keys()}}
        except Exception as e:
            print("####",e)
            response = {"result":"failure","message":"Something went wrong"}
        finally:
            return Response(response,status=status.HTTP_200_OK)
