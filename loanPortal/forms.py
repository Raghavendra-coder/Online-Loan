from django import forms
from .models import User, UserLoan
from django.db.models import Q
from django.contrib.auth import authenticate


class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password', 'profile_pic', 'mobile', 'address', 'city', 'state', 'zip')
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'zip': forms.TextInput(attrs={'class': 'form-control'})
        }


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        username_text = self.cleaned_data['username']
        password = self.cleaned_data['password']

        user_name = User.objects.filter(Q(username=username_text)).first()
        if user_name:
            username = user_name.username
        else:
            raise forms.ValidationError("No user with this username or mobile.")
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Username/password is incorrect")


class UpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password', 'profile_pic', 'mobile', 'address', 'city', 'state', 'zip')
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'zip': forms.TextInput(attrs={'class': 'form-control'})
        }


class LoanForm(forms.ModelForm):
    class Meta:
        model = UserLoan
        fields = ('principle', 'loan_type', 'tenure', 'emi')
        widgets = {
            'principle': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'in ₹'}),
            'loan_type': forms.Select(attrs={'class': 'form-control'}),
            'tenure': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'in months'}),
            'emi': forms.NumberInput(attrs={'class': 'form-control'}),
        }
