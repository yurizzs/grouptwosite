from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Genders, Users
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

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
    
def user_list(request):
    try:
        # Get all users with their related gender data
        user_list = Users.objects.select_related('gender').all()
        
        # Number of users per page
        paginator = Paginator(user_list, 10)  # Show 10 users per page
        
        # Get the current page number from the request
        page_number = request.GET.get('page', 1)
        
        # Get the page object
        page_obj = paginator.get_page(page_number)
        
        data = {
            'users': page_obj,
            'page_obj': page_obj,  # This will be used in the template for pagination
        }
        
        return render(request, 'user/UserList.html', data)
    except Exception as e:
        return HttpResponse(f'Error: {e}')
    
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

            if not birthDate:
                messages.error(request, 'Birth date is required.')
                return redirect('/user/add')

            try:
                # Validate date format
                birthDate = datetime.strptime(birthDate, '%Y-%m-%d').date()
            except ValueError:
                messages.error(request, 'Invalid date format. Please use YYYY-MM-DD format.')
                return redirect('/user/add')
            
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
            
            if not gender:
                messages.error(request, 'Please select a gender')
                return redirect(f'/user/edit/{userId}')
            
            if password and confirmPassword:
                if password != confirmPassword:
                    messages.error(request, 'Password and Confirm Password do not match!')
                    return redirect(f'/user/edit/{userId}')
                userObj.password = make_password(password)
            
            try:
                genderObj = Genders.objects.get(pk=gender)
                userObj.gender = genderObj
            except Genders.DoesNotExist:
                messages.error(request, 'Invalid gender selected')
                return redirect(f'/user/edit/{userId}')
            
            userObj.full_name = fullname
            userObj.birth_date = birthDate
            userObj.address = address
            userObj.contact_number = contactNumber
            userObj.email = email
            userObj.username = username
            userObj.save()
            
            messages.success(request, 'User updated successfully!')
            return redirect('/user/list')
        else:
            userObj = Users.objects.get(pk=userId)
            genderObj = Genders.objects.all()
            
            data = {
                'user': userObj,
                'gender': genderObj
            }
            
            return render(request, 'user/EditUser.html', data)
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')
        return redirect('/user/list')

def delete_user(request, userId):
    try:
        user = Users.objects.get(pk=userId)
        if request.method == 'GET':
            user.delete()
            messages.success(request, f"User {user.username} has been deleted.")
            return redirect('/user/list')
    except Users.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('/user/list')
    except Exception as e:
        messages.error(request, f"Error deleting user: {e}")
        return redirect('/user/list')

def login_view(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            try:
                user = Users.objects.get(username=username)
                if check_password(password, user.password):
                    request.session['user_id'] = user.user_id
                    request.session['username'] = user.username
                    messages.success(request, 'Login successful!')
                    return redirect('/user/list')
                else:
                    messages.error(request, 'Invalid username or password.')
                    return render(request, 'user/login.html')
            except Users.DoesNotExist:
                messages.error(request, 'Invalid username or password.')
                return render(request, 'user/login.html')
        else:
            return render(request, 'user/login.html')
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')
        return render(request, 'user/login.html')

def logout_view(request):
    request.session.flush()
    messages.success(request, 'You have been logged out successfully.')
    return redirect('/login/')