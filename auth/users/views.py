from .serializers import UserSerializer
from .models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status, permissions


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh_token': str(refresh),
        'access_token': str(refresh.access_token),
    }


def get_user_from_token(request):
    jwt = JWTAuthentication()
    header = jwt.get_header(request)
    raw_token = jwt.get_raw_token(header)
    validated_token = jwt.get_validated_token(raw_token)
    user = jwt.get_user(validated_token)
    return user


class RegisterView(APIView):
    @staticmethod
    def post(request):
        if len(request.data['password']) < 6:
            return Response({"password": ["Password length must be atleast 6 characters"]})
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        user = User.objects.get(email=serializer.data['email'])
        token = get_tokens_for_user(user)
        refresh_token = token['refresh_token']
        access_token = token['access_token']
        return Response({**serializer.data, "refresh_token": refresh_token, "access_token": access_token})


class LoginView(APIView):
    @staticmethod
    def post(request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()
        print('user: ', user)

        if user is None:
            raise AuthenticationFailed('User not found')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        token = get_tokens_for_user(user)
        return Response(
            {"message": "Successfully logged in.", "refresh_token": token['refresh_token'], "access_token": token['access_token']}
        )


class GetUser(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def get(request):
        user = get_user_from_token(request)
        print('user:', user)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)