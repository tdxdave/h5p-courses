import sys

from django.db.models import Value
from django.db.models.functions import Concat,Lower
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    TemplateView
)

from django.views.decorators.csrf import (
    csrf_exempt,
    csrf_protect
)

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages

from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic.edit import (
    FormView,
    CreateView,
    UpdateView,
    DeleteView
)

from django_tables2 import Column, Table, SingleTableMixin

from .models import (
    Learner,
    Course,
    CourseVersion,
    Organization,
    CourseLearnerStatus,
    CourseLibrary,
    CourseLibraryCourse,
    OrganizationCourseLibrary
)

from .forms import (
    AdminOrgCourseLibraryForm,
    LearnerLoginForm,
    LearnerSetupForm
)

from courses.utils import course_learner_status_update

class HomeView(TemplateView):
    template_name = "homepage.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('learner_course_list')
        return super(HomeView, self).get(self, request)

class LearnerLoginView(FormView):
    form_class = LearnerLoginForm
    template_name = "learner_login.html"
    success_url = reverse_lazy('learner_course_list')
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('learner_course_list')
        return super(LearnerLoginView, self).get(self, request)
    
    def form_valid(self, form):
        # find out if this person matches an existing user and
        # login or redirect to complete signup
        if form.cleaned_data['email'] != '':
            try:
                learner = Learner.objects.get(user__email=form.cleaned_data['email'],user__groups__organization=form.cleaned_data['organization'])
                login(self.request,learner.user)
                return redirect(self.get_success_url())
            
            except Learner.DoesNotExist:
                # fall through to learner setup
                # for new person
                pass
            
        self.request.session['login_in_progress'] = True
        self.request.session['organization'] = form.cleaned_data['organization'].id
        return redirect('learner_setup')

class LearnerSetupView(FormView):
    form_class = LearnerSetupForm
    template_name = "learner_setup.html"
    success_url = reverse_lazy('learner_course_list')

    def get(self, request):
        if not request.session['login_in_progress']:
            return redirect('/')
        if not request.session['organization']:
            return redirect('/')
        return super(LearnerSetupView, self).get(self, request)
    
    def form_valid(self, form):
        org = Organization.objects.get(id=self.request.session['organization'])
        username = org.name + ' ' + form.cleaned_data['first_name'] + ' ' + form.cleaned_data['last_name']
        if form.cleaned_data['email'] != '':
            username = username + ' ' +form.cleaned_data['email']

        user, created = User.objects.get_or_create(username = username, first_name = form.cleaned_data['first_name'], last_name = form.cleaned_data['last_name'], email = form.cleaned_data['email'])
        user.save()
        if created:
            learner = Learner.objects.create(user = user,organization = org)
            learner.save()
        else:
            learner = Learner.objects.get(user = user)
        login(self.request,user)            
        return redirect('learner_course_list')

@method_decorator(login_required, name='dispatch')
class LearnerCourseList(ListView):
    model = CourseVersion
    template_name = "course_list.html"
    context_object_name = "courses"

    def get_queryset(self):
        """
        Get all the courses a user can see.
        User could be staff, administrator
        or learner. Otherwise they can't see any courses.
        """
        if self.request.user.is_staff:
            return CourseVersion.objects.all()

        organization = self.request.user.learner.organization
        libraries = CourseLibrary.objects.filter(organization_library__organization=organization)
        return CourseVersion.objects.prefetch_related('course_status').filter(libraries__course_library__in=libraries)


class LearnerCourseDetail(DetailView):
    model=Course

# Admin Views

class AdminDashboardView(TemplateView):
    template_name = "admin/dashboard.html"

@method_decorator(login_required, name='dispatch')    
class AdminCourseDetail(DetailView):
    model=Course
    template_name = "admin/course_detail.html"
    
@method_decorator(login_required, name='dispatch')
class AdminCourseCreate(CreateView):
    model = Course
    fields = ['title','certificate_title','tags','is_enabled']
    success_url = reverse_lazy("admin_course_list")
    template_name = "admin/course_form.html"    
    
@method_decorator(login_required, name='dispatch')    
class AdminCourseUpdate(UpdateView):
    model = Course
    fields = ['title','certificate_title','tags','is_enabled']
    success_url = reverse_lazy("admin_course_list")
    template_name = "admin/course_form.html"
    
