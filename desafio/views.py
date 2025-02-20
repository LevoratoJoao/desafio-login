from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

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

        try:
            username = User.objects.get(email=email)
            if (username.check_password(password) == False):
                messages.error(request, 'Senha inválida')
        except User.DoesNotExist:
            username = None

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            if (checkIfEmailExists(email)):
                messages.error(request, 'E-mail inválido')

    return render(request, "desafio/login.html")

def isPasswordValid(request, password):
    errors = []
    if len(password) < 8:
        errors.append('Senha deve ter no mínimo 8 caracteres')
    if not any(char in string.punctuation for char in password):
        errors.append('Senha deve ter no mínimo 1 caractere especial')
    if not any(char.isdigit() for char in password):
        errors.append('Senha deve ter no mínimo 1 número')
    if not any(char.isupper() for char in password):
        errors.append('Senha deve ter no mínimo 1 letra maiúscula')
    for error in errors:
        messages.error(request, error)
    return not errors

def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        password = form.data['password1']
        email = form.data['email']
        # if User.objects.filter(email=email).exists():
        #     messages.error(request, 'Email já cadastrado')

        if isPasswordValid(request, password) and form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Usuário ' + user + ' foi criado ')
    context = {'form': form}
    return render(request, "desafio/register.html", context)

def logoutView(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))
