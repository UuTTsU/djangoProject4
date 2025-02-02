from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from .models import CustomUser
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from rest_framework.permissions import AllowAny
class Home(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)

class RegisterUserView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUser(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = None
        if '@' in username:  # Check if the username is an email
            try:
                user = CustomUser.objects.get(email=username)
            except ObjectDoesNotExist:
                pass

        if not user:
            user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            access = AccessToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(access),
            }, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutUser(APIView):
        permission_classes = [IsAuthenticated]

        def post(self, request):
            try:
                refresh_token = request.data.get('refresh_token')
                if not refresh_token:
                    return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

                token = RefreshToken(refresh_token)
                token.blacklist()

                return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)