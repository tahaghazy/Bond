from django.contrib import admin
from .models import *
# Register your models here.from
from admin_auto_filters.filters import AutocompleteFilter
from django.contrib.admin.actions import delete_selected
from django.contrib.auth import get_permission_codename
from admin_totals.admin import ModelAdminTotals

from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter
from django.db.models import Sum

from admin_totals.admin import ModelAdminTotals
from django.contrib import admin
from django.db.models import Sum, Avg
from import_export.admin import *




class ArtistFilter(AutocompleteFilter):
    title = 'المحل'  # display title
    field_name = 'shop'  # name of the foreign key field



class Pos(admin.ModelAdmin):

    list_display = [
        'title',
        'num',
        'num2',
        'mobile',
        'author'

    ]
    search_fields = ['title','num2', 'num', 'mobile', 'author']



class PostImportExport(ModelAdminTotals):

    def has_change_permission(self, request, obj=Bond):
        if obj is not None and obj.author != request.user:
            if request.user.is_superuser:
                return True
            else:
                return False


        return True

    def has_delete_permission(self, request, obj=Bond):
        if obj is not None and obj.author != request.user:
            if request.user.is_superuser:
                return True
            else:
                return False

        return True



    list_display = [
        'operation_number',
        'id',
        'shop',
        'author',
        'deserved_amount',
        'paid_amount',
        'residual',
        'discount',
        'bond_date',
        'peration_date',
        'content',
        'active',
        'isactive',
        "updated_by"

    ]
    list_filter = [ArtistFilter,('peration_date', DateRangeFilter), 'bond_date',
                   'active']
    search_fields = ['from2', 'to', 'operation_number', 'shop__title', 'author__username', 'active', 'deserved_amount',
                     'paid_amount',
                     'residual', ]
    autocomplete_fields = ['shop']
    list_totals = [ ('paid_amount', Sum),('deserved_amount', Sum),('residual', Sum),('discount', Sum)]




    def make_refund_accepted(self, request, object):
        object.update(active=False,isactive=True,residual=0)
        for b in Bond.objects.all():
            b.save()




    def make_refund_accepte(self, request, object):
        object.update(active=True,isactive=False,paid_amount=0)
        for b in Bond.objects.all():
            b.save()




    def make_refund_accept(self, request, queryset):

        queryset.delete()


    



    make_refund_accepted.short_description = 'لم يتبقي عليه مدفوعات'
    make_refund_accepte.short_description = 'باقي مدفوعات'
    make_refund_accept.short_description = 'حذف '





    actions = [make_refund_accept, make_refund_accepted, make_refund_accepte]

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_total(self):
        # functions to calculate whatever you want...
        total = Bond.objects.all().aggregate(tot=Sum('discount'))['tot']
        return total

    class Media:
        pass


class Cv(admin.ModelAdmin):
    list_display = [
        'shop',
        'from1',
        'to'

    ]
    autocomplete_fields = ['shop']

    list_filter = ['shop', 'from1', 'to']


admin.site.register(Shop, Pos)
admin.site.register(Bond, PostImportExport)
admin.site.register(Cc, Cv)

admin.site.site_header = 'مدخل الموظفين'
admin.site.site_title = 'شركة هاني حسن رضي ابو عبدالله وشركاه'
admin.site.index_title = 'شركة هاني حسن رضي ابو عبدالله وشركاه'
admin.site.site_url = "/disclosures"


class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_string', 'action_time', 'user', 'action_flag', 'object_repr',)
    list_filter = ['action_time', 'user__username', 'action_flag']

    actions = None

    def get_string(self, obj):
        return str(obj)

    search_fields = ['=user__username', ]
    fieldsets = [
        (None, {'fields': ()}),
    ]

    def __init__(self, *args, **kwargs):
        super(LogEntryAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = None


admin.site.register(admin.models.LogEntry, LogEntryAdmin)























