from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, logout
from rest_framework.authtoken.models import Token
from ..serializers import UserRegistrationSerializer
from rest_framework import generics

class RegisterUserAPIView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            message = f"User {user.username} has been created successfully!"
            response_data = {
                'user': {
                    'id': user.id,
                    'username': user.username,
                },
                'message': message  
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ObtainAuthTokenAPIView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token = Token.objects.create(user=user) 
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

class DeleteAuthTokenAPIView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            # Delete the user's token
            Token.objects.filter(user=user).delete()
            # Logout the user
            logout(request)
            return Response({'success': 'Logged out successfully'})
        else:
            return Response({'error': 'User not authenticated'}, status=status.HTTP_400_BAD_REQUEST)
