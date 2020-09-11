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
            return Response({
                'status':200,
                'message':'查询单个用户成功',
                'result':{'username':stu_obj.username,'email':stu_obj.email}
            })