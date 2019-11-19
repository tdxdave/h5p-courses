from django.contrib import admin
from .models import (
    Course,
    CourseVersion,
    Learner,
    CourseLearnerStatus,
    Organization
)


class CourseVersionAdmin(admin.ModelAdmin):
    pass


class CourseAdmin(admin.ModelAdmin):
    pass


class LearnerAdmin(admin.ModelAdmin):
    pass


class CourseLearnerStatusAdmin(admin.ModelAdmin):
    pass


class OrganizationAdmin(admin.ModelAdmin):
    pass


admin.site.register(CourseVersion, CourseVersionAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Learner, LearnerAdmin)
admin.site.register(CourseLearnerStatus, CourseLearnerStatusAdmin)
admin.site.register(Organization, OrganizationAdmin)
