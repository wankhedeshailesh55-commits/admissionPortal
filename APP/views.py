import os
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.views.decorators.http import require_POST, require_http_methods

from .models import Student

# Create your views here.
@login_required
# @permission_required('APP.add_student', raise_exception=True)
def registration(request):
    return render(request,'registrationForm.html')

@login_required
def getUser(request):

    if request.method == 'POST':

        # Check whether this user already has a Student record
        student = Student.objects.filter(user=request.user).first()

        if student:
            messages.error(
                request,
                'You have already registered.'
            )

            return redirect(f'/admission/view/{student.id}/')

        name = request.POST.get('userName')
        email = request.POST.get('userEmail')
        mobile = request.POST.get('userMobile')
        date = request.POST.get('userBirth')
        gender = request.POST.get('gender')
        course = request.POST.get('course')
        address = request.POST.get('address')

        student = Student.objects.create(
            user=request.user,
            name=name,
            email=email,
            mobile=mobile,
            birth=date,
            gender=gender,
            course=course,
            address=address
        )

        return render(
            request,
            'viewRegisterUser.html',
            {
                'student': student
            }
        )

@login_required
@permission_required('APP.view_student', raise_exception=True)
def getAllUsers(request):

    students = Student.objects.all()

    context = {
        'students': students
    }

    return render(request, 'viewAllUsers.html', context)

def home(request):
    return render(request, 'home.html')

@login_required
def manageUser(request, id):

    if request.user.is_superuser or request.user.groups.filter(name='Admission Staff').exists():

        student = get_object_or_404(Student, id=id)

    else:

        student = get_object_or_404(
            Student,
            id=id,
            user=request.user
        )

    context = {
        'student': student
    }

    return render(request, 'viewRegisterUser.html', context)

@login_required
# @permission_required('APP.change_student', raise_exception=True)
def editUserForm(request, id):

    if request.user.is_superuser or request.user.groups.filter(name='Admission Staff').exists():

        student = get_object_or_404(Student, id=id)

    else:

        student = get_object_or_404(
            Student,
            id=id,
            user=request.user
        )

    context = {
        'student': student
    }

    return render(request, 'showEditUserForm.html', context)

# @login_required
# @permission_required('APP.change_student', raise_exception=True)
@login_required
def editUser(request, id):

    if request.user.is_superuser or request.user.groups.filter(name='Admission Staff').exists():

        student = get_object_or_404(Student, id=id)

    else:

        student = get_object_or_404(
            Student,
            id=id,
            user=request.user
        )

    if request.method == 'POST':

        student.name = request.POST.get('userName')
        student.email = request.POST.get('userEmail')
        student.mobile = request.POST.get('userMobile')
        student.birth = request.POST.get('userBirth')
        student.gender = request.POST.get('gender')
        student.course = request.POST.get('course')
        student.address = request.POST.get('address')

        student.save()

        return redirect(f'/admission/view/{id}/')

    return render(request, 'showEditUserForm.html', {
        'student': student
    })

@login_required
# @permission_required('APP.delete_student', raise_exception=True)
@require_POST
def deleteUser(request, id):

    if not (
        request.user.is_superuser
        or request.user.groups.filter(name='Admission Staff').exists()
    ):
        return render(
            request,
            'error.html',
            {
                'error_code': 403,
                'error_title': 'Forbidden',
                'error_message': 'You do not have permission to delete students.'
            },
            status=403
        )

    student = get_object_or_404(Student, id=id)

    student.delete()

    messages.success(
        request,
        'Student deleted successfully.'
    )

    return redirect('/admission/viewAllUsers/')

def viewCourses(request):
    return render(request,'ourCourses.html')

def contactUs(request):
    return render(request,'contactInfo.html')

def aboutUs(request):
    return render(request,'aboutUs.html')


def signUpForm(request):
    return render(request,'signup.html')

