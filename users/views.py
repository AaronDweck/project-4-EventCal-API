from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotAuthenticated, ValidationError
from .serializers.common import UserSerializer
from datetime import datetime, timedelta
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

def generate_token(user):
    exp_date = datetime.now() + timedelta(days=1)
            
    token = jwt.encode(
        payload={
            'user': {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
            },
            'exp': int(exp_date.strftime('%s'))
        },
        key=settings.SECRET_KEY,
        algorithm='HS256'
    )

    return(token)

# Create your views here.
class RegisterView(APIView):

    def post(self, request):
        serialized_user = UserSerializer(data=request.data)
        if not serialized_user.is_valid():
            return Response(serialized_user.errors, 422)
        serialized_user.save()

        user = User.objects.get(email=request.data['email'])

        token = generate_token(user)

        return Response({'message': 'Registration was successful', 'token': token}, 201)
    
class LoginView(APIView):

    def post(self, request):
        try:
            user = User.objects.get(email=request.data['email'])

            if not user.check_password(request.data['password']):
                raise ValidationError('Incorrect password')
            
            token = generate_token(user)
            
            return Response({'message': 'Login was successful', 'token': token})

        except (User.DoesNotExist, ValidationError) as error:
            print(error)
            raise NotAuthenticated({'detail' : ['Invalid credentials']})
