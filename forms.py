from django import forms
from core.models import ProductReview
from core.models import Staff
from django.contrib.auth.models import User

class ProductReviewForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={'placeholder': "Write review"}))
    
    class Meta:
        model= ProductReview
        fields = ['review','Rating']


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['ID_card', 'Started', 'Birthday', 'Position']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']