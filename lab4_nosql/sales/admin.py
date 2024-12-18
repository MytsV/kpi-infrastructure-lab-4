from django.contrib import admin
from .models import Salesperson


class SalespersonAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'age', 'gender', 'phone_number', 'date_joined', 'picture_tag')
    search_fields = ('full_name', 'code')
    list_filter = ('gender',)


admin.site.register(Salesperson, SalespersonAdmin)
