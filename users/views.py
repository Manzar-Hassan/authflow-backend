from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterUserSerializer, SignInSerializer, UserSerializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer


class LoginView(generics.GenericAPIView):
    serializer_class = SignInSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            user_serializer = UserSerializers(user)

            response = Response({
                "message": "Login successful",
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": user_serializer.data,
            }, status=status.HTTP_200_OK)

            return response

        return Response({'message': 'Invalid Credential'}, status=401)


# class LogoutView(APIView):
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

    def get(self, req):
        user = req.user
        user_serializer = UserSerializers(user)

        return Response({
            'message': 'Welcome to dashboard !!',
            'user': user_serializer.data
        }, 200)
