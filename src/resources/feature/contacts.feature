# contacts.feature
Feature: Contacts Module Functionality

  Background:
    Given user launches MyClario application
    When user logs into the application
    Then dashboard should be displayed

  @smoke @contact
  Scenario: MC_CN_TC_004 Verify at least one contact info required
    Given user navigates to Contacts page
    When user clicks on New Contact button
    And user enters mandatory contact details
    And user clicks on Create Contact button
    Then contact should be created successfully

  @regression
  Scenario: MC_CN_TC_016 Verify user can add professional information successfully
    Given user navigates to Contacts page
    When user opens Add Contact modal
    And user enters professional information
    And user saves the contact
    Then professional information should be saved successfully

  @regression
  Scenario: MC_CN_TC_017 Verify user can update professional information successfully
    Given professional information already exists
    When user updates professional information
    And user saves updated contact
    Then updated professional information should reflect correctly

  @smoke
  Scenario: MC_CN_TC_024 Verify successful contact creation
    Given user navigates to Contacts page
    When user clicks on New Contact button
    And user enters valid contact details
    And user clicks on Create Contact button
    Then contact should be created successfully

  @ui
  Scenario: MC_CN_TC_025 Verify cancel functionality
    Given user navigates to Contacts page
    When user clicks on New Contact button
    And user clicks Cancel button
    Then Add Contact modal should close successfully

  @ui
  Scenario: MC_CN_TC_026 Verify close icon functionality
    Given user navigates to Contacts page
    When user clicks on New Contact button
    And user clicks Close icon
    Then Add Contact modal should close successfully

  @regression
  Scenario: MC_CN_TC_027 Verify Download Template button works
    Given user navigates to Contacts page
    When user clicks Download Template button
    Then template file should download successfully

  @regression
  Scenario: MC_CN_TC_028 Verify Upload Excel button works
    Given user navigates to Contacts page
    When user uploads valid excel file
    Then contacts should be imported successfully

  @negative
  Scenario: MC_CN_TC_035 Upload Invalid file
    Given user navigates to Contacts page
    When user uploads invalid file format
    Then unsupported format validation message should display

  @regression
  Scenario: MC_CN_TC_039 Verify correct Excel data upload
    Given user navigates to Contacts page
    When user uploads valid excel data
    Then excel data should import correctly

  @edge
  Scenario: MC_CN_TC_041 Upload empty excel file
    Given user navigates to Contacts page
    When user uploads empty excel file
    Then empty file validation message should display

  @ui
  Scenario: MC_CN_TC_045 Verify upload modal close action
    Given user opens upload modal
    When user clicks upload modal close button
    Then upload modal should close successfully

  @regression
  Scenario: MC_CN_TC_046 Verify refresh icon
    Given user navigates to Contacts page
    When user clicks refresh icon
    Then latest contacts data should display

  @regression
  Scenario: MC_CN_TC_047 Verify Select Contacts to Merge enables selection mode
    Given user navigates to Contacts page
    When user clicks Select Contacts to Merge
    Then selection mode should enable successfully

  @regression
  Scenario: MC_CN_TC_049 Verify Review & Merge flow
    Given user selected duplicate contacts
    When user clicks Review and Merge
    Then review modal should open successfully

  @regression
  Scenario: MC_CN_TC_052 Verify merging of two contacts successfully
    Given user selected duplicate contacts
    When user merges selected contacts
    Then contacts should merge successfully

  @ui
  Scenario: MC_CN_TC_054 Verify switching between table and grid
    Given user navigates to Contacts page
    When user switches between table and grid view
    Then contacts should display correctly in both views

  @functional
  Scenario: MC_CN_TC_058 Verify summary cards display corresponding contacts correctly
    Given user navigates to Contacts page
    When user clicks Total Contacts card
    And user clicks Unique Contacts card
    And user clicks Need Review card
    Then corresponding contacts should display correctly

  @functional
  Scenario: MC_CN_TC_059 Verify switching between summary cards updates contacts dynamically
    Given user navigates to Contacts page
    When user switches between summary cards
    Then contacts list should update dynamically

  @smoke
  Scenario: MC_CN_TC_061 Verify search functionality
    Given user navigates to Contacts page
    When user searches valid contact name
    Then matching contacts should display

  @negative
  Scenario: MC_CN_TC_062 Verify no results case
    Given user navigates to Contacts page
    When user searches invalid keyword
    Then no contacts message should display

  @functional
  Scenario: MC_CN_TC_065 Verify More button displays additional filter options
    Given user navigates to Contacts page
    When user clicks More Filters button
    Then additional filters should display correctly

  @functional
  Scenario: MC_CN_TC_066 Verify contacts are filtered correctly
    Given user opens additional filters
    When user applies contact filters
    Then filtered contacts should display correctly

  @ui
  Scenario: MC_CN_TC_068 Verify additional filter dropdown closes properly
    Given additional filters dropdown is open
    When user clicks outside dropdown
    Then additional filters dropdown should close

  @functional
  Scenario: MC_CN_TC_069 Verify proper message for unavailable filter results
    Given no contacts match selected filter
    When user applies unavailable filter
    Then no matching contacts message should display

  @functional
  Scenario: MC_CN_TC_075 Verify options under 3 dots and navigation
    Given user navigates to Contacts page
    When user clicks 3 dots menu
    Then all menu options should display correctly

  @functional
  Scenario: MC_CN_TC_077 Verify updating contact details
    Given user opens Edit Contact page
    When user updates contact details
    And user clicks Update Contact button
    Then updated contact should display correctly

  @functional
  Scenario: MC_CN_TC_078 Verify delete confirmation popup
    Given user selects Delete Contact option
    When delete confirmation popup appears
    And user confirms deletion
    Then contact should delete successfully

  @functional
  Scenario: MC_CN_TC_080 Verify meeting creation functionality
    Given user opens Create Meeting modal
    When user enters mandatory meeting details
    And user clicks Create Meeting button
    Then meeting should create successfully

  @functional
  Scenario: MC_CN_TC_084 Verify user can add preparation checklist successfully
    Given user opens Preparation Checklist section
    When user adds checklist item
    Then checklist item should add successfully

  @functional
  Scenario: MC_CN_TC_086 Verify user can edit and delete checklist items successfully
    Given checklist items already exist
    When user edits checklist item
    And user deletes checklist item
    Then checklist item changes should reflect correctly

  @functional
  Scenario: MC_CN_TC_088 Verify delete confirmation popup for checklist task
    Given checklist item already exists
    When user deletes checklist item
    Then checklist delete confirmation popup should display

  @functional
  Scenario: MC_CN_TC_090 Verify user can add and view notes successfully
    Given user opens Notes section
    When user adds note
    Then note should save successfully

  @functional
  Scenario: MC_CN_TC_093 Verify user can edit and delete notes successfully
    Given notes already exist
    When user edits note
    And user deletes note
    Then notes changes should reflect correctly

  @functional
  Scenario: MC_CN_TC_094 Verify delete confirmation popup for note
    Given note already exists
    When user deletes note
    Then note delete confirmation popup should display

  @functional
  Scenario: MC_CN_TC_096 Verify user can create action point successfully
    Given user opens Action Points section
    When user creates action point
    Then action point should save successfully

  @functional
  Scenario: MC_CN_TC_098 Verify additional action point details validation
    Given user creates action point
    When user adds action point additional details
    Then additional action point details should save correctly

  @functional
  Scenario: MC_CN_TC_100 Verify user can mark action point completed and revert status
    Given action point already exists
    When user updates action point status
    Then action point status should update successfully

  @functional
  Scenario: MC_CN_TC_101 Verify filters display correct data and empty state message
    Given user opens Action Points page
    When user applies action point filters
    Then filtered action points should display correctly

  @functional
  Scenario: MC_CN_TC_102 Verify user can edit and update action point successfully
    Given action point already exists
    When user edits action point details
    Then updated action point should display correctly

  @functional
  Scenario: MC_CN_TC_103 Verify user can delete action point successfully
    Given action point already exists
    When user deletes action point
    Then action point should delete successfully

  @functional
  Scenario: MC_CN_TC_104 Verify delete and merge operations maintain data consistency
    Given notes and action points exist
    When user performs merge operation
    Then notes and action points should remain consistent

  @negative
  Scenario: MC_CN_TC_105 Verify merge operation maintains data consistency
    Given two contacts contain checklist notes and action points
    When user merges both contacts
    Then all checklist notes and action points should merge correctly

  @functional
  Scenario: MC_CN_TC_106 Verify tag addition
    Given user opens Manage Tags popup
    When user adds new tag
    Then tag should add successfully

  @functional
  Scenario: MC_CN_TC_107 Verify Manage Tags popup opens successfully
    Given user clicks Add Tags button
    Then Manage Tags popup should open successfully

  @functional
  Scenario: MC_CN_TC_108 Verify user can create a new tag successfully
    Given Manage Tags popup is open
    When user creates new tag
    Then new tag should display successfully

  @functional
  Scenario: MC_CN_TC_109 Verify existing tag can be assigned
    Given Manage Tags popup is open
    When user assigns existing tag
    Then assigned tag should display correctly

  @functional
  Scenario: MC_CN_TC_110 Verify assigned tag can be removed successfully
    Given assigned tag already exists
    When user removes assigned tag
    Then tag should remove successfully

  @functional
  Scenario: MC_CN_TC_111 Verify search functionality works for tags
    Given Manage Tags popup is open
    When user searches existing tag
    Then matching tags should display correctly

  @validation
  Scenario: MC_CN_TC_112 Verify system prevents duplicate tag creation
    Given Manage Tags popup is open
    When user enters duplicate tag name
    Then Add button should remain disabled

  @ui
  Scenario: MC_CN_TC_113 Verify Cancel button closes popup without saving changes
    Given Manage Tags popup is open
    When user clicks Cancel button
    Then Manage Tags popup should close without saving

  @functional
  Scenario: MC_CN_TC_114 Verify Save Changes button updates tag information correctly
    Given user updates tag changes
    When user clicks Save Changes button
    Then updated tag changes should reflect correctly

  @ai
  Scenario: MC_CN_TC_115 Verify fuzzy matching
    Given duplicate contacts exist
    Then system should flag duplicate contacts correctly

  @negative
  Scenario: MC_CN_TC_121 Verify duplicate email unique contact restriction validation
    Given duplicate contacts contain same email
    When user clicks Keep as Unique
    Then duplicate email validation message should display
