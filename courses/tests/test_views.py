from django.test import RequestFactory

from ..test import MyTestCase
from ..views import LearnerLoginView


class TestHomeView(MyTestCase):
    """
    Test Home
    """

class TestLearnerLoginView(MyTestCase):
    """
    Test Learner Login
    """
    def setUp(self):
        self.org = self.create_org()
        self.learner = self.create_learner(self.org)
        
    def test_login_redirect(self):
        self.login(self.learner.user)

        response = self.get("learner_login", follow=True)
        self.assertRedirects(
            response, self.reverse("learner_course_list"), status_code=302, target_status_code=200
        )
        
