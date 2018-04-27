from django.conf.urls import url

from web.views import index,cart,orders,vip

urlpatterns = [
    # 前台首页
    url(r'^$', index.index, name="index"),	#商城首页
    url(r'^list$', index.lists, name="list"),# 商品列表
    url(r'^list/(?P<pIndex>[0-9]+)$', index.lists, name="list"),# 商品列表
    url(r'^detail/(?P<gid>[0-9]+)$', index.detail, name="detail"), # 商品详情

    # 会员登录和退出路由配置
    url(r'^login$', index.login, name="login"),
    url(r'^dologin$', index.dologin, name="dologin"),
    url(r'^logout$', index.logout, name="logout"),

    # 会员注册路由
    url(r'^register$', index.register, name="register"),
    url(r'^insert$', index.insert, name="insert"),

    # 购物车信息管理路由配置
    url(r'^cart$', cart.index, name="cart_index"),
    url(r'^cart/add/(?P<gid>[0-9]+)$', cart.add, name="cart_add"),
    url(r'^cart/del/(?P<gid>[0-9]+)$', cart.delete, name="cart_del"),
    url(r'^cart/clear$', cart.clear, name="cart_clear"),
    url(r'^cart/change$', cart.change, name="cart_change"),

    # 订单处理
    url(r'^orders/add$', orders.add,name='orders_add'), #订单的表单页
    url(r'^orders/confirm$', orders.confirm,name='orders_confirm'), #订单确认页
    url(r'^orders/insert$', orders.insert,name='orders_insert'), #执行订单添加操作

    # 会员中心
    url(r'^vip/orders$', vip.viporders,name='vip_orders'), #会员中心我的订单
    url(r'^vip/odstate$', vip.odstate,name='vip_odstate'), #修改订单状态（确认收货）
    url(r'^vip/info$', vip.info,name='vip_info'), #会员中心的个人信息
    url(r'^vip/edit$', vip.edit,name='vip_edit'), #加载修改消息表单
    url(r'^vip/update$', vip.update,name='vip_update'), #执行修改会员信息
    url(r'^vip/resetpass$', vip.resetpass,name='vip_resetpass'), #重置密码表单
    url(r'^vip/doresetpass$', vip.doresetpass,name='vip_doresetpass'), #执行重置密码
]
