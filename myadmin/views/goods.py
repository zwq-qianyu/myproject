from django.shortcuts import render
from django.http import HttpResponse

from common.models import Goods,Types
from datetime import datetime
from PIL import Image
import time,os
from django.db.models import Q
from django.core.paginator import Paginator
# Create your views here.

# 浏览商品信息
def index(request,pIndex):
    '''浏览信息'''
    #获取商品类别信息
    tlist = Types.objects.extra(select={'_has':'concat(path,id)'}).order_by('_has')
    for ob in tlist:
        ob.pname = '. . .'*(ob.path.count(',')-1)

    #获取商品信息查询对象
    mod = Goods.objects
    mywhere=[] #定义一个用于存放搜索条件列表

    # 获取、判断并封装关keyword键搜索
    kw = request.GET.get("keyword",None)
    if kw:
        # 查询商品名中只要含有关键字的都可以
        list = mod.filter(goods__contains=kw)
        mywhere.append("keyword="+kw)
    else:
        list = mod.filter()
    # 获取、判断并封装商品类别typeid搜索条件
    typeid = request.GET.get('typeid','0')
    if typeid != '0':
        tids = Types.objects.filter(Q(id=typeid) | Q(pid=typeid)).values_list('id',flat=True)
        list = list.filter(typeid__in=tids)
        mywhere.append("typeid="+typeid)
    # 获取、判断并封装商品状态state搜索条件
    state = request.GET.get('state','')
    if state != '':
        list = list.filter(state=state)
        mywhere.append("state="+state)

    #执行分页处理
    pIndex = int(pIndex)
    page = Paginator(list,5) #以5条每页创建分页对象
    maxpages = page.num_pages #最大页数
    #判断页数是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex) #当前页数据
    plist = page.page_range   #页码数列表

    #遍历商品信息，并获取对应的商品类别名称，以typename名封装
    for vo in list2:
        ty = Types.objects.get(id=vo.typeid)
        vo.typename = ty.name
    #封装信息加载模板输出
    context = {'typelist':tlist,"goodslist":list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere,'typeid':int(typeid)}
    return render(request,"myadmin/goods/index.html",context)
    

def add(request):
    '''加载添加页面'''
    #获取商品类息
    tlist = Types.objects.extra(select={'_has':'concat(path,id)'}).order_by('_has')
    for ob in tlist:
        ob.pname = '. . .'*(ob.path.count(',')-1)
    context={'typelist':tlist}
    return render(request,"myadmin/goods/add.html",context)

def insert(request):
    '''执行添加'''
    try:
        # 图片的上传处理
        myfile = request.FILES.get("pic",None)
        if not myfile:
            return HttpResponse("没有上传文件信息")
        filename = str(time.time())+"."+myfile.name.split('.').pop()
        destination = open("./static/goods/"+filename,"wb+")
        for chunk in myfile.chunks():      # 分块写入文件  
            destination.write(chunk)  
        destination.close()

        # 图片的缩放
        im = Image.open("./static/goods/"+filename)
        # 缩放到375*375(缩放后的宽高比例不变):
        im.thumbnail((375, 375)) 
        im.save("./static/goods/"+filename,None)
        
        im = Image.open("./static/goods/"+filename)
        # 缩放到220*220(缩放后的宽高比例不变):
        im.thumbnail((220,220)) 
        im.save("./static/goods/m_"+filename,None)

        im = Image.open("./static/goods/"+filename)
        # 缩放到75*75(缩放后的宽高比例不变):
        im.thumbnail((75, 75)) 
        im.save("./static/goods/s_"+filename,None)

        #保存商品信息
        ob = Goods()
        ob.goods = request.POST['goods']
        ob.typeid = request.POST['typeid']
        ob.company = request.POST['company']
        ob.price = request.POST['price']
        ob.store = request.POST['store']
        ob.content = request.POST['content']
        ob.picname = filename
        ob.state = 1
        ob.addtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context={"info":"添加成功！"}
    except Exception as err:
        print(err)
        context={"info":"添加失败"}
    return render(request,"myadmin/info.html",context)

def delete(request,gid):
    '''删除信息'''
    try:
        ob = Goods.objects.get(id=gid)
        #执行图片删除
        os.remove("./static/goods/"+ob.picname)
        os.remove("./static/goods/s_"+ob.picname)
        os.remove("./static/goods/m_"+ob.picname)
        ob.delete()
        context={"info":"删除成功！"}
    except Exception as err:
        print(err)
        context={"info":"删除失败"}
    return render(request,"myadmin/info.html",context)


def edit(request,gid):
    '''加载编辑信息页面'''
    try:
        tlist = Types.objects.extra(select={'_has':'concat(path,id)'}).order_by('_has')
        for ob in tlist:
            ob.pname = '. . .'*(ob.path.count(',')-1)
        ob = Goods.objects.get(id=gid)
        context={"goods":ob,'typelist':tlist}   #同时传两个参数时，放在一个字典中传过去
        return render(request,"myadmin/goods/edit.html",context)
    except Exception as err:
        context={"info":"没有找到要修改的信息！"}
        return render(request,"myadmin/info.html",context)

def update(request,gid):
    '''执行编辑信息'''
    try:
        # 图片的上传处理
        myfile = request.FILES.get("pic",None)
        if not myfile:
            return HttpResponse("没有上传文件信息")
        filename = str(time.time())+"."+myfile.name.split('.').pop()
        destination = open("./static/goods/"+filename,"wb+")
        for chunk in myfile.chunks():      # 分块写入文件  
            destination.write(chunk)  
        destination.close()

        # 图片的缩放
        im = Image.open("./static/goods/"+filename)
        # 缩放到375*375(缩放后的宽高比例不变):
        im.thumbnail((375, 375)) 
        im.save("./static/goods/"+filename,None)
        
        im = Image.open("./static/goods/"+filename)
        # 缩放到220*220(缩放后的宽高比例不变):
        im.thumbnail((220,220)) 
        im.save("./static/goods/m_"+filename,None)

        im = Image.open("./static/goods/"+filename)
        # 缩放到75*75(缩放后的宽高比例不变):
        im.thumbnail((75, 75)) 
        im.save("./static/goods/s_"+filename,None)

        
        ob = Goods.objects.get(id=gid)
        old_picname = request.POST['old_picname']
        #删除原来的旧的图片
        os.remove("./static/goods/"+old_picname)
        os.remove("./static/goods/s_"+old_picname)
        os.remove("./static/goods/m_"+old_picname)
        ob.goods = request.POST['goods']
        ob.typeid = request.POST['typeid']
        ob.company = request.POST['company']
        ob.price = request.POST['price']
        ob.store = request.POST['store']
        ob.content = request.POST['content']
        ob.picname = filename
        ob.state = request.POST['state']
        ob.save()
        context={"info":"修改成功！"}
    except Exception as err:
        print(err)
        context={"info":"修改失败"}
    return render(request,"myadmin/info.html",context)
