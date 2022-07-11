from django.contrib import admin
from operations import  models

# Register your models here.
admin.site.register(models.Session)
admin.site.register(models.Faculty)
admin.site.register(models.Department)
admin.site.register(models.Applicant)
admin.site.register(models.Student)
admin.site.register(models.Course)
admin.site.register(models.CourseRegistration)
admin.site.register(models.NotificationStudent)
admin.site.register(models.Role)
admin.site.register(models.Staff)

# admin.site.register()
# admin.site.register()
# admin.site.register()
# admin.site.register()
# admin.site.register()