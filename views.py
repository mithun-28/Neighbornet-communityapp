from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Group, UserProfile
from .forms import SignupForm, LoginForm

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            group = form.cleaned_data['group']
            user = User.objects.create_user(username=username, password=password)
            UserProfile.objects.create(user=user, group=group)
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('group_page')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Group, UserProfile, Announcement
from .forms import AnnouncementForm

@login_required
def group_page_view(request):
    # Get user's profile and group
    profile = UserProfile.objects.get(user=request.user)
    group = profile.group

    # Fetch announcements for the group, ordered by timestamp
    announcements = Announcement.objects.filter(group=group)

    # Handle announcement submission
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            Announcement.objects.create(
                message=message,
                user=request.user,
                group=group
            )
            return redirect('group_page')  # Redirect after posting
    else:
        form = AnnouncementForm()

    return render(request, 'group_page.html', {
        'group': group,
        'announcements': announcements,
        'form': form
    })


# In your app's `views.py`
from django.contrib.auth import logout
from django.shortcuts import redirect

def custom_logout(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout


from .models import ServiceRequest
from .forms import ServiceRequestForm

@login_required
def service_page_view(request):
    # Get user's profile and group
    profile = UserProfile.objects.get(user=request.user)
    group = profile.group

    # Fetch service requests for the group
    service_requests = ServiceRequest.objects.filter(group=group).order_by('-timestamp')

    # Handle new service request submission
    if request.method == 'POST' and 'create_service' in request.POST:
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            service_name = form.cleaned_data['service_name']
            description = form.cleaned_data['description']
            ServiceRequest.objects.create(
                service_name=service_name,
                description=description,
                user=request.user,
                group=group
            )
            return redirect('service_page')  # Redirect after posting

    # Handle service request acceptance
    if request.method == 'POST' and 'accept_service' in request.POST:
        service_id = request.POST.get('service_id')
        service = ServiceRequest.objects.get(id=service_id, group=group)
        if not service.is_accepted:
            service.is_accepted = True
            service.accepted_by = request.user
            service.save()
        return redirect('service_page')  # Redirect after accepting

    else:
        form = ServiceRequestForm()

    return render(request, 'service_page.html', 
    {
        'group': group,
        'service_requests': service_requests,
        'form': form
    })


from .models import ProductAnnouncement
from .forms import ProductAnnouncementForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def sell_page_view(request):
    # Get user's profile and group
    profile = UserProfile.objects.get(user=request.user)
    group = profile.group

    # Fetch product announcements for the group
    product_announcements = ProductAnnouncement.objects.filter(group=group).order_by('-timestamp')

    # Handle new product announcement submission
    if request.method == 'POST' and 'create_product' in request.POST:
        form = ProductAnnouncementForm(request.POST, request.FILES)
        if form.is_valid():
            product_name = form.cleaned_data['product_name']
            description = form.cleaned_data['description']
            price = form.cleaned_data['price']
            image = form.cleaned_data['image']
            ProductAnnouncement.objects.create(
                product_name=product_name,
                description=description,
                price=price,
                image=image,
                user=request.user,
                group=group
            )
            return redirect('sell_page')  # Redirect after posting

    # Handle product request (buy button)
    if request.method == 'POST' and 'request_product' in request.POST:
        product_id = request.POST.get('product_id')
        product = ProductAnnouncement.objects.get(id=product_id, group=group)
        if not product.is_requested:
            product.is_requested = True
            product.requested_by = request.user
            product.save()
        return redirect('sell_page')  # Redirect after requesting

    else:
        form = ProductAnnouncementForm()

    return render(request, 'sell_page.html', {
        'group': group,
        'product_announcements': product_announcements,
        'form': form
    })


from .models import BusinessAdvertisement
from .forms import BusinessAdvertisementForm
@login_required
def business_page_view(request):
    # Get user's profile and group
    profile = UserProfile.objects.get(user=request.user)
    group = profile.group

    # Fetch business ads for the group
    business_ads = BusinessAdvertisement.objects.filter(group=group).order_by('-timestamp')

    # Handle new business advertisement submission
    if request.method == 'POST' and 'create_ad' in request.POST:
        form = BusinessAdvertisementForm(request.POST, request.FILES)
        if form.is_valid():
            service_name = form.cleaned_data['service_name']
            provider_name = form.cleaned_data['provider_name']
            description = form.cleaned_data['description']
            price = form.cleaned_data['price']
            contact_details = form.cleaned_data['contact_details']
            image = form.cleaned_data['image']
            BusinessAdvertisement.objects.create(
                service_name=service_name,
                provider_name=provider_name,
                description=description,
                price=price,
                contact_details=contact_details,
                image=image,
                user=request.user,
                group=group
            )
            return redirect('business_page')  # Redirect after posting

    # Handle business ad click (to show details)
    if request.method == 'POST' and 'show_details' in request.POST:
        ad_id = request.POST.get('ad_id')
        ad = BusinessAdvertisement.objects.get(id=ad_id, group=group)
        return render(request, 'neighbornet/business_page.html', {
            'group': group,
            'business_ads': business_ads,
            'ad_details': ad,
            'form': form
        })

    else:
        form = BusinessAdvertisementForm()

    return render(request, 'business_page.html', {
        'group': group,
        'business_ads': business_ads,
        'form': form
    })
