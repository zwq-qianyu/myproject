from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator

from common.models import Users,Types,Goods,Orders,Detail

# 公共信息加载函数
def loadinfo(request):
    lists = Types.objects.filter(pid=0)
    context = {'typelist':lists}
    return context

def  viporders(request):
    '''浏览订单信息'''
    context = loadinfo(request)
    #获取当前登录者的订单信息
    odlist = Orders.objects.filter(uid=request.session['vipuser']['id'])
    #遍历订单信息，查询对应的详情信息
    for od in odlist:
        delist = Detail.objects.filter(orderid=od.id)
        #遍历订单详情，并且获取对应的商品信息（图片）
        for og in delist:
            og.picname = Goods.objects.only("picname").get(id=og.goodsid).picname
        od.detaillist = delist

    context['orderslist'] = odlist
    return render(request,"web/viporders.html",context)

def odstate(request):
    ''' 修改订单状态 '''
    try:
        oid = request.GET.get("oid",'0')
        ob = Orders.objects.get(id=oid)
        ob.state = request.GET['state']
        ob.save()
        return redirect(reverse('vip_orders'))
    except Exception as err:
        print(err)
        return HttpResponse("订单处理失败！")

def info(request):
    '''加载编辑信息页面'''
    try:
        ob = Users.objects.get(id=request.session['vipuser']['id'])
        context={"vip":ob}
        print("id: "+ str(ob.id))
        return render(request,"web/vip/info.html",context)
    except Exception as err:
        print(err)
        context={"info":"没有找到信息！"}
        return render(request,"web/info.html",context)

def edit(request):
    '''加载编辑信息页面'''
    try:
        ob = Users.objects.get(id=request.session['vipuser']['id'])
        context={"vip":ob}
        print("id: "+ str(ob.id))
        return render(request,"web/vip/edit.html",context)
    except Exception as err:
        print(err)
        context={"info":"没有找到要修改的信息！"}
        return render(request,"web/info.html",context)

def update(request):
    '''执行编辑信息'''
    try:
        ob = Users.objects.get(id=request.session['vipuser']['id'])
        ob.name = request.POST['name']
        ob.sex = request.POST['sex']
        ob.address = request.POST['address']
        ob.code = request.POST['code']
        ob.phone = request.POST['phone']
        ob.email = request.POST['email']
        ob.state = 1
        ob.save()
        context={"info":"修改成功！"}
    except Exception as err:
        print(err)
        context={"info":"修改失败"}
    return render(request,"web/info.html",context)

def resetpass(request):
    '''加载重置会员密码信息页面'''
    try:
        ob = Users.objects.get(id=request.session['vipuser']['id'])
        context={"vip":ob}
        return render(request,"web/vip/resetpass.html",context)
    except Exception as err:
        context={"info":"没有找到要修改的信息！"}
        return render(request,"web/info.html",context)

def doresetpass(request):
    '''执行编辑信息'''
    try:
        ob = Users.objects.get(id=request.session['vipuser']['id'])
        #获取密码并md5
        import hashlib
        m = hashlib.md5() 
        m.update(bytes(request.POST['password'],encoding="utf8"))
        ob.password = m.hexdigest()
        ob.save()
        #context={"info":"密码重置成功！"}
        return render(request,"web/login.html")
    except Exception as err:
        print(err)
        context={"info":"密码重置失败"}
        return render(request,"web/info.html",context)