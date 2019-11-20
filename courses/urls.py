from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic import TemplateView



from .views import (
    LearnerLoginView,
    LearnerSetupView,
    LearnerCourseDetail,
    LearnerCourseList,
    AdminCourseList,
    AdminCourseDetail,
    AdminCourseCreate,
    AdminCourseUpdate,
    AdminCourseDelete,
    AdminCourseVersionDetail,    
    AdminCourseVersionCreate,
    AdminCourseVersionUpdate,
    AdminCourseVersionDelete,
    AdminDashboardView,
    AdminOrgDetail,
    AdminOrgList,
    AdminOrgCreate,
    AdminOrgUpdate,
    AdminOrgCourseLibraryCreate,
    AdminOrgCourseLibraryDelete,    
    AdminCourseLibraryList,
    AdminCourseLibraryDetail,
    AdminCourseLibraryCreate,
    AdminCourseLibraryUpdate,
    AdminCourseLibraryDelete,
    AdminCourseLibraryCourseCreate,
    ReportLearnerList,
    ReportCourseLearnerStatusList,
    ReportOrgCourseLearnerStatusList,    
    ReportCourseList,
    course_status_update,
    org_course_library_required_toggle    
)

urlpatterns = [
    path("", TemplateView.as_view(template_name="homepage.html"), name="home"),
    path("admin/admin/", admin.site.urls),
    path("account/", include("account.urls")),
    path("login/", LearnerLoginView.as_view(), name="learner_login"),
    path("setup/", LearnerSetupView.as_view(), name="learner_setup"),
    path("dashboard/", LearnerCourseList.as_view(), name="learner_course_list"),
    path("course/<int:pk>/", LearnerCourseDetail.as_view(), name="learner_course_view"),    
    path("admin/", AdminDashboardView.as_view(), name="course_admin"),
    path("admin/courses/", AdminCourseList.as_view(), name="admin_course_list"),
   path("admin/courses/<int:pk>/", AdminCourseDetail.as_view(), name="admin_course_view"),    
    path("admin/courses/add/", AdminCourseCreate.as_view(), name="admin_course_create"),
    path("admin/courses/edit/<int:pk>/", AdminCourseUpdate.as_view(), name="admin_course_update"),
   path("admin/courses/<int:course_id>/versions/<int:pk>/", AdminCourseVersionDetail.as_view(), name="admin_courseversion_view"),
   path("admin/courses/<int:course_id>/versions/add/", AdminCourseVersionCreate.as_view(), name="admin_courseversion_create"),
   path("admin/courses/<int:course_id>/versions/edit/<int:pk>/", AdminCourseVersionUpdate.as_view(), name="admin_courseversion_update"),    
   
    path("admin/orgs/", AdminOrgList.as_view(), name="admin_org_list"),
    path("admin/orgs/add/", AdminOrgCreate.as_view(), name="admin_org_create"),
    path("admin/orgs/<int:pk>/", AdminOrgDetail.as_view(), name="admin_org_view"),
    path("admin/orgs/edit/<int:pk>/", AdminOrgUpdate.as_view(), name="admin_org_update"),
    path("admin/orgs/(<int:organization_id>/course-lib/add/", AdminOrgCourseLibraryCreate.as_view(), name="admin_org_course_library_create"),
    path("admin/orgs/(<int:pk>/course-lib/unassign/", AdminOrgCourseLibraryDelete.as_view(), name="admin_org_course_library_delete"),    
    path("admin/course-lib/", AdminCourseLibraryList.as_view(), name="admin_courselibrary_list"),
   path("admin/course-lib/(<int:pk>/", AdminCourseLibraryDetail.as_view(), name="admin_courselibrary_view"),    
    path("admin/course-lib/add/", AdminCourseLibraryCreate.as_view(), name="admin_courselibrary_create"),
    path("admin/course-lib/edit/<int:pk>/", AdminCourseLibraryUpdate.as_view(), name="admin_courselibrary_update"),
    path("admin/course-lib/add-course/<int:course_library_id>", AdminCourseLibraryCourseCreate.as_view(), name="admin_courselibrarycourse_create"),
    path("admin/orgs/<int:organization_id>/reports/learner-list/", ReportLearnerList.as_view(), name="admin_report_learner_list"),
    path("admin/learner/<int:learner_id>/course-status/", ReportCourseLearnerStatusList.as_view(), name="admin_course_learner_status_list"),
    path("admin/orgs/<organization_id>/courses/", ReportCourseList.as_view(), name="admin_report_course_list"),
    path("admin/orgs/<int:organization_id>/courses/<course_id>/learners/", ReportOrgCourseLearnerStatusList.as_view(), name="admin_report_org_course_learner_list"),    
    path("admin/course/<course_id>/status-update/", course_status_update, name="course_status_update"),
    path("admin/orgs/course-lib/<int:org_course_library_id>/toggle/", org_course_library_required_toggle, name="admin_org_course_library_toggle")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

