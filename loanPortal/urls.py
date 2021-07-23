from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("user_login/", views.user_login, name="user_login"),
    path("user_signup/", views.user_signup, name="user_signup"),
    path("home/", views.home, name="home"),
    path("user_logout/", views.user_logout, name="user_logout"),
    path("update_profile/", views.update_profile, name="update_profile"),
    path("loan_form/", views.loan_form, name="loan_form"),
    path("request_loan/", views.request_loan, name="request_loan"),
    path("loan_status/<pk>", views.loan_status, name="loan_status"),
    path("requested_loan/", views.requested_loan, name="requested_loan"),
    path("approve_loan/<pk>", views.approve_loan, name="approve_loan"),
    path("reject_loan/<pk>", views.reject_loan, name="reject_loan"),
    path("my_loan/", views.my_loan, name="my_loan"),
    path("list_user/", views.list_user, name="list_user"),
    path("remove_user/<pk>", views.remove_user, name="remove_user"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("calculate_emi/", views.calculate_emi, name="calculate_emi"),
    path("cong/", views.cong, name="cong"),
]