def signUp(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')


        # Check password
        if password != confirm_password:

            messages.error(
                request,
                'Passwords do not match.'
            )

            return redirect('/admission/signUpForm/')


        # Check username already exists
        if User.objects.filter(username=username).exists():

            messages.error(
                request,
                'Username already exists.'
            )

            return redirect('/admission/signUpForm/')


        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )


        messages.success(
            request,
            'Account created successfully. You can now login.'
        )

        return redirect('/admission/loginForm/')


    return render(request, 'signup.html')

def loginForm(request):
    return render(request,'login.html')

def loginUser(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')


        # Authenticate user
        user = authenticate(
            request,
            username=username,
            password=password
        )


        if user is not None:

            # Create login session
            login(request, user)

            messages.success(
                request,
                f'Login successful. Welcome back, {user.username}!'
            )

            next_url = request.POST.get('next')
            if next_url:
                return redirect(next_url)

            return redirect('/admission/')


        else:

            messages.error(
                request,
                'Invalid username or password.'
            )

            return redirect('/admission/loginForm/')


    return render(request, 'login.html')

@login_required
def logoutUser(request):

    logout(request)

    messages.success(
        request,
        'You have been logged out successfully.'
    )

    return redirect('/admission/loginForm/')

@login_required
def searchingStudents(request):

    q = request.GET.get('q', '').strip()

    if request.user.is_superuser or request.user.groups.filter(name='Admission Staff').exists():

        # Staff and superuser can search all students
        students = Student.objects.filter(
            Q(name__icontains=q) |
            Q(course__icontains=q) |
            Q(email__icontains=q) |
            Q(mobile__icontains=q)
        )

    else:

        # Normal user can search only their own record
        students = Student.objects.filter(
            user=request.user
        ).filter(
            Q(name__icontains=q) |
            Q(course__icontains=q) |
            Q(email__icontains=q) |
            Q(mobile__icontains=q)
        )

    context = {
        'students': students,
    }

    return render(
        request,
        'viewAllUsers.html',
        context
    )





@require_http_methods(["GET", "POST"])
def production_setup(request):

    # Only allow setup when no superuser exists yet
    if User.objects.filter(is_superuser=True).exists():
        return HttpResponseForbidden(
            "Production setup has already been completed."
        )

    if request.method == "GET":
        return render(request, "production_setup.html")

    # Check secret setup key
    setup_key = request.POST.get("setup_key", "")
    expected_key = os.environ.get("PRODUCTION_SETUP_KEY", "")

    if not expected_key or setup_key != expected_key:
        return HttpResponseForbidden("Invalid setup key.")

    username = request.POST.get("username", "").strip()
    email = request.POST.get("email", "").strip()
    password = request.POST.get("password", "")
    confirm_password = request.POST.get("confirm_password", "")

    if not username or not email or not password:
        return render(
            request,
            "production_setup.html",
            {"error": "All fields are required."}
        )

    if password != confirm_password:
        return render(
            request,
            "production_setup.html",
            {"error": "Passwords do not match."}
        )

    if User.objects.filter(username=username).exists():
        return render(
            request,
            "production_setup.html",
            {"error": "Username already exists."}
        )

    try:
        validate_password(password)
    except ValidationError as e:
        return render(
            request,
            "production_setup.html",
            {"error": " ".join(e.messages)}
        )

    with transaction.atomic():

        # Create production superuser
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )

        # Create Admission Staff group
        group, created = Group.objects.get_or_create(
            name="Admission Staff"
        )

        # Give Student permissions to the group
        content_type = ContentType.objects.get_for_model(Student)

        permissions = Permission.objects.filter(
            content_type=content_type,
            codename__in=[
                "add_student",
                "change_student",
                "delete_student",
                "view_student",
            ]
        )

        group.permissions.set(permissions)

    return render(
        request,
        "production_setup.html",
        {
            "success": (
                "Production setup completed successfully. "
                "You can now login to Django Admin."
            )
        }
    )
