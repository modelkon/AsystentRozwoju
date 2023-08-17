from django.shortcuts import render, HttpResponse
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


class RegisterView(View):

    def get(self, request):
        return render(request, 'accounts/register_form.html')

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        # if password1 == password2

        if User.objects.filter(username=username).exists():
            base_msg = 'Użytkownik o podanej nazwie już istnieje.'
            return render(request, 'accounts/register_form.html', {'base_msg': base_msg})

        if password1 != password2:
            base_msg = 'Hasła nie są takie same'
            return render(request, 'accounts/register_form.html', {'base_msg': base_msg})


        user = User.objects.create_user(username=username, email=None, password=password1)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        login(request, user)
        return render(request, 'base/base.html', {'base_msg': f'Udało się zarejestrować użytkownika: {user}'})


class UserDetailView(View):
    def get(self, request):
        user = User.objects.get(username=request.user)
        return render(request, 'accounts/user_detail.html', {'user': user})



class UserUpdateView(View):

    def get(self, request):
        user = User.objects.get(username=request.user)
        return render(request, 'accounts/user_update_form.html', {'user': user})

    def post(self, request):
        user = User.objects.get(username=request.user)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        User.objects.filter(username=user.username).update(
            username=username, first_name=first_name, last_name=last_name, email=email)
        return render(request, 'base/base.html', {'base_msg': 'Dane zostały zmienione'})


class UserLoginView(View):

    def get(self, request):
        return render(request, 'accounts/login_form.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'base/base.html', {'base_msg': f'Witaj {user}'})
        else:
            base_msg = 'Wprowadziłeś błędny login lub hasło, spróbuj jeszcze raz lub załóż nowe konto.'
            return render(request, 'accounts/login_form.html', {'base_msg': base_msg})




class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return render(request, 'base/base.html', {'base_msg': "Wylogowano"})


class UserUpdatePasswordView(View):
    def get(self, request):
        return render(request, 'accounts/password_update_form.html')

    def post(self, request):
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            user = User.objects.get(request.username)
            user.set_password(password1)
            user.save()
            return render(request, 'base/base.html', {'base_msg': 'Hasło zostało zmienione'})
        else:
            return render(request, 'base/base.html', {'base_msg': 'Hasła różnią się.'})
