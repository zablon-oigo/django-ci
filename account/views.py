from django.shortcuts import render
from .models import CustomUser
def sign_in(request):
    if request.method == 'POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            
            user=authenticate(request, email=email, password=password)
            
            if user is not None and user.is_active:
                login(request, user)
                messages.success(request, 'Login request was successfull')
                return redirect('list')
        messages.error(request, 'Invalid username or password')
    form=LoginForm()
    return render(request,'accounts/login.html',{'form':form})