@method_decorator(login_required, name='dispatch')
class AdminCourseDelete(DeleteView):
    model = Course
    success_url = reverse_lazy("admin_course_list")
    template_name = "admin/course_delete_confirm.html"

@method_decorator(login_required, name='dispatch')    
class AdminCourseVersionDetail(DetailView):
    model=CourseVersion

@method_decorator(login_required, name='dispatch')    
class AdminCourseVersionCreate(CreateView):
    model = CourseVersion
    fields = ['course','year','content']
    success_url = reverse_lazy("admin_course_list")
    template_name = "admin/courseversion_form.html"    
    
@method_decorator(login_required, name='dispatch')    
class AdminCourseVersionUpdate(UpdateView):
    model = CourseVersion
    fields = ['course','year','content']
    success_url = reverse_lazy("admin_course_list")
    template_name = "admin/courseversion_form.html"
    
@method_decorator(login_required, name='dispatch')
class AdminCourseVersionDelete(DeleteView):
    model = CourseVersion
    success_url = reverse_lazy("admin_course_list")
    template_name = "admin/courseversion_delete_confirm.html"

@method_decorator(login_required, name='dispatch')
class AdminCourseList(ListView):
    model = Course
    template_name = "admin/course_list.html"
    context_object_name = "courses"

# Organization 
class AdminOrgDetail(DetailView):
    model = Organization
    template_name = "admin/org_view.html"

class AdminOrgList(ListView):
    model = Organization
    context_object_name = "orgs"
    template_name = "admin/org_list.html"
    
class AdminOrgCreate(CreateView):
    model = Organization
    template_name = "admin/org_form.html"
    fields = ['name','org_type','training_year_start','organization_password','billing_enabled']
    success_url = reverse_lazy("admin_org_list")
    
class AdminOrgUpdate(UpdateView):
    model = Organization
    template_name = "admin/org_form.html"
    fields = ['name','org_type','training_year_start','organization_password','billing_enabled']
    success_url = reverse_lazy("admin_org_list")

# CourseLibrary
@method_decorator(login_required, name='dispatch')
class AdminCourseLibraryCreate(CreateView):
    model = CourseLibrary
    fields = ['title']
    success_url = reverse_lazy("admin_courselibrary_list")
    template_name = "admin/courselibrary_form.html"
    
@method_decorator(login_required, name='dispatch')    
class AdminCourseLibraryUpdate(UpdateView):
    model = CourseLibrary
    fields = ['title']
    success_url = reverse_lazy("admin_courselibrary_list")
    template_name = "admin/courselibrary_form.html"    
    
@method_decorator(login_required, name='dispatch')
class AdminCourseLibraryDelete(DeleteView):
    model = CourseLibrary
    success_url = reverse_lazy("courselibrary_list")

    
@method_decorator(login_required, name='dispatch')
class AdminCourseLibraryList(ListView):
    model = CourseLibrary
    template_name = "admin/courselibrary_list.html"
    context_object_name = "course_libs"

    
class AdminCourseLibraryDetail(DetailView):
    model=CourseLibrary
    template_name = "admin/courselibrary_detail.html"

@method_decorator(login_required, name='dispatch')
class AdminCourseLibraryCourseCreate(CreateView):
    model = CourseLibraryCourse
    fields = ['course_library','course_version','description','sort_order']
    success_url = reverse_lazy("admin_courselibrary_list")
    template_name = "admin/courselibrarycourse_form.html"

@method_decorator(login_required, name='dispatch')
class AdminOrgCourseLibraryCreate(CreateView):
    model = OrganizationCourseLibrary
    form_class = AdminOrgCourseLibraryForm
    template_name = "admin/courses_app_form.html"

    def get_initial(self):
        data = super(AdminOrgCourseLibraryCreate, self).get_initial()
        data['organization'] = self.kwargs['organization_id']
        return data

    def get_form_kwargs(self):
        kwargs = super(AdminOrgCourseLibraryCreate, self).get_form_kwargs()
        kwargs.update(self.kwargs)
        return kwargs
    
    def form_valiid(self, form):
        orgcourselibrary = form.save(commit=False)
        orgcourselibrary.organization = self.kwargs['organization_id']
        orgcourselibrary.save()
        self.object = orgcourselibrary
        return redirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse_lazy('admin_org_view',kwargs={'pk':self.kwargs['organization_id']})

