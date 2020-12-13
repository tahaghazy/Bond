from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from author.decorators import with_author
from django.urls import reverse
import uuid
# Create your models here.


from django.contrib.admin.models import ADDITION, LogEntry


class Shop(models.Model):
    title = models.CharField(max_length=10000, verbose_name='اسم المحل')
    num = models.CharField(default="",max_length=1000, verbose_name='رقم جهاز مدى 1')
    num2 = models.CharField(default="",max_length=1000, verbose_name='رقم جهاز مدى 2')
    mobile = models.CharField(max_length=1000, verbose_name='رقم الهاتف')
    author = models.CharField(max_length=1000, verbose_name='المسؤول عن القبض  ')

    def __str__(self):
        a = str(self.title)+' رقم جهاز 1 '+'('+str(self.num)+')'+' رقم جهاز 2 '+'('+str(self.num2)+')'
        return a

    class Meta:
        ordering = ('-id',)
        verbose_name = ('محل')
        verbose_name_plural = ('المحلات')







@with_author
class Bond(models.Model):
    shop = models.ForeignKey(Shop,on_delete=models.CASCADE,unique=False,related_name='posts', verbose_name='المحل')
    operation_number = models.CharField(max_length=10000, unique=False,error_messages ={ "unique":"عزيزي الموظف رقم العمليه مكرر يرجى مراجعة البحث وشكرا."} ,verbose_name='رقم العمليه')
    deserved_amount = models.FloatField(default=0,verbose_name='المبلغ المستحق')
    paid_amount = models.FloatField(default=0,null=True,blank=True,verbose_name='المبلغ المدفوع')
    residual = models.FloatField(default=0,null=True,blank=True,verbose_name='المبلغ المتبقي')
    discount = models.FloatField(default=0,null=True,blank=True,verbose_name='الخصم')
    numa = models.CharField(max_length=10000,default="-",null=True,blank=True,verbose_name='رقم فاتورة المبيعات')
    nume = models.CharField(max_length=10000,default="-",null=True,blank=True,verbose_name='مبلغ فاتورة المبيعات')
    bond_date = models.DateTimeField(auto_now=True, verbose_name='تاريخ القبض')
    peration_date = models.DateField(default=timezone.now, verbose_name='تاريخ العمليه')
    content = models.TextField(null=True, blank=True,verbose_name='ملاحظات')
    author = models.ForeignKey(User,on_delete=models.PROTECT,null=True,blank=True,editable=False,verbose_name='الموظف الذي قام باالادخال')
    updated_by =  models.ForeignKey(User,on_delete=models.PROTECT,related_name='last',null=True,blank=True,editable=False,verbose_name='المعتمد للدفع ')
    active = models.BooleanField(default=True,verbose_name='باقي مدفوعات')
    isactive = models.BooleanField(default=False,verbose_name=' تم الدفع')
    rr = models.BooleanField(default=False,editable=False)

    def save(self, *args, **kwargs):
        if self.rr == False:
            self.deserved_amount = self.deserved_amount - self.discount
            self.residual = self.deserved_amount - self.paid_amount

            self.rr = True

        if self.active == False and self.isactive == True and self.residual == 0 and self.rr ==True:
            self.paid_amount = self.deserved_amount
        if self.active == True and self.isactive == False and self.paid_amount == 0and self.rr ==True:
            self.residual = self.deserved_amount - self.paid_amount
        super(Bond, self).save(*args, **kwargs)


    @property
    def ctc(self):
        return self.deserved_amount + self.discount
    def __str__(self):
        a = "سند رقم  " +str(self.id)
        return a
    def ad(self):
        ae = str(self.residual)
        return ae





    class Meta:
        unique_together = [['shop','operation_number']]
        ordering = ('-bond_date',)
        verbose_name = ('سند')
        verbose_name_plural = ('السندات')



class Cc(models.Model):
    HISTORY_ACTION_SYSTEM = 'chat'

    shop = models.ForeignKey(Shop,on_delete=models.CASCADE,related_name='poss', verbose_name='المحل')
    from1 = models.DateField(default=timezone.now, verbose_name='من')
    to = models.DateField(default=timezone.now, verbose_name='الي')

    def __str__(self):
        a = str(self.shop.title)

        return a
    class Meta:
        ordering = ('-to',)
        verbose_name = ('كشف')
        verbose_name_plural = ('الكشوفات')






