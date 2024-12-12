from django.contrib.auth.models import User
from django.db import models


    
class Group(models.Model):
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=100, default="Unknown")  # Add a default value here

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username


class Announcement(models.Model):
    message = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Announcement by {self.user.username} in {self.group.name}"

    class Meta:
        ordering = ['-timestamp']  # To show latest announcements first



from django.db import models
from django.contrib.auth.models import User
from .models import Group

class ServiceRequest(models.Model):
    service_name = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)  # Tracks if the service is accepted
    accepted_by = models.ForeignKey(User, related_name='accepted_services', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.service_name} by {self.user.username} in {self.group.name}"
    


class ProductAnnouncement(models.Model):
    product_name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    requested_by = models.ForeignKey(User, related_name='product_requests', on_delete=models.SET_NULL, null=True, blank=True)
    is_requested = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product_name} by {self.user.username} in {self.group.name}"
    

class BusinessAdvertisement(models.Model):
    service_name = models.CharField(max_length=100)
    provider_name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    contact_details = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='business_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.service_name} by {self.provider_name} in {self.group.name}"