@method_decorator(login_required, name='dispatch')
class AdminOrgCourseLibraryDelete(DeleteView):
    model = OrganizationCourseLibrary
    template_name = "admin/org_course_library_delete_confirm.html"
    
    def get_success_url(self):
        obj = self.object
        org = self.object.organization
        return reverse_lazy('admin_org_view',kwargs={"pk":org.id})

@method_decorator(login_required, name='dispatch')
class ReportLearnerList(ListView):
    model = Learner
    context_object_name = "learners"

    def get_queryset(self):
        self.organization = get_object_or_404(Organization, id=self.kwargs['organization_id'])
        return Learner.objects.filter(user__groups__id=self.organization.id)

    def get_context_data(self):
        ctx = super(ReportLearnerList, self).get_context_data()
        ctx['organization'] = self.organization
        return ctx

class ReportCourseLearnerStatusList(ListView):
    model = CourseLearnerStatus
    context_object_name = "status"
    template_name = "admin/report_courselearnerstatus_list.html"
    def get_queryset(self):
        self.learner = get_object_or_404(Learner,id=self.kwargs['learner_id'])
        self.organization = self.learner.organization
        return CourseLearnerStatus.objects.filter(learner=self.learner)

    def get_context_data(self):
        ctx = super(ReportCourseLearnerStatusList, self).get_context_data()
        ctx['learner'] = self.learner
        ctx['organization'] = self.organization
        return ctx

class RTable(Table):
    class Meta:
        model = CourseLearnerStatus
        attrs = {'class': 'table table-striped'}
        per_page = 50
        fields = ['course','learner','status','status_datetime']

    learner = Column(order_by='full_name')

@method_decorator(login_required, name='dispatch')        
class ReportOrgCourseLearnerStatusList(SingleTableMixin,ListView):
    model = CourseLearnerStatus
    context_object_name = "status"
    table_class = RTable
    template_name = "admin/report_org_course_learner_list.html"
    def get_queryset(self):
        self.organization = get_object_or_404(Organization,id=self.kwargs['organization_id'])
        self.course = get_object_or_404(CourseVersion,id=self.kwargs['course_id'])
        return CourseLearnerStatus.objects.filter(course_version=self.course,learner__user__groups__organization=self.organization.id).annotate(full_name=Lower(Concat('learner__user__last_name',Value(' '),'learner__user__first_name')))

    def get_context_data(self):
        ctx = super(ReportOrgCourseLearnerStatusList, self).get_context_data()
        ctx['course'] = self.course
        ctx['organization'] = self.organization
        return ctx
    
# TODO Create some courses. Button to click that sets status. Test reports
# and billing

# when its all working, get the H5P stuff from MGH
@method_decorator(login_required, name='dispatch')
class ReportCourseList(ListView):
    model = Course
    context_object_name = "courses"
    template_name = "admin/report_course_list.html"

    def get_queryset(self):
        self.org = get_object_or_404(Organization, id=self.kwargs['organization_id'])
        self.course_libraries = CourseLibraryCourse.objects.filter(course_library__organization_library__organization=self.org)
        return CourseVersion.objects.filter(libraries__in=self.course_libraries)

    def get_context_data(self):
        ctx = super(ReportCourseList, self).get_context_data()
        self.organization = get_object_or_404(Organization, id=self.kwargs['organization_id'])
        ctx['organization'] = self.organization
        return ctx
        
        
def report_billing(request):
    return ""

def report_learner_certificate(request):
    return ""

@login_required
def course_status_update(request,course_id):
    if request.method == "POST":
        try:
            course = CourseVersion.objects.get(pk=course_id)
            learner = Learner.objects.get(user=request.user)
            status = request.POST.get('status')
            c_l_s = course_learner_status_update(course,learner,status,timezone.now())
            messages.info(request,course.course.title + ' ' + status)
        except courses_app.models.DoesNotExist as e:
            e = sys.exc_info()[0]
            messages.info(request,e)
        return redirect(reverse("learner_course_view",kwargs={'pk':course.id}))

@login_required
def org_course_library_required_toggle(request,org_course_library_id):
    if request.method == "GET":
        course_library = get_object_or_404(OrganizationCourseLibrary, id=org_course_library_id)
        try:
            required = not course_library.required
            course_library.required = required
            course_library.save()
            messages.info(request,"Course Library Updated " + str(required))
        except:
            e = sys.exc_info()[0]
            messages.info(request,e)
    return redirect(reverse("admin_org_view",kwargs={'pk':course_library.organization_id}))
