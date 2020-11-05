from django.contrib import admin

# Register your models here.
from hostel_app.models import Student,Room,Hostel,CollegeInfo,Mess,wardenInfo,vehicle

admin.site.register(Student)
admin.site.register(Hostel)
admin.site.register(Mess)
admin.site.register(Room)
admin.site.register(CollegeInfo)
admin.site.register(wardenInfo)
admin.site.register(vehicle)
# admin.site.register(Branch)
