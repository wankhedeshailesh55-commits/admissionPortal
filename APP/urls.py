
from django.urls import path
from APP import views

urlpatterns = [
    path('register/',views.registration),
    path('viewRegisteringUser/',views.getUser),
    path('viewAllUsers/',views.getAllUsers),
    path('', views.home),

    path('view/<int:id>/', views.manageUser),
    path('view/edit/<int:id>/', views.editUserForm),
    path('edit/<int:id>/',views.editUser),
    path('delete/<int:id>/', views.deleteUser),

    path('courses/',views.viewCourses),
    path('contacts/',views.contactUs),
    path('abouts/',views.aboutUs),

    path('signUpForm/',views.signUpForm),
    path('signup/', views.signUp),
    path('loginForm/',views.loginForm),
    path('login/',views.loginUser),
    path('logout/',views.logoutUser),

    path('search/',views.searchingStudents),

    path('initial-setup/', views.production_setup),
]