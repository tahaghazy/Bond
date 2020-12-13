from django.shortcuts import render
from .models import *
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/login')
def home(request):
    shop = Cc.objects.all()
    return render(request,'home.html',context={'shop':shop})
from django.db.models import F

@login_required(login_url='/login')
def detail(request,post_id):
    shops = Shop.objects.all()
    rery = get_object_or_404(Cc,pk=post_id)
    
    bond = rery.shop.posts.filter(peration_date=rery.from1)
    shop = rery.shop


    totaldis = 0
    totald = 0
    totalp = 0
    for x in bond:
        totaldis += x.discount
    for xx in bond:
        totald += xx.residual
    for xxx in bond:
        totalp += xxx.paid_amount
    total = totald+totalp




    context = {'shop': shop,
                'shops': shops,
                'bond': bond,
               'totaldis':totaldis,
               'totald': totald,
               'totalp': totalp,
               'rery':rery,
               'total':total
               }
    return render(request,'detail.html',context)
from django.db.models import Q

def searchposts(request):
    if request.method == 'GET':
        query= request.GET.get('q')

        submitbutton= request.GET.get('submit')

        if query is not None:
            lookups= Q(operation_number__icontains=query)

            results= Bond.objects.filter(lookups).distinct()

            context={'results': results,
                     'submitbutton': submitbutton}

            return render(request, 'search.html', context)

        else:
            return render(request, 'search.html')

    else:
        return render(request, 'search.html')


def detai(request,post_id):
    rery = get_object_or_404(Bond,pk=post_id)
    re = float(rery.deserved_amount - rery.paid_amount - rery.discount)
    Bond.objects.filter(pk=rery.id).update(residual= re)

    

    return render(request,'o.html',context={'i':rery})

