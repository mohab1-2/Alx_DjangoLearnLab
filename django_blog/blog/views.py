from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileEditForm, CustomPasswordChangeForm

def register_view(request):
    if request.user.is_authenticated:
        return redirect('profile')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created successfully for {username}!')
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('profile')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name or username}!")
                next_page = request.GET.get('next', 'profile')
                return redirect(next_page)
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = AuthenticationForm()
    
    form.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
    form.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
    
    return render(request, "registration/login.html", {"form": form})

def logout_view(request):
    user_name = request.user.first_name or request.user.username
    logout(request)
    messages.success(request, f"Goodbye {user_name}! You have been logged out successfully.") 
    return redirect('login')

@login_required
def profile_view(request):
    return render(request, 'registration/profile.html', {'user': request.user})

# NEW: Profile Edit View
@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileEditForm(instance=request.user)
    
    return render(request, 'registration/edit_profile.html', {'form': form})

# NEW: Password Change View
@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)  # Important!
            messages.success(request, 'Your password has been changed successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomPasswordChangeForm(request.user)
    
    return render(request, 'registration/change_password.html', {'form': form})
