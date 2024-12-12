from django import forms
from django.contrib.auth.models import User
from .models import Group

class SignupForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    group = forms.ModelChoiceField(queryset=Group.objects.all(), empty_label="Select your location")

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['confirm_password']:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class AnnouncementForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea, label="Create Announcement")


class ServiceRequestForm(forms.Form):
    service_name = forms.CharField(max_length=100, label="Service Name")
    description = forms.CharField(widget=forms.Textarea, label="Description")

class ProductAnnouncementForm(forms.Form):
    product_name = forms.CharField(max_length=100, label="Product Name")
    description = forms.CharField(widget=forms.Textarea, label="Description")
    price = forms.DecimalField(max_digits=10, decimal_places=2, label="Price")
    image = forms.ImageField(label="Upload Image", required=False)


class BusinessAdvertisementForm(forms.Form):
    service_name = forms.CharField(max_length=100, label="Service Name")
    provider_name = forms.CharField(max_length=100, label="Service Provider Name")
    description = forms.CharField(widget=forms.Textarea, label="Description")
    price = forms.DecimalField(max_digits=10, decimal_places=2, label="Price")
    contact_details = forms.CharField(max_length=255, label="Contact Details")
    image = forms.ImageField(label="Upload Image", required=False)


