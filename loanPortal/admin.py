from django.contrib import admin
from .models import User, Loan, UserLoan
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'role', 'mobile')


class LoanAdmin(admin.ModelAdmin):
    list_display = ('name', 'interest')


class UserLoanAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'principle', 'loan_type')


admin.site.register(User, UserAdmin)
admin.site.register(UserLoan, UserLoanAdmin)
admin.site.register(Loan, LoanAdmin)







