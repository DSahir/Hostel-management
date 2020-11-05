from django.urls import path
from hostel_app import views

app_name = 'hostel_app'

urlpatterns = [
    path('register/',views.reg, name = "reg"),
    path('user_login/',views.user_login, name='user_login'),
    
    path('warden_register',views.warden_reg , name='warden_reg'),
    path('student_list/',views.StudentList, name='student-list'),
    path('hostel/',views.HostelList, name = 'hostel-list'),
    path('mess_details/',views.mess_details, name='mess-display'),

    path('hostel_details/',views.HostelWiseView, name='hostel-details'),
    path('hostel/student_list/',views.HostelStudentList, name='hostel-student-list'),
    path('profile/',views.StudentProfileView, name='student-details'),
    path('profile/edit',views.edit, name='edit-profile'),
    path('add_vehicle/',views.add_vehicle, name='add-vehicle'),
    path('warden_list/',views.warden_list, name='warden_list'),

    path('warden/add_room',views.add_room, name='warden-add-room'),
    path('warden/add_hostel',views.add_hostel, name='warden-add-hostel'),
    path('warden/add_mess',views.add_mess, name='warden-add-mess'),
    path('veh_list/',views.vehicle_list, name='vehicle_list'),

    path('clg_info/',views.clg_info, name='clg-form')


]
