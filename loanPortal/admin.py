from django.contrib import admin
from .models import User, Loan, UserLoan, Profile, AccuracyTable
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'role', 'mobile')


class LoanAdmin(admin.ModelAdmin):
    list_display = ('name', 'interest')


class UserLoanAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'principle', 'loan_type')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'education', 'income')


class AccuracyTableAdmin(admin.ModelAdmin):
    list_display = ('accuracy', 'created_on')


admin.site.register(User, UserAdmin)
admin.site.register(UserLoan, UserLoanAdmin)
admin.site.register(Loan, LoanAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(AccuracyTable, AccuracyTableAdmin)







