from django import forms

class DogForm(forms.Form):
    name = forms.CharField(max_length=100)
    breed = forms.CharField(max_length=100)
    age = forms.IntegerField()
    is_friendly = forms.BooleanField(required=False)

class UserForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.CharField(max_length=200)
    groups = forms.CharField(max_length=255, required=False)