from django.core.validators import validate_email
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your views here.


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('app:dashboard')  # il faut rediriger vers le lien dashboard
            return redirect('app:home')  # home dans le site
        else:
            messages.error(request, "Nom d\'utilisateur ou mot de passe incorrect")
    context = {
        'document_title': 'login'
    }
    return render(request, 'accounts/pages/login.html', context)


@login_required
def profile_user(request):
    context = {
        'document_title': 'profile'
    }
    return render(request, 'accounts/pages/profile.html', context)


def register_user(request):
    data_error = dict()
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')   

        print(username,email,password,password1)

        

        if username and User.objects.filter(username=username).exists():
            data_error['username'] = "Ce nom d'utilisateur existe déjà !"
        if email :
            try :
                validate_email(email)
                if User.objects.filter(email=email).exists():
                    data_error['email'] = "Cet email existe déjà"
            except ValationError:
                data_error['email'] = "Veuillez entrer un email valide"


        if password1 and password and password != password1:
            data_error['password1'] = 'Le deux mots de passe doivent être les mêmes'
        
        if not email or not username or not password or not password1:
            messages.error(request, 'Aucun champ ne doit être vide !!!')
            data_error['global'] =  'Aucun champ ne doit être vide1 !!!'

        # si au moins une erreur est trouvé
        if not data_error:
            # on crée le user
            user = User.objects.create_user(username=username,password=password)
            user.email = email
            user.save()
            messages.success(request, "Votre compte a été crée avec success")
            return redirect('accounts:login')
        

    context = {
        'document_title': 'enregistrement',
        'data_error':data_error
    }
    return render(request, 'accounts/pages/register.html', context)


def logout_user(request):
    logout(request)
    return redirect('accounts:login')
