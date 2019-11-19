from ..models import Learner, Organization

from ..test import MyTestCase

class TestLearnerMethods(MyTestCase):
    """
    Test methods on learner model
    """

    def setUp(self):
        self.org = self.create_org()
        self.learner = self.create_learner(self.org)


    def test_learner_org(self):
        self.assertIsInstance(self.learner.organization, Organization)
        self.assertIsInstance(self.learner, Learner)
        self.assertEqual(self.org,self.learner.organization)

        

        
