from pytest_bdd import scenarios

from src.test.step_definitions.contact_steps import *

scenarios("../../resources/feature/contacts.feature")