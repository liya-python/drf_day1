from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.decorators import  method_decorator
# Create your views here.
from django.views import View
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request
from app1.models import User
from rest_framework.renderers import BrowsableAPIRenderer,JSONRenderer
from rest_framework.parsers import JSONParser

'''
Django的视图模式分为两种
FBV:函数视图 function base view 基于函数定义的逻辑视图
CBV:类视图 class base view 基于类定义的视图
'''
# @csrf_protect  # 为某个视图单独开启csrf认证
@csrf_exempt  # 为某个视图免除csrf认证
def user(request):

    if request.method == 'GET':
        print(request.GET.get('username'))
        print('GET 访问成功')
        #  TODO 查询用户相关的操作
        return HttpResponse('GET 访问成功')
    if request.method == 'POST':
        print(request.POST.get('username'))
        # print('POST 访问成功')
        #  TODO 新增用户相关的操作
        return HttpResponse('POST 访问成功')
    if request.method == 'PUT':
        # print(request.POST.get('username'))
        print('PUT 更新成功')
        #  TODO 更新用户相关的操作
        return HttpResponse('PUT 访问成功')
    if request.method == 'DELETE':
        # print(request.POST.get('username'))
        print('DELETE 删除成功')
        #  TODO 删除用户相关的操作
        return HttpResponse('DELETE 访问成功')

@method_decorator(csrf_exempt,name='dispatch')  #让类视图免除crsf认证
class UserView(View):
    '''
    Django 的视图类
    '''
    def get(self,request,*args,**kwargs):
        print('GET请求 查询')
        return  HttpResponse('GET SUCCESS')
    def post(self,request,*args,**kwargs):
        print('POST请求 新增')
        return  HttpResponse('POST SUCCESS')
    def put(self,request,*args,**kwargs):
        print('PUT请求 更新')
        return  HttpResponse('PUT SUCCESS')
    def delete(self,request,*args,**kwargs):
        print('DELETE请求 删除')
        return  HttpResponse('DELETE SUCCESS')

'''
单个：获取单个 获取所有 添加单个 整体更新单个 局部更新单个
群体：一次增加多个   删除多个    整体修改多个  局部多个
'''
@method_decorator(csrf_exempt, name="dispatch")
class EmployeeView(View):

    def get(self, request, *args, **kwargs):
        """
        查询用户接口
        :param request: 请求对象，要有查询用户的id
        :return: 查询后的结果
        """

        # 获取前端传递的用户id
        user_id = kwargs.get('id')
        if user_id:
            # user_obj = User.objects.get(pk=user_id)
            user_obj = User.objects.filter(pk=user_id).values("username", "password", "gender", "email").first()
            # print(user_obj,type(user_obj))
            if user_obj:
                # 如果查询出对应的用户查信息，则将用户的信息返回到前台
                return JsonResponse({
                    'status':200,
                    'message':'查询单个用户成功',
                    'result':user_obj,
                })
        else:
            # 如果用户id为空，则代表要查询所有用户信息
            user_list = User.objects.all().values("username", "password", "gender", "email")
            print(user_list)
            return JsonResponse({
                'status': 200,
                'message': '查询所有用户成功',
                'result': list(user_list),
            })
        return JsonResponse({
            'status': 500,
            'message': '查询失败',
        })

    def post(self,request,*args,**kwargs):
        '''
        新增单个用户的信息
        :param request: 用户输入信息
        :param args:
        :param kwargs:
        :return:
        '''
        username = request.POST.get('username')
        pwd = request.POST.get('pwd')
        email = request.POST.get('email')
        # print(username,pwd,email)
        try:
            user_obj = User.objects.create(username=username,password=pwd,email=email)
            return JsonResponse({
                'status':201,
                'message':'创建用户成功',
                'result':{'username':user_obj.username,'email':user_obj.email}
            })
        except:
            return JsonResponse({
                'status': 500,
                'message': '创建用户失败',

            })

class UserAPIView(APIView):

    # 为某个类单独指定渲染器
    # 局部的渲染器比全局的优先级要高

    renderer_classes = (JSONRenderer,) # 元组

    # 指定此视图接收的参数类型
    parser_classes = [JSONParser]

    def get(self, request, *args, **kwargs): # DRF类视图中的request对象是经过封装后的request对象
        # 通过django原生的request对象来获取参数
        # 如果要访问django原生的request对象，可以通过_request来访问
        print(request._request.GET.get('username')) # 不推荐 了解即可

        # 可以通过DRF的request对象获取参数
        print(request.GET.get('username'))
        # 可以通过 query_params来获取参数 DRF扩展的方法
        print(request.query_params.get('username'))
        # 获取路径传参
        user_id = kwargs.get('id')
        return Response("DRF GET OK")

    def post(self, request, *args, **kwargs):

        # post 请求传递参数的形式 form_data www-urlencoded json
        print(request._request.POST,'3') #django原生的request对象 json拿不到
        print(request.POST,'2') #DRF封装后的request对象 json拿不到
        # DRF扩展的请求参数 兼容性最强 可以接受任意类型的参数
        print(request.data,'1')
        return Response("DRF POST OK")