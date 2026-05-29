Feature: MyClario Login

Background:
 Given I open the MyClario application
 When I click the Get Started button

 @MC_LI_TC_003
  Scenario: Login with valid credentials
   When User has successfully landed on the login page
    And I login with valid credentials
    And I handle the timezone popup
    Then I should see the dashboard page
  @MC_LI_TC_004  
  Scenario: Login with invalid credentials
   When User has successfully landed on the login page
    And I login with invalid credentials
     Then I should see an error message
  @MC_LI_TC_005   
  Scenario: Login with empty credentials
   When User has successfully landed on the login page
   And I login with empty credentials
   Then verify that user still remains on the login page
  @MC_LI_TC_009
  Scenario: Verify password reset link is sent when user clicks Forgot Password after entering registered email
    When User has successfully landed on the login page
    And I enter a registered email address
    And I click the Forgot Password link
    Then I should see a confirmation message that the password reset link has been sent to the email address
  @MC_LI_TC_010
  Scenario: Verify error message is displayed when user clicks Forgot Password after entering unregistered email
    When User has successfully landed on the login page
    And I enter an unregistered email address
    And I click the Forgot Password link
    Then I should see an error message that the email address is not registered
  @MC_LI_TC_012
  Scenario: Verify that clicking Sign Up link redirects user to registration page correctly
    When User has successfully landed on the login page
    And I click the Sign Up link
    Then I should be redirected to the registration page        