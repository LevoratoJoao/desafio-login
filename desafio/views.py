from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail

from desafio.forms import CreateUserForm
from .forms import User

import string

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return render(request, "desafio/menu.html")
    else:
        return render(request, "desafio/login.html")

def checkIfEmailExists(email):
    return User.objects.filter(email=email).exists() == False

def loginView(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        if (checkIfEmailExists(email)):
            messages.error(request, 'E-mail inexistente')
            return render(request, "desafio/login.html")

        username = User.objects.get(email=email)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        if (not username.check_password(password)):
            messages.error(request, 'Senha inválida')

    return render(request, "desafio/login.html")

def isPasswordValid(request, password, password2):
    errors = []
    if len(password) < 8:
        errors.append('Senha deve ter no mínimo 8 caracteres')
    if password != password2:
        errors.append('Senhas não coincidem')
    if not any(char in string.punctuation for char in password):
        errors.append('Senha deve ter no mínimo 1 caractere especial')
    if not any(char.isdigit() for char in password):
        errors.append('Senha deve ter no mínimo 1 número')
    if not any(char.isupper() for char in password):
        errors.append('Senha deve ter no mínimo 1 letra maiúscula')
    for error in errors:
        messages.error(request, error)
    return not errors

def isUsernameValid(username):
    if (any(char.isdigit() for char in username)) or (any(char in string.punctuation for char in username)):
        return False
    return True

def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        username = form.data['username']
        if username == '' or isUsernameValid(username) == False:
            messages.error(request, 'Nome de usuário não pode conter caracteres especiais ou números')
            return render(request, "desafio/register.html", {'form': form})

        email = form.data['email']
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email já cadastrado')
            return render(request, "desafio/register.html", {'form': form})

        password = form.data['password1']
        password2 = form.data['password2']
        if isPasswordValid(request, password, password2) and form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Usuário ' + user + ' foi criado ')
            send_mail(
                "Desafio login registrado",
                "Você foi registrado no desafio técnico da Fidelity!!",
                "django@mailtrap.club",
                [email])
            return redirect('login')

    context = {'form': form}
    return render(request, "desafio/register.html", context)

def logoutView(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))
