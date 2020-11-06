from django import forms
from hostel_app.models import Student,Room,Hostel,CollegeInfo,Mess,wardenInfo,vehicle

from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username', 'password']
        help_texts = {
            'username': 'Same as hostel ID.',
        }

class StudentForm(forms.ModelForm):
    # room = forms.ModelChoiceField(queryset=Student.objects.filter(room__room_alloted=False))
    class Meta():
        model = Student
        fields = ('student_name','room','own_vehicle','mis_id','gender');

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.fields['room'].queryset = Room.objects.filter(room_alloted=False)
        # self.fields['mis_id'].queryset = CollegeInfo.objects.filter(room_alloted=False)

class VehicleForm(forms.ModelForm):
    class Meta():
        model = vehicle
        fields = ('vehicleno','licence','h_id')

class ClgForm(forms.ModelForm):
    class Meta():
        model = CollegeInfo
        fields = ('mis','email','phone_no','branch','batchof');

class RoomForm(forms.ModelForm):
    class Meta():
        model = Room
        fields = ['hostel','room_num','capacity']

class HostelForm(forms.ModelForm):
    class Meta():
        model = Hostel
        fields = ['hostel_name', 'warden','gender','mess']
class WardenForm(forms.ModelForm):
    class Meta():
        model = wardenInfo
        fields = ['name','email','phone_no','gender','slot']

class MessForm(forms.ModelForm):
    class Meta():
        model = Mess
        fields = ['mess_name' , 'mess_type','contractor','daily_fees']