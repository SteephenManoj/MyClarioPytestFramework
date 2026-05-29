Feature: MyClario Registration
Background:
  When User launces the MyClario application
  When User clicks on Create Account button

  # @TC_SIP_001
  # Scenario: Registering a new user with complete and valid details
  #   Given User is on the MyClario registration page
  #   When User enters the valid registration details
  #   Then Create Account button should be enabled
  #   When User clicks on Create account to submit the registration form
  #   Then User should navigate to Verify Your Email page

  @TC_SIP_002
  Scenario: Registering a new user with incomplete and valid details
    Given User is on the MyClario registration page
    When User does not enter the valid registration details
    Then We receive an error message indicating that email is required

  @TC_SIP_003
  Scenario: Verify duplicate email error message
    Given User is on the MyClario registration page
    When User enters duplicate email details
    And User enters the remaining details 
    When User clicks on Create Account submit button 
    Then Duplicate email error message should be displayed

  @TC_SIP_004
  Scenario: Verify Sign In link navigation 
    Given User is on the MyClario registration page
    When User clicks on Sign In link 
    Then User should navigate to Sign In page