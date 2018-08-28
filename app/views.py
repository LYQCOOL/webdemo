from django.shortcuts import render, HttpResponse, redirect
from app import models
from django import forms
from django.forms import fields
from django.forms import widgets
from django.core.validators import RegexValidator
from io import BytesIO
from utils.check_code import create_validate_code
import json
import re
import datetime


class User(forms.Form):
    username = fields.CharField(error_messages={'required': '用户名不能为空'},
                                widget=widgets.Input(attrs={'type': "text", 'class': "form-control", 'name': "username",
                                                            'id': "username", 'placeholder': "请输入用户名"}))
    password = fields.CharField(error_messages={'required': '密码不能为空.'},
                                widget=widgets.Input(
                                    attrs={'type': "password", 'class': "form-control", 'name': "password",
                                           'id': "password",
                                           'placeholder': "请输入密码"})
                                )


class Newuser(forms.Form):
    username = fields.CharField(max_length=12, min_length=3,
                                error_messages={'required': '用户名不能为空', 'max_length': '用户名长度不能12',
                                                'min_length': '用户名长度不能小于3'},
                                widget=widgets.Input(attrs={'type': "text", 'class': "form-control", 'name': "username",
                                                            'id': "username", 'placeholder': "请输入用户名"}))
    realname = fields.CharField(validators=[RegexValidator(r'^[\u4e00-\u9fa5 ]{2,4}$', '名字格式不正确！！中国人哈应在两到四个汉字之间！'), ],
                                error_messages={'required': '姓名不能为空', 'invalid': '姓名格式不正确.'}, widget=widgets.Input(
            attrs={'type': "text", 'class': "form-control", 'name': "realname", 'id': "realname",
                   'placeholder': "请输入真实姓名"}))
    password = fields.CharField(max_length=12, min_length=6,
                                error_messages={'required': '密码不能为空.', 'max_length': '密码长度不能大于12',
                                                'min_length': '密码长度不能小于6'},
                                widget=widgets.Input(
                                    attrs={'type': "password", 'class': "form-control", 'name': "password",
                                           'id': "password",
                                           'placeholder': "请输入密码"})
                                )
    confirm_password = fields.CharField(max_length=12, min_length=6,
                                        error_messages={'required': '不能为空.', 'max_length': '两次密码不一致',
                                                        'min_length': '两次密码不一致'},
                                        widget=widgets.Input(
                                            attrs={'type': "password", 'class': "form-control",
                                                   'name': "confirm_password",
                                                   'id': "confirm_password",
                                                   'placeholder': "请重新输入密码"})
                                        )


def check_code(request):
    """
    验证码
    :param request:
    :return:
    """
    stream = BytesIO()
    img, code = create_validate_code()
    img.save(stream, 'PNG')
    request.session['CheckCode'] = code
    return HttpResponse(stream.getvalue())


def login(request):
    """
    登陆
    :param request:
    :return:
    """
    # if request.method == "POST":
    #     if request.session['CheckCode'].upper() == request.POST.get('check_code').upper():
    #         pass
    #     else:
    #         print('验证码错误')
    er = ''
    s = ''
    if request.method == 'GET':
        obj = User()
        return render(request, 'login.html', {'obj': obj})
    if request.method == 'POST':
        obj = User(request.POST)
        code = request.POST.get('check_code')
        auto = request.POST.get('auto')
        if auto:
            request.session.set_expiry(2419200)
        else:
            pass
        if code.upper() == request.session['CheckCode'].upper():
            u = request.POST.get('username')
            t1 = models.User.objects.filter(username=u)
            if t1:
                pwd = request.POST.get('password')
                if pwd == t1[0].pwd:
                    request.session['user'] = u
                    request.session['is_login'] = True
                    request.session['pwd'] = pwd
                    f = request.session.get('is_login', None)
                    return redirect('/index-0/')
                else:
                    s = '''
                  <script>alert('密码错误!!!请重新输入!!!');</script>
                  '''
            else:
                s = '''
           <script>alert('该用户名不存在!!!请检查是否正确!!!');</script>
                                '''

        else:
            er = '验证码错误'
        return render(request, 'login.html', {'obj': obj, 'er': er, 's': s})


