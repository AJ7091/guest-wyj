from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event,Guest
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.shortcuts import render,get_object_or_404

# Create your views here.
def index(request):
    #return HttpResponse("Hellow,Django!")
    return render(request,"index.html")

#登录动作
def login_action(request):
    if request.method=='POST':
        username=request.POST.get('username','')
        password=request.POST.get('password','')
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user) #登录
            #return HttpResponse('Login Sucesss!')
            #response.set_cookie('user',username,3600) # 添加浏览器cookie
            request.session['user']=username # 将session信息写到服务器
            response = HttpResponseRedirect('/event_manage/')
            return response

        else:
            return render(request,'index.html',{'error':'username or password error!'})

#发布会管理
@login_required()
def event_manage(request):
    #username=request.COOKIES.get('user','') # 读取浏览器cookie
    username = request.session.get('user', '')  # 读取服务器session信息
    event_list=Event.objects.all()

    paginator=Paginator(event_list,2)
    page=request.GET.get('page')
    try:
        contacts=paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    return render(request,'event_manage.html',{'user':username,'events':contacts})

#嘉宾管理
@login_required()
def guest_manage(request):
    username=request.session.get('user','')
    guest_list=Guest.objects.all()

    paginator= Paginator(guest_list,2)
    page= request.GET.get('page')
    try:
        contacts=paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    return render(request,'guest_manage.html',{'user':username,'guests':contacts})


#发布会名称搜索
@login_required()
def search_name(request):
    username= request.session.get('user','')
    search_name= request.GET.get('name','')
    event_list= Event.objects.filter(name__contains=search_name)

    paginator = Paginator(event_list, 2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    return render(request,'event_manage.html',{'user':username,'events':contacts})

#嘉宾手机号搜索
@login_required()
def search_phone(request):
    username= request.session.get('user','')
    search_phone= request.GET.get('phone','')
    search_name_bytes = search_phone.encode(encoding="utf-8")  # 采用utf-8编码方式对手机号码进行编码
    guest_list = Guest.objects.filter(phone__contains=search_name_bytes)

    paginator = Paginator(guest_list, 10)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    return render(request, "guest_manage.html", {"user": username,
                                                 "guests": contacts})



#签到页面
@login_required()
def sign_index(request,eid):
    event= get_object_or_404(Event,id=eid) #找不到对象，抛出一个HTTP404异常,而不是模型的DoesNotExist 异常
    return render(request,'sign_index.html',{'event':event})


# 签到动作
@login_required
def sign_index_action(request,eid):

    event = get_object_or_404(Event, id=eid)
    phone = request.POST.get('phone', '')
    print(phone)

    guest_list = Guest.objects.filter(event_id=eid)
    sign_list = Guest.objects.filter(sign="1", event_id=eid)
    guest_data = str(len(guest_list))
    sign_data = str(len(sign_list))

    result = Guest.objects.filter(phone = phone)

    if not result:
        return render(request, 'sign_index.html', {'event': event,'hint': 'phone error.','guest':guest_data,'sign':sign_data})

    result = Guest.objects.filter(phone = phone,event_id = eid)
    if not result:
        return render(request, 'sign_index.html', {'event': event,'hint': 'event id or phone error.','guest':guest_data,'sign':sign_data})

    result = Guest.objects.get(event_id = eid,phone = phone)
    if result.sign:
        return render(request, 'sign_index.html', {'event': event,'hint': "user has sign in.",'guest':guest_data,'sign':sign_data})
    else:
        Guest.objects.filter(event_id = eid,phone = phone).update(sign = '1')
        return render(request, 'sign_index.html', {'event': event,'hint':'sign in success!',
            'guest': result,
            'Guest_Number':guest_data,
            'sign':str(int(sign_data)+1)
            })


#退出登录
@login_required()
def logout(request):
    auth.logout(request)
    response=HttpResponseRedirect('/index')
    return response