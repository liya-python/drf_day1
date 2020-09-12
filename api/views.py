from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from app1.models import User


class StudentAPIView(APIView):
    def get(self,request,*args,**kwargs):
        stu_id = kwargs.get('id')
        if stu_id:
            stu_obj = User.objects.get(pk=stu_id)
            if stu_obj:
                return Response({
                    'status':200,
                    'message':'查询单个用户成功',
                    'result':{'username':stu_obj.username,'email':stu_obj.email}
                })
        else:
            stu_list = User.objects.all().values("username", "password", "gender", "email")
            return Response({
                'status': 200,
                'message': '查询所有用户成功',
                'result': list(stu_list),
            })
        return Response({
            'status': 500,
            'message': '查询失败',
        })

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        pwd = request.data.get('pwd')
        email = request.data.get('email')
        try:
            stu_obj = User.objects.create(username=username,password=pwd,email=email)
            return Response({
                'status':201,
                'message':'创建用户成功',
                'result':{'username':stu_obj.username,'email':stu_obj.email}
            })
        except:
            return Response({
                'status': 500,
                'message': '创建用户失败',

            })

    def put(self, request, *args, **kwargs):
        stu_id = kwargs.get('id')
        if stu_id:
            stu_obj = User.objects.get(pk=stu_id)
            if stu_obj:
                    username = request.data.get('username')
                    pwd = request.data.get('pwd')
                    gender = request.data.get('gender')
                    email = request.data.get('email')
                    try:
                        stu_obj.username =username
                        stu_obj.password = pwd
                        stu_obj.gender =gender
                        stu_obj.email =email
                        stu_obj.save()
                        return Response({
                            'status': 201,
                            'message': '更新用户成功',
                            'result': {'username': stu_obj.username, 'email': stu_obj.email}
                        })
                    except:
                        return Response({
                            'status': 500,
                            'message': '更新用户失败',
                        })
        return Response({
            'status': 500,
            'message': '未查到要更新的用户',
        })