def register(request):
    """
    注册
    :param request:
    :return:
    """
    er = ''
    if request.method == 'GET':
        obj = Newuser()
        return render(request, 'register.html', {'obj': obj, 'er': er})
    if request.method == 'POST':
        try:
            obj = Newuser(request.POST)
            r = obj.is_valid()
            if r:
                code = request.POST.get('check_code')
                if code.upper() == request.session['CheckCode'].upper():
                    user = request.POST.get('username')
                    realname = request.POST.get('realname')
                    u = models.User.objects.filter(username=user)
                    if u:
                        s = '''
                    <script>alert('用户名已经存在，请从新输入用户名！');
                </script>
                    '''
                    else:
                        pwd1 = request.POST.get('password')
                        pwd2 = request.POST.get('confirm_password')
                        if pwd1 != pwd2:
                            s = '''
                        <script>alert('两次密码不一致，请核对重新输入！');</script>'''
                        else:
                            models.User.objects.create(username=user, pwd=pwd1, realname=realname)
                            s = '''
                        <script>alert('注册成功！');
                        </script>'''
                    return render(request, 'register.html', {'obj': obj, 'er': er, 's': s})
                else:
                    er = '验证码错误'
                    return render(request, 'register.html', {'obj': obj, 'er': er})

            else:
                s = '''
            <script>alert('信息格式不正确,注册失败！');
                </script>'''
                return render(request, 'register.html', {'obj': obj, 'er': er, 's': s})
        except:
            s = '''
           <script>alert('意外出错！！！！');</script>'''
            obj = Newuser()
            return render(request, 'register.html', {'s': s, 'obj': obj})


def goods(request):
    good_list = models.Goods.objects.all();
    return render(request, 'shangpin.html', {'goods': good_list, })


# Create your views here.
def index(request, nid):
    f = request.session.get('is_login', None)
    u = request.session.get('user', None)
    if u:
        u_id = models.User.objects.filter(username=u).first().id
    else:
        u_id = None
    if request.method == 'GET':
        style = models.Style.objects.all()
        if nid == '0':
            good_list = models.Goods.objects.all()
        else:
            good_list = models.Goods.objects.filter(shangpinleixing_id=nid)
        return render(request, 'shangpin.html', {'goods': good_list, 'style': style, 'f': f, 'u': u})
    elif request.method == 'POST':
        ret = {'data': None, 'status': True, 'error': None}
        if f:
            number = request.POST.get('number')
            w_id = request.POST.get('w_id')
            # print(u_id,w_id,number)
            models.Shoppingcar.objects.create(goods_id=w_id, user_id=u_id, number=number)
            return HttpResponse(json.dumps(ret))
        else:
            ret['status'] = False
            return HttpResponse(json.dumps(ret))


def shoppingcar(request):
    f = request.session.get('is_login', None)
    ret = {'data': None, 'status': True, 'error': None}
    if f:
        number = request.POST.get('number')
        return HttpResponse(json.dumps(ret))
    else:
        ret['status'] = False
        number = request.POST.get('number')
        return HttpResponse(json.dumps(ret))


def shopcar(request):
    f = request.session.get('is_login', None)
    u = request.session.get('user', None)
    if f:
        if request.method == 'GET':
            id = models.User.objects.filter(username=u)[0].id
            obj = models.Shoppingcar.objects.filter(user_id=id)
            if obj:
                error = ''
            else:
                error = '您的购物车还为空！！赶快去商城购买吧！！！'
            return render(request, 'shopcar.html', {'obj': obj, 'u': u, 'f': f, 'error': error})
        elif request.method == 'POST':
            s_id = request.POST.get('id_1')
            print(s_id)
            models.Shoppingcar.objects.filter(id=s_id).delete()
            id = models.User.objects.filter(username=u)[0].id
            obj = models.Shoppingcar.objects.filter(user_id=id)
            if obj:
                error = ''
            else:
                error = '您的购物车还为空！！赶快去商城购买吧！！！'
            return render(request, 'shopcar.html', {'obj': obj, 'u': u, 'f': f, 'error': error})


def logout(request):
    request.session.clear()
    f = request.session.get('is_login', None)
    u = request.session.get('user', None)
    style = models.Style.objects.all()
    good_list = models.Goods.objects.all()
    return render(request, 'shangpin.html', {'goods': good_list, 'style': style, 'f': f, 'u': u})
    return render(request, 'shangpin.html', {'f': f})


def sousuo(request):
    ret = {'status': True, 'data': None, 'error': None}
    good_list = []
    style = models.Style.objects.all()
    content = request.POST.get('content')
    print(content)
    if content:
        obj = models.Goods.objects.all()
        a = re.compile(content, re.X)
        for row in obj:
            if a.match(row.shangpinmingchen):
                print(row.shangpinmingchen)
                good_list.append(row.id)
        if good_list:
            ret['data'] = good_list
            return HttpResponse(json.dumps(ret))
            # return redirect('/login/')
        else:
            ret['status'] = False
            ret['error'] = '未搜索到相关内容！！！'
            return HttpResponse(json.dumps(ret))

    else:
        ret['status'] = False
        ret['error'] = '搜索内容不能为空！！！'
        return HttpResponse(json.dumps(ret))


def sousuo_index(request):
    good_list = request.POST.get('data')
    style = models.Style.objects.all()
    print(111)
    # return HttpResponse('HEllo')
    return render(request, 'sousuo.html', {'goods': good_list, 'style': style})


