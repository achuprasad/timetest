from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from testapp.forms import PersonCreationForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.


class Register(View):
    def get(self,request):
        context={}
        form=PersonCreationForm()
        context['form']=form

        return render(request,'register.html',context)

    def post(self, request):
        context = {}
        form = PersonCreationForm(request.POST)
        if form.is_valid():
            print("valid")
            user = form.save(commit=False)
            password = form.cleaned_data.get('password1')
            user.password = make_password(password)
            user.save()
            return redirect('login')
        else:
            print("invalid")
            context['form'] = form
            print(form.errors)
        return render(request, 'register.html', context)


class Login(View):
    def get(self,request):
        context={}
        form = LoginForm()
        context['form']=form
        return render(request,'login.html',context)

    def post(self,request):
        context = {}
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                # Redirect based on user role
                if user.role == 'student':
                    print("student")
                    return redirect('/student')
                elif user.role == 'staff':
                    print("staff")
                    return redirect('/staff')
                elif user.role == 'admin':
                    print("admin")
                    return redirect('/admin')
                elif user.role == 'editor':
                    print("editor")
                    return redirect('/editor')
            else:
                context['form'] = form
                context['error'] = "Invalid email or password"
                return render(request, 'login.html', context)
        else:
            context['form'] = form
        return render(request, 'login.html', context)

class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('login')


@method_decorator(login_required, name='dispatch')
class StudentPageView(View):
    def get(self, request):
        return render(request, 'student_page.html')

@method_decorator(login_required, name='dispatch')
class StaffPageView(View):
    def get(self, request):
        return render(request, 'staff_page.html')

@method_decorator(login_required, name='dispatch')
class AdminPageView(View):
    def get(self, request):
        return render(request, 'admin_page.html')

@method_decorator(login_required, name='dispatch')
class EditorPageView(View):
    def get(self, request):
        return render(request, 'editor_page.html')
