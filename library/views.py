from django.shortcuts import render
from django.http import HttpResponseRedirect
from . import forms,models
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from django.contrib import auth
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.core.mail import send_mail
#from lms.settings import EMAIL_HOST_USER

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/after_login')
    return render(request,'home.html')

#for showing signup/login button for student
def student(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/after_login')
    return render(request,'click_student.html')

#for showing signup/login button for teacher
def adm(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/after_login')
    return render(request,'click_admin.html')


def adminsignup(request):
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()


            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)

            return HttpResponseRedirect('/admin_login')
    return render(request,'admin_signup.html',{'form':form})



def studentsignup(request):
    form1=forms.StudentUserForm()
    form2=forms.StudentExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST)
        form2=forms.StudentExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            f2.save()

            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)

        return HttpResponseRedirect('/student_login')
    return render(request,'student_signup.html',context=mydict)



def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()

def afterlogin(request):
    if is_admin(request.user):
        return render(request,'admin_afterlogin.html')
    else:
        return render(request,'student_afterlogin.html')

def aboutus(request):
    return render(request,'about_us.html')


@login_required(login_url='/admin_login')
@user_passes_test(is_admin)
def addbook(request):
    #now it is empty book form for sending to html
    form=forms.BookForm()
    if request.method=='POST':
        #now this form have data from html
        form=forms.BookForm(request.POST)
        if form.is_valid():
            user=form.save()
            return render(request,'book_added.html')
    return render(request,'add_book.html',{'form':form})

@login_required(login_url='/admin_login')
@user_passes_test(is_admin)
def viewbook(request):
    books=models.Book.objects.all()
    return render(request,'view_book.html',{'books':books})




@login_required(login_url='/admin_login')
@user_passes_test(is_admin)
def issuebook(request):
    form=forms.IssuedBookForm()
    if request.method=='POST':
        #now this form have data from html
        form=forms.IssuedBookForm(request.POST)
        if form.is_valid():
            obj=models.IssuedBook()
            obj.enrollment=request.POST.get('enrollment2')
            obj.isbn=request.POST.get('isbn2')
            obj.save()
            return render(request,'book_issued.html')
    return render(request,'issue_book.html',{'form':form})


@login_required(login_url='/admin_login')
@user_passes_test(is_admin)
def viewissuedbook(request):
    issuedbooks=models.IssuedBook.objects.all()
    li=[]
    for ib in issuedbooks:
        issdate=str(ib.issuedate.day)+'-'+str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate=str(ib.expirydate.day)+'-'+str(ib.expirydate.month)+'-'+str(ib.expirydate.year)
        #fine calculation
        days=(date.today()-ib.issuedate)
        print(date.today())
        d=days.days
        fine=0
        if d>30:
            day=d-30
            fine=day*10


        books=list(models.Book.objects.filter(isbn=ib.isbn))
        students=list(models.StudentExtra.objects.filter(enrollment=ib.enrollment))
        i=0
        for l in books:
            t=(students[i].get_name,students[i].enrollment,books[i].name,books[i].author,issdate,expdate,fine)
            i=i+1
            li.append(t)

    return render(request,'view_issued_book.html',{'li':li})

@login_required(login_url='/admin_login')
@user_passes_test(is_admin)
def viewstudent(request):
    students=models.StudentExtra.objects.all()
    return render(request,'view_student.html',{'students':students})


@login_required(login_url='/student_login')
def viewissuedbookbystudent(request):
    student=models.StudentExtra.objects.filter(user_id=request.user.id)
    issuedbook=models.IssuedBook.objects.filter(enrollment=student[0].enrollment)

    li1=[]

    li2=[]
    for ib in issuedbook:
        books=models.Book.objects.filter(isbn=ib.isbn)
        for book in books:
            t=(request.user,student[0].enrollment,student[0].branch,book.name,book.author)
            li1.append(t)
        issdate=str(ib.issuedate.day)+'-'+str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate=str(ib.expirydate.day)+'-'+str(ib.expirydate.month)+'-'+str(ib.expirydate.year)
        #fine calculation
        days=(date.today()-ib.issuedate)
        print(date.today())
        d=days.days
        fine=0
        if d>30:
            day=d-30
            fine=day*10
        t=(issdate,expdate,fine)
        li2.append(t)

    return render(request,'view_issued_book_by_student.html',{'li1':li1,'li2':li2})
