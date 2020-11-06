from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator 

# Create your models here.
class Student(models.Model):

    user = models.OneToOneField(User,max_length=7,on_delete=models.CASCADE)
    student_name = models.CharField(max_length=50)
    own = [('Y',"Yes"),('N',"No")]
    own_vehicle = models.CharField(choices=own, max_length=1, default='N')
    # hostel_b = models.ForeignKey("Hostel",on_delete=models.SET_NULL,null=True)
    room = models.ForeignKey("Room",on_delete=models.SET_NULL,null=True)
    mis_id = models.ForeignKey("CollegeInfo",null=False,on_delete=models.CASCADE,default='0000000')
    gender_choice = [('M',"Male"),('F',"Female")]
    gender = models.CharField(choices=gender_choice, max_length=1, default=None , null=False)
    
    def clean(self):
        if (self.gender and self.room != None):
            if self.gender != self.room.hostel.gender:
                raise ValidationError("Sorry. We don't offer mixed hostels.")
            if self.room.room_alloted==True:
                raise ValidationError('Room is already alotted.')
        # if Student.objects.filter(user__username__iexact=user.username).exists() :
        #     raise ValidationError("User already exists")
        # elif not re.match(r"[mbp]\d{6}[a-z][a-z]",str(user.username),re.I):
        #     print("Invalid Roll No")

    def __str__(self):
        return self.user.id
class vehicle(models.Model):
    vehicleno = models.CharField(max_length=20,primary_key=True)
    licence =  models.BigIntegerField(null=True)#on_delete=models.SET_NULL,null=True)
    h_id = models.ForeignKey("Student", on_delete=models.CASCADE)#, primary_key=True)#on_delete=models.CASCADE)
    
    def __str__(self):
        return vehicleno   


class CollegeInfo(models.Model):
    mis = models.CharField(unique=True, max_length=7, primary_key=True)
    
    email = models.CharField( max_length=50,null=True)#on_delete=models.SET_NULL,null=True)
    phone_no = models.BigIntegerField(null=True)#on_delete=models.SET_NULL,null=True)
    # branch = models.CharField(db_column='BRANCH', max_length=20,null=True)
    batchof = models.PositiveIntegerField(default=2023, validators=[MinValueValidator(2000), MaxValueValidator(2025)])

    # branch = models.ForeignKey("Branch",on_delete=models.SET_NULL,null=True)
    branch = models.CharField(max_length=25,null=True)

    def __str__(self):
        return self.mis

class Hostel(models.Model):

    hostel_name = models.CharField(max_length=25, primary_key=True)
    warden = models.ForeignKey("wardenInfo", on_delete=models.SET_NULL,null=True)
    gender_choice = [('M',"Male"),('F',"Female")]
    gender = models.CharField(choices=gender_choice, max_length=1, default=None)
    mess = models.OneToOneField("Mess", on_delete=models.SET_NULL,null=True)
    # rector = models.CharField(max_length=25)
    # b_phone_no = models.BigIntegerField(null=True)
    # totroom = models.IntegerField(default=0)
    def __str__(self):
        return self.hostel_name

class Mess(models.Model):
    mess_name = models.CharField(max_length=25,default="COEP-Mess")
    mess_type = models.CharField(max_length=50)
    contractor = models.CharField(max_length=50,null=True)
    daily_fees = models.IntegerField(null=True)

    def __str__(self):
        return self.mess_name

class Room(models.Model):

    hostel = models.ForeignKey("Hostel", on_delete=models.CASCADE)
    room_num = models.IntegerField()
    room_alloted = models.BooleanField(default=False)
    # capacity = models.IntegerField(min_value=1,max_value=4,default=1)
    capacity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(0), MaxValueValidator(1)])

    def __str__(self):
        ret_str = str(self.hostel) + "-" + str(self.room_num)
        return ret_str
        # return room_num
    class Meta:
        unique_together = ('hostel','room_num',)
        ordering = ['hostel','room_num']

# class Branch(models.Model):

#     branch_code = models.CharField(max_length=50,primary_key=True)
#     branch_name = models.CharField(max_length=50)
#     faculty = models.CharField(max_length=50)

    # def __str__(self):
    #     return self.branch_name
class wardenInfo(models.Model):
    name = models.CharField(unique=True, max_length=50, primary_key=True)
    email = models.CharField(max_length=50,null=True)#on_delete=models.SET_NULL,null=True)
    phone_no = models.BigIntegerField(null=True)#on_delete=models.SET_NULL,null=True)
    gender_choice = [('M',"Male"),('F',"Female")]
    gender = models.CharField(choices=gender_choice, max_length=1, default=None)
    # hostel = models.ForeignKey("Hostel",on_delete=models.SET_NULL,null=True)
    slot_c = [('M',"Morning"),('N',"Night")]
    slot = models.CharField(choices=slot_c, max_length=1, default=None)
    
    def __str__(self):
        return self.name
