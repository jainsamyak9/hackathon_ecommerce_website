from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

PATMENT_CHOICES =(
    ('P','Paypal'),
    ('Pt','Paytm')
)

class CheckoutForm(forms.Form):
    address = forms.CharField(widget=forms.TextInput(attrs={
        'Class':'stext-111 cl2 plh3 size-116 p-l-30 p-r-30'    }))
    city = forms.CharField(widget=forms.TextInput(attrs={
        'Class':'stext-111 cl2 plh3 size-116  p-l-30 p-r-30'    }))
    state= forms.CharField(widget=forms.TextInput(attrs={
        'Class':'stext-111 cl2 plh3 size-116 p-l-30 p-r-30'    }))
    zip= forms.CharField(widget=forms.TextInput(attrs={
        'Class':'stext-111 cl2 plh3 size-116 p-l-30 p-r-30'    }))
    same_billing_address = forms.BooleanField(widget=forms.CheckboxInput(),required=False)
    save_info = forms.BooleanField(widget=forms.CheckboxInput(),required=False)
    payment_option= forms.ChoiceField(widget=forms.RadioSelect,choices= PATMENT_CHOICES)

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User

        email = forms.EmailField()
        fields = ['username','email','password1','password2']