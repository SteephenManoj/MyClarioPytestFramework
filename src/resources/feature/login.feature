Feature: MyClario Login

  Scenario: Login with valid credentials
    Given I open the MyClario application
    When I click the Get Started button
    And I login with valid credentials
    And I handle the timezone popup
    Then I should see the dashboard page
  Scenario: Login with invalid credentials
    Given I open the MyClario application
    When I click the Get Started button
    And I login with invalid credentials
    Then I should see an error message