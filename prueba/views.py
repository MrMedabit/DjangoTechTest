from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm
from .models import CustomUser, Product, Event
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'home.html')

@login_required
def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': CustomUserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = CustomUser.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                new_event = Event(event_type=2, description='User created', creator=request.user)
                new_event.save()
                user.save()
                return HttpResponse('User created successfully')
            except:
                return HttpResponse('User already exists')
        return HttpResponse('Passwords do not match')
    
def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Username or password is incorrect'
            })
        else:
            print(request.user)
            login(request, user)
            return redirect('/products')

def products(request):
    if request.method == 'GET':
        products = Product.objects.all().order_by('name')
        return render(request, 'products.html', {
            'products': products
        })
    else:
        if request.POST['form_type'] == 'create':
            product = Product(name=request.POST['name'], description=request.POST['description'], quantity=request.POST['quantity'], creator=request.user)
            new_event = Event(event_type=1, description='Product added', creator=request.user)
            new_event.save()
            product.save()
            return redirect('/products')
        
        elif request.POST['form_type'] == 'edit':
            product = get_object_or_404(Product, pk=request.POST['id'])#Product(name=request.POST['name'], description=request.POST['description'], quantity=request.POST['quantity'], creator=request.user, id=request.POST['id'])
            product.name = request.POST['name']
            product.description = request.POST['description']
            product.quantity = request.POST['quantity']
            product.save()
            new_event = Event(event_type=1, description='Product updated', creator=request.user)
            new_event.save()
            return redirect('/products')
        else:
            product = get_object_or_404(Product, pk=request.POST['id'])
            product.delete()
            return redirect('/products')    
def signout(request):
    logout(request)
    return redirect('home')

def users(request):
    if request.user.level < 3 and request.method == 'GET':
        return HttpResponseForbidden()
    else:
        if request.method == 'POST' and request.user.level > 2:
            if request.POST['form_type'] == 'create':
                new_user = CustomUser.objects.create_user(username=request.POST['username'], password=request.POST['password'])
                new_event = Event(event_type=2, description='User created', creator=request.user)
                new_event.save()
                new_user.save()
                return redirect('/users')
            else:
                user = get_object_or_404(CustomUser, pk=request.POST['id'])
                user.delete()
                return redirect('/users')
        userlist = CustomUser.objects.all()
        return render(request, 'users.html', {
            'users': userlist
        })
    
@login_required
def dashboard(request):
    if request.user.level > 2:
        if request.method == 'POST':
            if request.POST['form_type'] == 'userDelete':
                user = get_object_or_404(CustomUser, pk=request.POST['id'])
                user.delete()
                return redirect('/dashboard')
            elif request.POST['form_type'] == 'productEdit':
                product = get_object_or_404(Product, pk=request.POST['id'])#Product(name=request.POST['name'], description=request.POST['description'], quantity=request.POST['quantity'], creator=request.user, id=request.POST['id'])
                product.name = request.POST['name']
                product.description = request.POST['description']
                product.quantity = request.POST['quantity']
                product.save()
                new_event = Event(event_type=1, description='Product updated', creator=request.user)
                new_event.save()
                return redirect('/dashboard')
            elif request.POST['form_type'] == 'productDelete':
                product = get_object_or_404(Product, pk=request.POST['id'])
                product.delete()
                new_event = Event(event_type=1, description='Product deleted', creator=request.user)
                new_event.save()
                return redirect('/dashboard')

        events = Event.objects.all().order_by('date')
        products = Product.objects.all().order_by('name')
        users = CustomUser.objects.all().order_by('username')
        return render(request, 'dashboard.html', {
            'events': events,
            'products': products,
            'users': users
        })
    else:
        return HttpResponseForbidden()