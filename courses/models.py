from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Group

from h5p.models import H5PContent

from taggit.managers import TaggableManager

class Course(models.Model):
    title = models.CharField("Title",max_length=200, unique=True)
    certificate_title = models.CharField("Certificate Title",max_length=400,blank=True)
    is_enabled = models.BooleanField("Is Enabled",default=True)
    tags = TaggableManager()
    
class CourseVersion(models.Model):
    course = models.ForeignKey(Course,related_name="versions", on_delete=models.CASCADE)
    content = models.ForeignKey(H5PContent, blank=True, null=True, on_delete=models.CASCADE)
    year = models.CharField("Year",max_length=16)

    def __unicode__(self):
        return self.course.title + ' ' + self.year
    def __str__(self):
        return self.course.title + ' ' + self.year
    
STATUS_CHOICES = [
    ('started','Started'),
    ('passed','Passed'),
    ('failed','Failed'),
    ('completed','Completed'),
]

ORG_TYPE_CHOICES = [
    ('school','School'),
    ('municipality','Municipality'),
    ('private employer','Private Employer'),
]

EMP_TYPE_CHOICES = [
    ('professional','Professional'),
    ('non-professional','Non-professional'),
    ('default','Default'),
]

class Learner(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='learner', on_delete=models.CASCADE)
    job_title = models.CharField("Job Title",max_length=200, blank=True)
    employee_type = models.CharField("Employee Type",choices=EMP_TYPE_CHOICES,max_length=100, blank=True)

    @property
    def organization(self):
        group = self.user.groups.all().filter(organization__isnull=False).first()
        return group.organization

    def __unicode__(self):
        return self.user.first_name + ' ' + self.user.last_name
    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

    @classmethod
    def get_or_create(cls, user, organization):
        learner,created = cls.objects.get_or_create(user=user)
        if created:
            learner.user.groups.add(organization)
            learner.save()
            
        return learner
    
class CourseLearnerStatus(models.Model):
    course_version = models.ForeignKey(CourseVersion,related_name="course_status", on_delete=models.CASCADE)
    learner = models.ForeignKey(Learner,verbose_name="Learner",related_name="learner_status", on_delete=models.CASCADE)    
    status = models.CharField("Status",choices=STATUS_CHOICES,max_length=100,default="started")
    status_datetime = models.DateTimeField(default=timezone.now)
    start_datetime = models.DateTimeField(default=timezone.now)
    end_datetime = models.DateTimeField(null=True,blank=True)
    
class Organization(Group):
    org_type = models.CharField("Organization Type",choices=ORG_TYPE_CHOICES,max_length=100)
    training_year_start = models.DateField("Training Year Start")
    organization_password = models.CharField("Training Password",null=True,blank=True,max_length=256)
    billing_enabled = models.BooleanField("Billing Enabled",default=False)
    
class CourseLibrary(models.Model):
    title = models.CharField(max_length=200)

    def __unicode__(self):
        return self.title
    
class CourseLibraryCourse(models.Model):
    course_library = models.ForeignKey(CourseLibrary,related_name="courses", on_delete=models.CASCADE)
    course_version = models.ForeignKey(CourseVersion,related_name="libraries", on_delete=models.CASCADE)
    description = models.CharField(max_length=200,blank=True)
    sort_order = models.IntegerField(default=0)

    class Meta:
        unique_together = ('course_version','course_library')
    
class OrganizationCourseLibrary(models.Model):
    organization = models.ForeignKey(Organization,related_name="course_libraries", on_delete=models.CASCADE)
    course_library = models.ForeignKey(CourseLibrary,related_name="organization_library", on_delete=models.CASCADE)
    required = models.BooleanField(default=False)

    class Meta:
        unique_together = ('organization','course_library')
    
        
