from rest_framework.views import APIView
from .serializers import UserSerializer
from .models import User
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed


class RegisterView(APIView):
    @staticmethod
    def post(request):
        if len(request.data['password']) < 6:
            return Response({"password": ["Password length must be atleast 6 characters"]})
        serializer = UserSerializer(data=request.data)
        print('before')
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            print('after')
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user =User.objects.filter(email=email).first()
        print('user: ', user)

        if user is None:
            raise AuthenticationFailed('User not found')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        return Response({
            "message": "Success"
        })




