from .serializers import UserSerializer
from .models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh_token': str(refresh),
        'access_token': str(refresh.access_token),
    }


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
    def get(self, request):
        print('request: ',  request.headers['Authorization'])
        return Response("This is to return user data")

