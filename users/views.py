from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from .serializers import RegisterUserSerializer, SignInSerializer, UserSerializers

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)

            print(serializer)  # Debug log
            print(request.data)  # Debug log
            
            if not serializer.is_valid():
                return Response({
                    "status": "error",
                    "message": "Validation failed",
                    "errors": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            user = serializer.save()

            return Response({
                "status": "success",
                "message": "Account created successfully",
                "data": {
                    "username": user.username,
                    "email": user.email
                }
            }, status=status.HTTP_201_CREATED)

        except IntegrityError:
            return Response({
                "status": "error",
                "message": "User with this username or email already exists"
            }, status=status.HTTP_409_CONFLICT)

        except Exception as e:
            return Response({
                "status": "error",
                "message": "An unexpected error occurred",
                "detail": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginView(generics.GenericAPIView):
    serializer_class = SignInSerializer

    def post(self, request, *args, **kwargs):
        try:
            username = request.data.get('username')
            password = request.data.get('password')

            print(f"Login attempt for username: {username}")  # Debug log

            if not username or not password:
                return Response({
                    "status": "error",
                    "message": "Both username and password are required"
                }, status=status.HTTP_400_BAD_REQUEST)

            # Try to get the user first to check if they exist
            try:
                user_exists = User.objects.get(username=username)
                print(f"User exists: {user_exists.username}")  # Debug log
            except User.DoesNotExist:
                print(f"User does not exist: {username}")  # Debug log
                return Response({
                    "status": "error",
                    "message": "Invalid credentials. Please check your username and password"
                }, status=status.HTTP_401_UNAUTHORIZED)

            # Now try to authenticate
            user = authenticate(username=username, password=password)
            print(f"Authentication result: {user}")  # Debug log

            if not user:
                return Response({
                    "status": "error",
                    "message": "Invalid credentials. Please check your username and password"
                }, status=status.HTTP_401_UNAUTHORIZED)

            refresh = RefreshToken.for_user(user)
            user_serializer = UserSerializers(user)

            return Response({
                "status": "success",
                "message": "Login successful",
                "data": {
                    "access_token": str(refresh.access_token),
                    "refresh_token": str(refresh),
                    "user": user_serializer.data
                }
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Login error: {str(e)}")  # Debug log
            return Response({
                "status": "error",
                "message": "An unexpected error occurred",
                "detail": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# class LogoutView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         refresh_token = request.COOKIES.get('refresh_token')

#         if refresh_token:
#             try:
#                 refresh = RefreshToken(refresh_token)
#                 refresh.blacklist()
#             except Exception as e:
#                 return Response({"message": "Something went wrong !!", "error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

#         response = Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
#         response.delete_cookie("access_token")
#         response.delete_cookie("refresh_token")

#         return response

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            user_serializer = UserSerializers(user)

            return Response({
                "status": "success",
                "message": "Dashboard data retrieved successfully",
                "data": {
                    "user": user_serializer.data,
                    "last_login": user.last_login,
                    "date_joined": user.date_joined
                }
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "status": "error",
                "message": "Failed to retrieve dashboard data",
                "detail": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
