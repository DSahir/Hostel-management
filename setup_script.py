import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','hostel_management.settings')

import django
django.setup()

from hostel_app.models import Student,Room,Hostel,CollegeInfo,Mess,wardenInfo,vehicle
from django.contrib.auth.models import User

import random

NUMBER_OF_ROOMS = 5

# def add_branch():
#     branch_list = ['Computer Science','Electronics','Mechanical','Civil']
#     faculty_list = ['Saidalavi','Santiago','Jayaraj','George Varghese']

#     for index,branch_name in enumerate(branch_list):
#         branch_code = "A0"+str(index)
#         c = Branch.objects.get_or_create(branch_code=branch_code,branch_name=branch_name,faculty=faculty_list[index])[0]
#         c.save()

def add_mess():
    mess_type_list = ['Veg','Non Veg','Continental','North Indian','South Indian','Arabian','Thai','Chinese','Gujarathi']
    contractor_list = ['Babu P Raj','Sandeep Kumar','Vijay','Reshma','Susheela','Al Qatil','Lee Xang','B D Wong','Navaneeth Patel']
    daily_fees = [55,85,102,70,60,125,101,67,97]
    for index in range(len(mess_type_list)):
        m = Mess.objects.get_or_create(mess_type = mess_type_list[index], contractor = contractor_list[index],daily_fees=daily_fees[index])[0]
        m.save()

def add_clg():
    mis_list = ['1110001','1110002','1110003','1110004']
    
    batchof = [2020,2020,2022,2022]
    for index in range(len(mis_list)):
        m = CollegeInfo.objects.get_or_create(mis = mis_list[index],batchof=batchof[index])[0]
        m.save()


def add_hostel():
    messes = Mess.objects.all()
    vivan_hostel = Hostel.objects.get_or_create(hostel_name="Vivan",warden="Johny",gender="M",mess=messes[0])[0]
    shiv_hostel = Hostel.objects.get_or_create(hostel_name="Shiv",warden="Tommy",gender="M",mess=messes[1])[0]
    jijau_hostel = Hostel.objects.get_or_create(hostel_name="Jijau",warden="Salomi",gender="F",mess=messes[2])[0]
    riva_hostel = Hostel.objects.get_or_create(hostel_name="Riva",warden="Diana",gender="F",mess=messes[3])[0]

    vivan_hostel.save()
    shiv_hostel.save()
    jijau_hostel.save()
    riva_hostel.save()


def add_rooms():
    hostels = Hostel.objects.all()
    for hostel in hostels:
        for i in range(NUMBER_OF_ROOMS):
            room = Room.objects.get_or_create(hostel=hostel, room_num=i+1,room_alloted=False)[0]
            room.save()
def add_wardens():
    names = ['Avika','Amol','Vidya','Rima']
    emails = ['avika@mail.com','amol@mail.com','rawal23@mail.com','rwagh11@gmail.com']
    phones=[1234567890, 9876543210,5555544444,9999922222]
    gen=['F','M','F','F']
    slots=['M','N','M','N']
    
    for index in range(len(names)):
        m = wardenInfo.objects.get_or_create(name = names[index],email=emails[index],phone_no=phones[index],gender=gen[index],slot=slots[index])[0]
        m.save()
if __name__ == '__main__':
    print("Populating")
    # add_branch()
    add_mess()
    # add_hostel()
    add_rooms()
    add_clg()
    add_wardens()
    print("Populated")
    #Adding warden
    user=User.objects.create_user('chief_warden', password='warden@hostels')
    user.save()
    print("Added Warden")
