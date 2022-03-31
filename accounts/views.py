from django.shortcuts import render, redirect
from django.contrib import messages, auth
from accounts.models import User
from contacts.models import Contact
from listings.models import Listing, Contract


def register(request):
    if request.method == 'POST':
        # Get Form Values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        eth_acc = request.POST['eth_acc']
        is_renter = request.POST.get('is_renter', False)
        is_renter = True if is_renter else False

        # Check if passwords match
        if password == password2:
            # Check Username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'This email is in use')
                    return redirect('register')
                else:
                    # Looks good
                    user = User.objects.create_user(username=username, password=password, email=email, eth_acc=eth_acc, first_name=first_name, last_name=last_name, is_renter=is_renter)
                    # Login After Register
                    # auth.login(request, user)
                    # messages.success(request, 'You are now logged in')
                    # return redirect('index')
                    user.save()
                    messages.success(request,'You are now registred and can login')
                    return redirect('login')
        else:
            messages.error(request, 'Password do not match')
            return redirect('register')    
    else:
        return render(request, 'accounts/register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Вы залогинены!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Неправильные данные')
            return redirect('login')    
    else:
        return render(request, 'accounts/login.html')
    

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('index')
    
def dashboard(request):
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)
    listings = Listing.objects.order_by('list_date').filter(contract__tenant__contains=request.user.eth_acc) | Listing.objects.order_by('list_date').filter(user=request.user)
    contracts = Contract.objects.order_by('listing').filter(listing=listings)


    context = {
        'contacts': user_contacts,
        'listings':listings,
        'contracts': contracts
    }
    return render(request, 'accounts/dashboard.html', context)    
