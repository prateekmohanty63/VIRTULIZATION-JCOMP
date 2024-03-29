from django.contrib import admin

from appointment.models import Doctor,Hospital,DocReview,DocAppointment,HospitalReview,TempDoc,TempAppointment

# Register your models here.


# Register your models here.
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'Username', 'Email')

class DocReviewAdmin(admin.ModelAdmin):
    list_display= ('id','doctor','user','star_rating')
    
admin.site.register( Doctor)

# admin.site.register(User)

admin.site.register(Hospital)

admin.site.register(DocReview)

admin.site.register(DocAppointment)

admin.site.register(HospitalReview)

admin.site.register(TempDoc)

admin.site.register(TempAppointment)