def information(request):
    '''基本信息修改'''
    f = request.session.get('is_login', None)
    u = request.session.get('user', None)
    error = ''
    if f:
        if request.method == 'GET':
            obj = models.User.objects.filter(username=u).first()
            return render(request, 'information.html', {'obj': obj, 'error': error, 'f': f, 'u': u})
        elif request.method == 'POST':
            id = request.POST.get('u-id')
            u2 = request.POST.get('u-name')
            r2 = request.POST.get('r-name')
            r = models.User.objects.filter(id=id)[0].realname
            if u2 and r2:
                if u2 == u and r2 == r:
                    error = '信息与原来相同！！！'
                    obj = models.User.objects.filter(id=id).first()
                    return render(request, 'information.html', {'obj': obj, 'error': error, 'f': f, 'u': u})
                else:
                    error = '修改成功！！！请从新登录！！！'
                    models.User.objects.filter(id=id).update(username=u2, realname=r2)
                    obj = models.User.objects.filter(id=id).first()
                return render(request, 'information.html', {'obj': obj, 'error': error, 'f': f, 'u': u})

            else:
                error = '信息均不能为空！！！！'
                obj = models.User.objects.filter(id=id).first()
                return render(request, 'information.html', {'obj': obj, 'error': error, 'f': f, 'u': u})
    else:
        obj = User()
        return render(request, 'login.html', {'obj': obj})


def pwd(request):
    f = request.session.get('is_login', None)
    u = request.session.get('user', None)
    id = models.User.objects.filter(username=u).first().id
    error = ''
    if f:
        if request.method == 'GET':
            return render(request, 'pwd.html', {'error': error, 'f': f, 'u': u})
        elif request.method == 'POST':

            o_pwd = request.POST.get('o_pwd')
            new1 = request.POST.get('new1')
            new2 = request.POST.get('new2')
            pwd = models.User.objects.filter(id=id)[0].pwd
            print(o_pwd, new1, new2, pwd)
            if o_pwd == pwd:
                if len(new1) <= 12 and len(new1) >= 6:
                    if o_pwd != new1:
                        if new1 == new2:
                            models.User.objects.filter(id=id).update(pwd=new1)
                            error = '修改成功！！请从新登录！！！'
                            return render(request, 'pwd.html', {'error': error, 'f': f, 'u': u})
                        else:
                            error = '两次密码不一致，请从新输入！！！'
                            return render(request, 'pwd.html', {'error': error, 'f': f, 'u': u})
                    else:
                        error = '新密码和原来相同！！！'
                        return render(request, 'pwd.html', {'error': error, 'f': f, 'u': u})
                else:
                    error = '密码长度应大于6，小于12！！！！'
                    return render(request, 'pwd.html', {'error': error, 'f': f, 'u': u})
            else:
                error = '原密码不正确，请从新输入！！！'
                return render(request, 'pwd.html', {'error': error, 'f': f, 'u': u})
    else:
        obj = User()
        return render(request, 'login.html', {'obj': obj})


def clean(request):
    u = request.session.get('user', None)
    id = models.User.objects.filter(username=u)[0].id
    ret = {'status': True, 'data': None, 'error': None}
    models.Shoppingcar.objects.filter(user_id=id).delete()
    return HttpResponse(json.dumps(ret))


def order(request):
    f = request.session.get('is_login', None)
    u = request.session.get('user', None)
    if f:
        id = models.User.objects.filter(username=u)[0].id
        if request.method == 'GET':
            orders = models.Order.objects.all()
            return render(request, 'order.html', {'u': u, 'f': f, 'orders': orders})
        elif request.method == 'POST':
            ret = {'status': True, 'error': None, 'data': None}
            u_id = request.POST.get('id')
            obj1 = models.Shoppingcar.objects.filter(user_id=u_id)
            if obj1:
                time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                for row in obj1:
                    models.Order.objects.create(status=0, date=time, goods_id=row.goods_id, user_id=row.user_id,
                                                number=row.number)
                return HttpResponse(json.dumps(ret))
            else:
                ret['status'] = False
                ret['error'] = '购买失败！！！'
                return HttpResponse(json.dumps(ret))


    else:
        obj = Newuser()
        return render(request, 'login.html', {'obj': obj})


def goumai(request):
    u = request.session.get('user', None)
    f = request.session.get('is_login', None)
    if f:
        ret = {'status': True, 'data': None, 'error': None}
        id = request.POST.get('id')
        number = request.POST.get('nu')
        print(number)
        if id:
            u_id = models.User.objects.filter(username=u)[0].id
            time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            models.Order.objects.create(status=0, date=time, goods_id=id, user_id=u_id, number=number)
            return HttpResponse(json.dumps(ret))
        else:
            ret['status'] = False
            ret['error'] = '购买失败！！'
            return HttpResponse(json.dumps(ret))
