from pytest_bdd import scenarios

# Import step definitions 
from src.test.step_definitions.login_steps import *
from src.test.step_definitions.signup_steps import *


# scenarios("../../resources/feature/login.feature")
scenarios("../../resources/feature/signup.feature")
