"""Functionality file"""

import datetime

from django.contrib.auth import authenticate

from django.db.models import Q

# Create your views here.
from rest_framework import status

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from rest_framework.views import APIView

from Loginandlogout.models import Account, StudentData
from Loginandlogout.serializers import StudentDataSerializer
from Loginandlogout.utils import CustomMessage


class RegisterAPI(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            name = request.data['name']
            user_name = request.data['user_name']
            password = request.data['password']
            mobile = request.data.get("mobile", None)
            email = request.data.get('email', None)
            if len(name) > 60:
                raise CustomMessage("Name cannot be more than 60 Characters")
            try:
                Account.objects.get(user_name=user_name)
                raise CustomMessage("username already exists")
            except Account.DoesNotExist:
                pass
            if len(user_name) < 5 or len(user_name) > 100:
                raise CustomMessage(
                    "Username length should be 5 to 100 characters")
            if len(password) < 8 or len(password) > 15:
                raise CustomMessage(
                    "Password length should be between 8 to 15 characters")
            if mobile and len(mobile) > 10:
                raise CustomMessage(
                    "Mobile cannot be more than 10 Characters")
            if email and '@' not in email:
                raise CustomMessage("Email is invalid")
            Account.objects.create_user(name=name, password=password,
                                        email=email, mobile=mobile,
                                        user_name=user_name)

            return Response({"data": {"is_success": True, "name": name,
                                      "message": "Account created successfully"},
                             })
        except CustomMessage as e:
            return Response(
                {"data": {"is_success": False, "message": e.message}},
                status=status.HTTP_200_OK)
                
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
         

class LoginAPI(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            user_name = request.data['user_name']
            password = request.data['password']
            user = authenticate(request, user_name=user_name,
                                password=password)
            if user is not None:
                user_obj = Account.objects.get(user_name=user_name)
                jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
                payload = jwt_payload_handler(user_obj)
                del payload['email']
                payload["first_name"] = user_obj.name
                token = jwt_encode_handler(payload)
                StudentData.objects.create(student=user_obj)

                return Response({"data": {"is_success": True,
                                          "message": "Login Success",
                                          "token": token}},
                               )
            else:
                raise CustomMessage("Credentials didn't match")
        except CustomMessage as e:
            return Response(
                {"data": {"is_success": False, "message": e.message}},
                status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                 "message": "fail", "raw_message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Logout(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            student_obj = StudentData.objects.filter(
                Q(student=request.user) & Q(
                    logout_datetime__isnull=True)).order_by('-id')
            if student_obj:
                student_obj2 = student_obj[0]
                student_obj2.logout_datetime = datetime.datetime.now()
                student_obj2.save()
            else:
                raise CustomMessage("User is not logged in")
            return Response({"data": {"is_success": True,
                                      'message': "Logout Successful"}},
                            status=status.HTTP_200_OK)
        except CustomMessage as e:
            return Response(status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"message": "fail", "error": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StudentDataAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            try:
                Account.objects.get(Q(id=request.user.id))
            except StudentData.DoesNotExist:
                raise CustomMessage("Student ID is invalid")
            student_data_obj = StudentData.objects.filter(
                Q(student=request.user) &
                Q(created_date=datetime.datetime.today()))
            serializer_data = StudentDataSerializer(student_data_obj,
                                                    many=True).data
            login_count = 0
            logout_count = 0
            for i in serializer_data:
                if i["login_datetime"]:
                    login_count += 1
                if i["logout_datetime"]:
                    logout_count += 1
            return Response({"data": {"is_success": True,
                                      'message': serializer_data,
                                      "login_count": login_count,
                                      "logout_count": logout_count}},
                            status=status.HTTP_200_OK)
        except CustomMessage as e:
            return Response(status=status.HTTP_403_FORBIDDEN)
       
        except Exception as e:
            return Response({"message": "fail", "error": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
