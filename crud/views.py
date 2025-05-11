from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Genders, Users
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def gender_list(request):
    try:
        genders = Genders.objects.all()
        
        data = {
            'genders':genders
        }
        
        return render(request, 'gender/GenderList.html', data)
    except Exception as e:
        return HttpResponse(f'Error tanga: {e}')

def add_gender(request):
    try:
        if request.method == 'POST':
            gender = request.POST.get('gender')
            
            Genders.objects.create(gender=gender).save()
            messages.success(request, 'Gender added na, boi!')
            return redirect('/gender/list')
        else:
            return render(request, 'gender/AddGender.html')
    except Exception as e:
        return HttpResponse(f'Error tanga: {e}')
    
def edit_gender(request, genderId):
    try:
        if request.method == 'POST':
            genderObj = Genders.objects.get(pk=genderId)
            
            gender = request.POST.get('gender')
            
            genderObj.gender = gender
            genderObj.save()
            
            messages.success(request, 'Gender updated na, boi!')
            
            data = {
                'gender':genderObj
            }
            
            return render(request, 'gender/EditGender.html', data)
        else:
            genderObj = Genders.objects.get(pk=genderId)
            
            data = {
                'gender':genderObj
            }
        
            return render(request, 'gender/EditGender.html', data)
    except Exception as e:
        return HttpResponse(f'Error tanga: {e}')

def delete_gender(request, genderId):
    try:
        if request.method == 'POST':
            genderObj = Genders.objects.get(pk=genderId)
            genderObj.delete()
            
            messages.success(request, 'Gender deleted na, boi!')
            return redirect('/gender/list')
        else:
            genderObj = Genders.objects.get(pk=genderId)
                
            data = {
                'gender':genderObj
            }
        
            return render(request, 'gender/DeleteGender.html', data)
    except Exception as e:
        return HttpResponse(f'May Error tanga: {e}')
    
def user_list(reuqest):
    try:
        userObj = Users.objects.select_related('gender')
        
        data = {
            'users':userObj
        }
        
        return render(reuqest, 'user/UserList.html', data)
    except Exception as e:
        return HttpResponse(f'Error tanga: {e}')
    
def add_user(request):
    try:
        if request.method == 'POST':
            fullname = request.POST.get('full_name')
            gender = request.POST.get('gender')
            birthDate = request.POST.get('birth_date')
            address = request.POST.get('address')
            contactNumber = request.POST.get('contact_number')
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')
            confirmPassword = request.POST.get('confirm_password')
            
            if password != confirmPassword:
                messages.error(request, 'Password and Confirm Password do not match!')
                return redirect('/user/add')
            
            Users.objects.create(
                full_name=fullname,
                gender=Genders.objects.get(pk=gender),
                birth_date=birthDate,
                address=address,
                contact_number=contactNumber,
                email=email,
                username=username,
                password=make_password(password)    
            ).save()
            
            messages.success(request, 'User added na, boi!')
            return redirect('/user/add')
        else:
            genderObj = Genders.objects.all()
            
            data = {
                'genders': genderObj
            }
            
            return render(request, 'user/AddUser.html', data)
    except Exception as e:
        return HttpResponse(f'Error bobo: {e}')
    
def edit_user(request, userId):
    try:
        if request.method == 'POST':
            userObj = Users.objects.get(pk=userId)
            
            fullname = request.POST.get('full_name')
            gender = request.POST.get('gender')
            birthDate = request.POST.get('birth_date')
            address = request.POST.get('address')
            contactNumber = request.POST.get('contact_number')
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')
            confirmPassword = request.POST.get('confirm_password')
            
            if password and confirmPassword:
                if password != confirmPassword:
                    messages.error(request, 'mali password mo tanga')
                    return redirect('/user/edit')
                userObj.password = make_password(password)
            
            userObj.full_name=fullname
            userObj.gender=Genders.objects.get(pk=gender)
            userObj.birth_date=birthDate
            userObj.address=address
            userObj.contact_number=contactNumber
            userObj.email=email
            userObj.username=username
            userObj.save()
            
            messages.success(request, 'User updated boi good job!')
            return redirect('/user/list')
        else:
            userObj = Users.objects.get(pk=userId)
            genderObj = Genders.objects.all()
            
            data = {
                'user':userObj,
                'gender':genderObj
            }
            
            return render(request, 'user/EditUser.html', data)
    except Exception as e:
        return HttpResponse(f'may error tanga: {e}')

def login_view(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('/user/list')  # Replace 'home' with your main page URL name
            else:
                messages.error(request, 'Invalid username or password.')
                return render(request, 'user/login.html')
    except Exception as e:
        return HttpResponse(f'Error gago: {e}')    

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login/')