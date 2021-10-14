from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response


class RegisterView(APIView):
    @staticmethod
    def post(request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if len(request.data['password']) < 6:
                return Response({"password": ["Password length must be atleast 6 characters"]})
            serializer.save()
        return Response(serializer.data)

