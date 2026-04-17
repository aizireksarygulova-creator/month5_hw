from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import ConfirmSerializer, RegisterSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import UserConfirmation
import random
from rest_framework.views import APIView 


class AuthorizationAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            try:
                token = Token.objects.get(user=user)
            except:
                token = Token.objects.create(user=user)
            return Response(data={'key': token.key})
        return Response(status=status.HTTP_401_UNAUTHORIZED)
           
 
class RegistrationAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        user = User.objects.create_user(
            username=username,
            password=password,
            is_active=False  
        )

        code = str(random.randint(100000, 999999))

        UserConfirmation.objects.create(
            user=user,
            code=code
        )

        return Response({
            'user_id': user.id,
            'code': code  
        }, status=201)


class ConfirmAPIView(APIView):
    def post(self, request):
        serializer = ConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = request.data.get('user_id')
        code = request.data.get('code')

        try:
            user = User.objects.get(id=user_id)
            confirm = UserConfirmation.objects.get(user=user)
        except User.DoesNotExist:
            return Response({'error': 'user not found'})
        except UserConfirmation.DoesNotExist:
            return Response({'error': 'confirmation not found'})

        if confirm.code == code:
            user.is_active = True
            user.save()
            return Response({'message': 'confirmed'})
        
        return Response({'error': 'wrong code'})




#aziko 123