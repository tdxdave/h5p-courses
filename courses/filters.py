from django_filters import FilterSet
from .models import CourseLearnerStatus


class CourseLearnerStatusFilter(FilterSet):
    class Meta:
        model = CourseLearnerStatus
        fields = ['learner', 'course']
