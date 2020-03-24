from django.shortcuts import render

# Create your views here.

from django.http import  HttpResponse,JsonResponse,HttpResponseRedirect
from django.views import  View
from userapp.models import *
from utils.code import  *


class RegisterView(View):
    def get(self,request):

        return render(request,'register.html')

    def post(self,request):
        #获取请求参数
        uname = request.POST.get('uname','')
        pwd = request.POST.get('pwd','')


        #插入数据库
        user = UserInfo.objects.create(uname=uname,pwd=pwd)

        #判断是否注册成功
        if user:
            request.session['user'] = user #将用户信息存放到session中，通过全局上下文操作

            return HttpResponseRedirect('/user/center/')

        return HttpResponseRedirect('/user/register/')


class CheckUnameView(View):
    def get(self,request):
        #获取请求参数
        uname = request.GET.get('uname','')

        #根据用户名去数据库中查询
        userList = UserInfo.objects.filter(uname=uname)

        flag = False

        #判断是否存在
        if userList:
            flag = True

        return JsonResponse({'flag':flag})

class CenterView(View):
    def get(self,request):
        return  render(request,'center.html')


class LogoutView(View):
    def post(self,request):
        #删除session中数据
        if 'user' in request.session:
            del request.session['user']
        return  JsonResponse({'delflag':True})

class LoginView(View):
    def get(self,request):
        return render(request,'login.html')

class LoadCodeView(View):
    def get(self,request):
        img,str = gene_code()
        return HttpResponse(img,content_type='image/png')