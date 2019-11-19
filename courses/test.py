from test_plus.test import CBVTestCase, TestCase

from django.conf import settings

from account.mixins import LoginRequiredMixin

from courses.models import Learner, Organization

class force_login(object):

    def __init__(self, testcase, user):
        self.testcase = testcase
        testcase.client.force_login(user)

    def __enter__(self):
        pass

    def __exit__(self, *args):
        self.testcase.client.logout()

class MyTestHelperMixin(object):
                        
    def login(self, user):
        """
        Force login to simulate checking credentials, avoiding password hashing
        algorithms and speed up tests.
        """
        return force_login(self, user)

    def create_learner(self,org):
        """ 
        create test learner
        """
        reg_user = self.make_user("reg_user")        
        return Learner.get_or_create(user=reg_user,organization=org)
                                      
    def create_org(self,
                   org_type="school",
                   name="test_org",
                   training_year_start="2017-07-01"):
        """
        Create organization for testing
        """
        return Organization.objects.create(org_type=org_type,
                                           name=name,
                                           training_year_start=training_year_start)
                        
class MyLoginRequired(object):

    def test_login_required(self):
        """
        Ensure view class inherits from LoginRequiredMixin
        """
        self.assertTrue(issubclass(self.get_view_class(), LoginRequiredMixin))

class MyTestCase(MyTestHelperMixin, TestCase):
    pass
                        
class MyCBVTestCase(MyTestHelperMixin, CBVTestCase):
    pass
