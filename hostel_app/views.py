from django.shortcuts import render, redirect
from hostel_app import forms

from django.urls import reverse
from hostel_app.models import Student,Room,Hostel,CollegeInfo,Mess,wardenInfo,vehicle
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import re

# Create your views here.

def index(request):
    return render(request,'hostel_app/index.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

# for rex  in Mess.objects.raw('select * from hostel_app_mess'):
#     print(rex)

def reg(request):

    registered = False

    if request.method == 'POST':
        user_form = forms.UserForm(request.POST)
        student_form = forms.StudentForm(request.POST)
        # clg_form = forms.ClgForm(request.POST)

        if user_form.is_valid() and student_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)  #For hashing passwords
            user.save()

            student = student_form.save(commit=False)
            student.user = user;

            #b = Room.objects.get(hostel = student.room.hostel , room_num = student.room.room_num)
            b = Room.objects.raw('SELECT * FROM hostel_app_room WHERE room_num = %s and hostel_id =%s',[student.room.room_num,student.room.hostel])[0]
            b.room_alloted = True;
            b.save()

            # clg = clg_form.save(commit=False)
            # clg.save()
            student.save()
            registered = True

        else:
            print(user_form.errors , student_form.errors )

    else:
        user_form = forms.UserForm()
        student_form = forms.StudentForm()
        # clg_form = forms.ClgForm()

    #boys_hostel = Hostel.objects.filter(gender="M")
    #girls_hostel = Hostel.objects.filter(gender="F")
    validmis = CollegeInfo.objects.raw('SELECT mis FROM hostel_app_collegeinfo');
    
    boys_hostel = Hostel.objects.raw('SELECT * FROM hostel_app_hostel WHERE gender="M"');
    girls_hostel = Hostel.objects.raw('SELECT * FROM hostel_app_hostel WHERE gender="F"');

    return render(request,'hostel_app/reg.html',
                            {'user_form':user_form,
                            'student_form':student_form,
                            'registered':registered,
                            'boys_hostel':boys_hostel,
                            'validmis':validmis,
                            'girls_hostel':girls_hostel})


@login_required
def edit(request):
    current_student = Student.objects.raw('SELECT h.* FROM hostel_app_student as h ,auth_user as a WHERE a.id=h.user_id and a.username=%s',[request.user.get_username()])[0]
    current_hostel = current_student.room.hostel.hostel_name
    current_room = current_student.room.room_num
    if request.method == 'POST':
        #Deallocating current room
        #b = Room.objects.get(hostel = current_hostel , room_num = current_room)
        b = Room.objects.raw('SELECT * FROM hostel_app_room WHERE room_num = %s and hostel_id =%s',[current_room,current_hostel])[0]
        b.room_alloted = False;
        b.save()

        student_form = forms.StudentForm(request.POST, instance=request.user.student)
        if student_form.is_valid():
            current_student = Student.objects.raw('SELECT h.* FROM hostel_app_student as h ,auth_user as a WHERE a.id=h.user_id and a.username=%s',[request.user.get_username()])[0]
            current_hostel = current_student.room.hostel.hostel_name
            current_room = current_student.room.room_num

            student = student_form.save(commit=False)

            #Allocating new room
            #b = Room.objects.get(hostel = student.room.hostel , room_num = student.room.room_num)
            b = Room.objects.raw('SELECT * FROM hostel_app_room WHERE room_num = %s and hostel_id =%s',[student.room.room_num,student.room.hostel])[0]
            b.room_alloted = True;
            b.save()

            student.save()
            return StudentProfileView(request)
        else:
            #Re-allocating current room
            #b = Room.objects.get(hostel = current_hostel , room_num = current_room)
            b = Room.objects.raw('SELECT * FROM hostel_app_room WHERE room_num = %s and hostel_id =%s',[current_room,current_hostel])[0]
            b.room_alloted = True;
            b.save()
    else:
        student_form = forms.StudentForm(instance=request.user.student)

    #boys_hostel = Hostel.objects.filter(gender="M")
    #girls_hostel = Hostel.objects.filter(gender="F")
    boys_hostel = Hostel.objects.raw('SELECT * FROM hostel_app_hostel WHERE gender="M"');
    girls_hostel = Hostel.objects.raw('SELECT * FROM hostel_app_hostel WHERE gender="F"');

    return render(request,'hostel_app/profile_edit.html',
                            {'student_form':student_form,
                            'boys_hostel':boys_hostel,
                            'girls_hostel':girls_hostel})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username , password = password)

        if user is not None:
            if user.is_active:
                login(request,user)
                if username=="chief_warden":
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return StudentProfileView(request)
            else:
                return HttpResponse("Account not active")
        else:
            print("Someone tried to login")
            print("Username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details")
    else:
        return render(request,'hostel_app/login.html')

