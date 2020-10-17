from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from library import views
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name = 'home'),
    #path('accounts/',include('django.contrib.auth.urls') ),

    path('adm/',views.adm, name = 'adm'),
    path('student/',views.student, name = 'student'),

    path('student_signup/',views.studentsignup, name = 'student signup'),
    path('student_login/',LoginView.as_view(template_name='student_login.html')),
    path('admin_login/',LoginView.as_view(template_name='admin_login.html')),
    path('admin_signup/',views.adminsignup, name = 'admin_signup'),

    path('logout/', LogoutView.as_view(template_name='home.html')),
    path('after_login/', views.afterlogin),

    path('about_us/', views.aboutus, name='about us'),

    path('add_book/', views.addbook),
    path('view_book/', views.viewbook),
    path('issue_book/', views.issuebook),
    path('view_issued_book/', views.viewissuedbook),
    path('view_student/', views.viewstudent),
    path('view_issued_book_by_student/', views.viewissuedbookbystudent),

]