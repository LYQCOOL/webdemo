from django.db import models


# Create your models here.
class User(models.Model):
    '''
    用户信息表
    '''
    username = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)
    realname = models.CharField(max_length=32)


class Style(models.Model):
    name = models.CharField(max_length=32)


class Goods(models.Model):
    '''
    商品信息表
    '''
    shangpintupian = models.CharField(max_length=32)
    shangpinmingchen = models.CharField(max_length=50)
    pub_date = models.DateTimeField('date published')
    shangpinleixing = models.ForeignKey(Style, on_delete=True)
    shangpinjiage = models.CharField(max_length=5000)
    shangpinshuoming = models.CharField(max_length=5000)
    lianxidianhua = models.CharField(max_length=5000)


class Shoppingcar(models.Model):
    '''
    购物车表
    '''
    user = models.ForeignKey('User', on_delete=True)
    goods = models.ForeignKey('Goods', on_delete=True)
    number = models.CharField(max_length=32)


# 订单的三种状态
choice = ((0, '已付款'), (1, '待付款'), (2, '待评价'))


class Order(models.Model):
    '''
    订单表
    '''
    user = models.ForeignKey('User', on_delete=True)
    goods = models.ForeignKey('Goods', on_delete=True)
    status = models.IntegerField(choices=choice)
    date = models.DateTimeField()
    number = models.IntegerField(default=1)