from django.views import generic

def HostelList(request):
    #hostel = Hostel.objects.all()
    hostel = Hostel.objects.raw('SELECT * FROM hostel_app_hostel')
    context = {
        'hostel_list':hostel,
    }
    return render(request,'hostel_app/hostel_list.html',
                            context=context)

@login_required
def HostelWiseView(request):
    #current_student = Student.objects.get(user__username=request.user.get_username())
    current_student = Student.objects.raw('SELECT h.* FROM hostel_app_student as h ,auth_user as a WHERE a.id=h.user_id and a.username=%s',[request.user.get_username()])[0]
    hostel_name = current_student.room.hostel.hostel_name
    #students = Student.objects.filter(room__hostel__hostel_name=hostel_name)
    #count = students.count()
    #hostel = Hostel.objects.get(hostel_name=hostel_name)
    students = Student.objects.raw('SELECT s.* FROM hostel_app_student s, hostel_app_room r WHERE s.room_id=r.id and hostel_id=%s',[hostel_name])
    count = len(students)
    hostel = Hostel.objects.raw('SELECT * FROM hostel_app_hostel WHERE hostel_name=%s',[hostel_name])[0]
    context = {
        'students':students,
        'hostel':hostel,
        'num_students': count,
    }
    return render(request,'hostel_app/hostelwise_details.html',
                            context=context)

def StudentList(request):
    #student = Student.objects.all()
    student = Student.objects.raw('SELECT * FROM hostel_app_student')
    clg = CollegeInfo.objects.raw('SELECT * FROM hostel_app_collegeinfo')
    context = {
        'student_list':student,
        'clg_list':clg
    }
    return render(request,'hostel_app/student_list.html',
                            context=context)

