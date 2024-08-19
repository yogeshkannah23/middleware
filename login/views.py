from django.shortcuts import render
from django.http import HttpResponse,request,JsonResponse
from rest_framework.decorators import APIView
from login.serializers import UserSerializers,PostSerializers
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from login.models import User,Post

import datetime
import jwt
# Create your views here.

def index(request):
    return HttpResponse("hi")



class Register(APIView):

    def post(self,request):
        serializer = UserSerializers(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
class AddPost(APIView):

    def post(self,request):

        token = request.data['jwt']
        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('unauthenticated!')
        
        user = User.objects.filter(id = payload['id']).first()
        serializer = UserSerializers(user)
        serializer_post = PostSerializers(data = request.data)
        if serializer_post.is_valid():
            user = User.objects.filter(email=serializer.data['email']).first()
            serializer_post.save(author=user)
            return Response(serializer_post.data)
        else:
            return JsonResponse({"message":"failed"})

class LoginView(APIView):

    def post(self,request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()


        if email is None:
            raise AuthenticationFailed("Email id not found")

        if not user.check_password(password):
            raise AuthenticationFailed("Password incorrect")        

        payload = {
            'id':user.id,
            'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat':datetime.datetime.utcnow()
        }

        token = jwt.encode(payload,'secret',algorithm='HS256')

        response = Response()
        # response.set_cookie(key='jwt',value=token,httponly=True)
        # print(token)
        response.data={
            'jwt':str(token)
        }
        # print(response))
        return response
    
class UserView(APIView):
    def get(self,request):
        # token = request.COOKIES.get('jwt')
        token = request.data['jwt']

        if not token:
            raise AuthenticationFailed("Unauthenticated")

        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('unauthenticated!')
        
        user = User.objects.filter(id = payload['id']).first()
        serializer = UserSerializers(user)

        return Response(serializer.data)


class GetAllPost(APIView):
    def get(self,request):
        token = request.data['jwt']

        if not token:
            raise AuthenticationFailed("Unauthenticated")

        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired!')
        
        # user_id = payload['id']
        # request.data['author'] = user_id
        post = request.posts
        serializers = PostSerializers(post,many=True)

        return Response(serializers.data)
    
class GetByUser(APIView):
    def get(self,request):
        token = request.data['jwt']

        if not token:
            raise AuthenticationFailed("Unauthenticated")

        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('unauthenticated!')
        
        
        post = Post.objects.filter(author=payload['id'])
        serializers = PostSerializers(post,many=True)
        return Response(serializers.data)
