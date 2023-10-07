from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_jwt.settings import api_settings
from rest_framework.decorators import api_view
from .models import User,Todo
# Create your views here.
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

def my_views(request):
    return HttpResponse("Todo App")

class SignupView(APIView):
    def post(self,request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        age = request.data.get('age')
        gender = request.data.get('gender')

        if not username or not email or not password:
            return Response({'error':"Usename , Password and Email are required fields!"})
        
        try:
            user = User(username=username , email=email , password=password , age = age , gender=gender)
            user.set_password(password)
            user.save()
            return Response({'msg':"User Successfully Created!" }, status=status.HTTP_201_CREATED )

        except Exception as e:
            return Response({'error': f'Could not create User. Error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginView(APIView):
    def post(self,request):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"msg":"Invalid Email or password"} , status=status.HTTP_401_UNAUTHORIZED)
        
        if user.check_password(password):
            user_id = str(user.id)

            payload = {
                'user_id': user_id,
                'username': user.username
            }
        
            print(payload)

            token = jwt_encode_handler(payload)

            return Response({'msg':"Login Successfull!" , 'token':token , 'payload':payload} , status=status.HTTP_200_OK)
        
        else:
            return Response({'error': 'Invalid email or password.'}, status=status.HTTP_401_UNAUTHORIZED)

class CreateTodoView(APIView):
    def post(self,request):
        user_id = request.data.get("user_id")
        title = request.data.get("title")
        description = request.data.get("description")
        completed = request.data.get("completed")

        try:
            user = User.objects.get(id = user_id)

            todo = Todo(
                title=title,
                description=description,
                completed=completed,
                user = user,
                user_name = user.username,
            )
            todo.save()

            return Response({'message': 'Todo created successfully.'}, status=status.HTTP_201_CREATED)
        except Todo.DoesNotExist :
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Could not create a Todo. Error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetTodoView(APIView):
    def get(self,request,user_id):
        try:
            user = User.objects.get(id = user_id)

            todo = Todo.objects.filter(user=user)

            arr=[]

            for el in todo:
                arr.append({
                    'user_id':str(el.id),
                    'title':el.title,
                    'description': el.description,
                    'completed':el.completed,
                    'user_name':el.user_name
                })
            
            return Response(arr , status=status.HTTP_200_OK)
        except Todo.DoesNotExist:
            return Response({'error': 'Todo not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Could not retrieve Todo. Error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





        

