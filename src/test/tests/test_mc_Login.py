from pytest_bdd import scenarios

from src.test.step_definitions.login_steps import *


scenarios("../../resources/feature/login.feature")
