import csv
import datetime
import calendar

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from django.contrib.auth.models import User

from .models import (
    Learner,
    Organization,
    CourseLearnerStatus
)


def import_learners():
    path = "courses_app/learners.csv"
    with open(path,'rU') as csvfile:
        r = csv.DictReader(csvfile,fieldnames=['org_name','email','full_name'])
        for row in r:
            name_parts = row['full_name'].split()
            if len(name_parts) != 2:
                continue
            first_name = name_parts[0]
            last_name = name_parts[1]
            try:
                org = Organization.objects.get(name=row['org_name'])
            except ObjectDoesNotExist:
                continue

            username = org.name + ' ' + first_name + ' ' + last_name
            if row['email'] != '':
                username = username + ' ' + row['email']
            try:
                user = User.objects.get(username = username, email=row['email'],groups__organization__name=row['org_name'],first_name=first_name,last_name=last_name)
            except ObjectDoesNotExist:
                try:
                    user = User.objects.create(username=username, email=row['email'],first_name=first_name,last_name=last_name)
                    user.groups.add(org)                
                    learner = Learner.objects.create(user = user)
                except:
                    pass


def populate_test_data():
    # loop over orgs
    orgs = Organization.objects.all()

    for org in orgs:
        # find their course library
        cl = org.course_libraries.all().first()
        if cl == None:
            continue
        # loop over their users
        users = User.objects.filter(groups__organization=org)
        months = (7,8,9,10,11,12,1,2,3,4,5,6)
        month_counter = 0
        days = (1,2,3,5,7,10,14,17,23,28,99)
        hours = (8,9,10,11,12)
        hour_counter = 0
        minutes = (0,12,24,36,48,59)
        minute_counter = 0
        durations = (3,15,29,58)
        duration_counter = 0
        day_counter= 0
        for user in users:
        # assign first course date from July 1 to June 30 2017
            learner = user.learner
            month = months[month_counter]
            month_counter=month_counter+1
            if month_counter == len(months):
                month_counter = 0
            day = days[day_counter]
            day_counter=day_counter+1
            if day_counter == len(days):
                day_counter = 0
            if month > 6:
                year = 2016
            else:
                year = 2017
            if day == 99:
                day = calendar.monthrange(year,month)[1]
                
            for course in cl.course_library.courses.all():
                hour = hours[hour_counter]
                hour_counter=hour_counter+1
                if hour_counter == len(hours):
                    hour_counter = 0
                minute = minutes[minute_counter]
                minute_counter=minute_counter+1
                if minute_counter == len(minutes):
                    minute_counter = 0
                status = "started"
                status_datetime = datetime.datetime(year,month,day,hour,minute)
                course_status_update(course.course,learner,status,status_datetime)
                status = "completed"
                duration = durations[duration_counter]
                duration_counter=duration_counter+1
                if duration_counter == len(durations):
                    duration_counter = 0
                minute = minute + duration
                if minute > 59:
                    minute = duration
                status_datetime = datetime.datetime(year,month,day,hour,minute)
                if duration > 3:
                    course_status_update(course.course,learner,status,status_datetime)

                    
def course_learner_status_update(course,learner,status,status_datetime=timezone.now):
    c_l_s,created = CourseLearnerStatus.objects.get_or_create(course_version=course,learner=learner)
    if created or status != c_l_s.status:
        c_l_s.status = status
        c_l_s.status_datetime = status_datetime
        if status == 'completed':
            c_l_s.end_datetime = status_datetime
    c_l_s.save()
    return c_l_s
