from django.contrib import admin
from .models import Profile
from .models import TransactionHistory
from .models import Code, BotErrors
# from .models import MultiReferral
# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'risk_profile', 'wallet', 'last_modified', 'date_activated', 'run_flag', 'profit_value')


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'TransactionID', 'amount', 'TransactionCreated', 'status')


class CodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'number')


class ErrorsAdmin(admin.ModelAdmin):
    list_display = ('user', 'Error')


# class MultiReferralAdmin(admin.ModelAdmin):
#     list_display = ('user', 'parent2', 'parent3', 'parent4', 'parent5')


admin.site.register(Profile, ProfileAdmin)
admin.site.register(TransactionHistory, TransactionAdmin)
admin.site.register(Code, CodeAdmin)
admin.site.register(BotErrors, ErrorsAdmin)
# admin.site.register(MultiReferral, MultiReferralAdmin)