@login_required
def HostelStudentList(request):
    #current_student = Student.objects.get(user__username=request.user.get_username())
    current_student = Student.objects.raw('SELECT h.* FROM hostel_app_student as h ,auth_user as a WHERE a.id=h.user_id and a.username=%s',[request.user.get_username()])[0]
    hostel_name = current_student.room.hostel.hostel_name
    students = Student.objects.filter(room__hostel__hostel_name=hostel_name).order_by('room__room_num')
    row_count = students.count()
    students = Student.objects.raw('SELECT s.* FROM hostel_app_student s, hostel_app_room r WHERE s.room_id=r.id and hostel_id=%s order by r.room_num',[hostel_name])
    n = 4
    students_list = [students[i * n:(i + 1) * n] for i in range((len(students) + n - 1) // n )]
    context = {
        'student_list':students_list,
        'num_rows':range(row_count),
    }
    return render(request,'hostel_app/hostel_student_list.html',
                            context=context)

@login_required
def StudentProfileView(request):

    #student = Student.objects.get(user__username = current_user)
    current_user = request.user.get_username()
    student = Student.objects.raw('SELECT h.* FROM hostel_app_student as h ,auth_user as a WHERE a.id=h.user_id and a.username=%s',[current_user])[0]
    clg = CollegeInfo.objects.raw('SELECT * FROM hostel_app_collegeinfo where mis=%s',[student.mis_id_id])[0]
    # # for e in clg:
    # print(clg.batchof)
    context = {
        'student':student,
        'clg':clg
    }
    return render(request,'hostel_app/student_details.html',
                            context=context)

@login_required
def add_room(request):

    print(request.user.get_username())
    current_user = request.user.get_username()
    warden = True
    if current_user!="chief_warden":
        warden = False

    room_added = False
    if request.method == 'POST':
        room_form = forms.RoomForm(request.POST)
        if room_form.is_valid():
            room = room_form.save(commit=False)
            room.save()
            room_added = True;
    else:
        room_form = forms.RoomForm()

    return render(request,'hostel_app/add_room.html',
                                {'room_form':room_form, 'room_added':room_added, 'is_warden':warden})

@login_required
def add_hostel(request):
    current_user = request.user.get_username()
    warden = True
    if current_user!="chief_warden":
        warden = False

    hostel_added = False
    if request.method == 'POST':
        hostel_form = forms.HostelForm(request.POST)
        if hostel_form.is_valid():
            hostel = hostel_form.save(commit=False)
            hostel.save()
            hostel_added = True;
            hostel_form = forms.HostelForm()
    else:
        hostel_form = forms.HostelForm()

    return render(request,'hostel_app/add_hostel.html',
                                {'hostel_form':hostel_form, 'hostel_added':hostel_added, 'is_warden':warden})

@login_required
def add_vehicle(request):
    veh_added = False
    current_user = request.user.get_username()
    student = Student.objects.raw('SELECT h.* FROM hostel_app_student as h ,auth_user as a WHERE a.id=h.user_id and a.username=%s',[current_user])[0]
        
    if request.method == 'POST':
        veh_form = forms.VehicleForm(request.POST)
        
        if veh_form.is_valid():
            current_user = request.user.get_username()
            # student = Student.objects.raw('SELECT h.* FROM hostel_app_student as h ,auth_user as a WHERE a.id=h.user_id and a.username=%s',[current_user])[0]
        
            #b = Room.objects.get(hostel = student.room.hostel , room_num = student.room.room_num)
            # b = Student.objects.raw('SELECT * FROM hostel_app_student WHERE user_id =%s',[current_user])
            
            
            # veh.save()
            veh = veh_form.save(commit=False)
            veh.save()
            veh_added = True;
            veh_form = forms.VehicleForm()
            
    else:
        veh_form = forms.VehicleForm()
    # print('h_id', request.user.get_username())
    return render(request,'hostel_app/add_vehicle.html',
                                {'veh_form':veh_form, 'vehicle_added':veh_added, 'student':student})#request.user.get_username()})


def add_mess(request):
    current_user = request.user.get_username()
    warden = True
    if current_user!="chief_warden":
        warden = False

    mess_added = False
    if request.method == 'POST':
        mess_form = forms.MessForm(request.POST)
        if mess_form.is_valid():
            mess = mess_form.save(commit=False)
            mess.save()
            mess_added = True;
            mess_form = forms.MessForm()
    else:
        mess_form = forms.MessForm()

    return render(request,'hostel_app/add_mess.html',
                                {'mess_form':mess_form, 'mess_added':mess_added, 'is_warden':warden})

def warden_reg(request):
    pass

def mess_details(request):
    #student = Student.objects.all()
    mess = Mess.objects.raw('SELECT * FROM hostel_app_mess')
    
    clg = CollegeInfo.objects.raw('SELECT * FROM hostel_app_collegeinfo')
    context = {
        'mess_details':mess,
        'clg_list':clg
    }
    return render(request,'hostel_app/mess_details.html',
                            context=context)
def clg_info(request):
    pass
def warden_list(request):
    ward = wardenInfo.objects.raw('SELECT * FROM hostel_app_wardeninfo')
    
    clg = CollegeInfo.objects.raw('SELECT * FROM hostel_app_collegeinfo')
    context = {
        'warden':ward,
        'clg_list':clg
    }
    return render(request,'hostel_app/warden_list.html',
                            context=context)

def vehicle_list(request):
    veh = vehicle.objects.raw('SELECT * FROM hostel_app_vehicle')
    
    # clg = CollegeInfo.objects.raw('SELECT * FROM hostel_app_collegeinfo')
    context = {
        'veh_list':veh,
        # 'clg_list':clg
    }
    return render(request,'hostel_app/vehicle_list.html',
                            context=context)