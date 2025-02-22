from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

# Create your views here.
def show_account(request):
    context={}
    if request.POST and 'register' in request.POST:
        context['register'] = True
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')
            address = request.POST.get('address')
            phone = request.POST.get('phone')
            # Creates user account
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email
            )
            # Creates customer account
            customer = Customer.objects.create(
                name=username,
                user=user,
                phone=phone,
                address=address
            )
            success_message = "User registered successfully!"
            messages.success(request, success_message)
            return redirect('account')
        except Exception as e:
            error_message = "Duplicate value or invalid input"
            messages.error(request, error_message)

    if request.POST and 'login' in request.POST:
        context['register'] = False
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid credentials')

    return render(request, 'account.html', context)

def sign_out(request):
    logout(request)
    return redirect('index')
