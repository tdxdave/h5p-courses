from django import forms
from django.core.exceptions import ValidationError

from .models import (
    CourseLibrary,
    Organization,
    OrganizationCourseLibrary
)


class LearnerLoginForm(forms.Form):
    organization = forms.ModelChoiceField(queryset=Organization.objects.all())
    email = forms.EmailField(required=False)
    skip_email = forms.BooleanField(required=False, widget=forms.CheckboxInput, label="I do not have an email address")
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(LearnerLoginForm, self).clean()
        if cleaned_data['password'] != cleaned_data['organization'].organization_password:
            self.add_error(None, ValidationError("Employer or Password entered was not correct. Please check your entry and try again."))

        if cleaned_data['email'] == "" and cleaned_data['skip_email'] is False:
            self.add_error(None, ValidationError('Please enter an email address or check "I do not have an email address" box.'))
        return cleaned_data


class LearnerSetupForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField(required=False)
    skip_email = forms.BooleanField(required=False, widget=forms.CheckboxInput, label="I do not have an email address")


class AdminLogin(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class AdminOrgCourseLibraryForm(forms.ModelForm):
    class Meta:
        model = OrganizationCourseLibrary
        fields = ('course_library', 'organization', 'required')
        widgets = {
            'organization': forms.HiddenInput()
        }

    def __init__(self, organization_id=None, *args, **kwargs):
        super(AdminOrgCourseLibraryForm, self).__init__(*args, **kwargs)
        if organization_id is not None:
            assigned_libs = CourseLibrary.objects.filter(organization_library__organization=organization_id)
            self.fields['course_library'].queryset = CourseLibrary.objects.exclude(id__in=assigned_libs)
