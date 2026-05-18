# 🤖 MyClario Automation Testing Framework (Python + Playwright)

A comprehensive end-to-end automation framework for testing the **MyClario** platform, covering core modules including Dashboard, Contacts, Travel, Meeting, Action Items, Agents, and On-Behalf functionalities with robust UI and backend integrations.

---

## 📌 Overview

This framework is designed to automate testing for the **MyClario** platform, focusing on:

- Dashboard analytics and data validation  
- Contact management operations  
- Travel booking and itinerary workflows  
- Meeting scheduling and management  
- Action item tracking and completion  
- AI Agent interactions and configurations  
- On-Behalf delegation and permissions  

Built with **Python**, **Playwright**, and **pytest**, the framework supports **cross-browser**, **parallel**, and **headless/headed** execution with detailed reporting and hybrid test design.

---

## 🧠 Key Features

- ✅ Page Object Model (Modular & Reusable)
- ✅ Hybrid Framework (supports both procedural & BDD-style tests)
- ✅ Cross-browser Testing (Chrome, Firefox, Edge, WebKit)
- ✅ Parallel Test Execution (pytest-xdist)
- ✅ Allure / pytest-html Reporting
- ✅ Database Integration (PostgreSQL with psycopg2)
- ✅ Excel-based Test Data Management (openpyxl / pandas)
- ✅ Environment Configuration (.env / config.yaml)
- ✅ Robust Error Handling & Screenshots on Failure
- ✅ Smart Waits (Playwright's auto-waiting & retries)
- ✅ CI/CD Ready (GitHub Actions / GitLab CI / Jenkins)

---

## 📂 Project Structure
MyClario_AutomationTesting/
├── pages/ # Page Object Model classes
│ ├── base_page.py
│ ├── dashboard_page.py
│ ├── contacts_page.py
│ ├── travel_page.py
│ ├── meeting_page.py
│ ├── action_items_page.py
│ ├── agents_page.py
│ └── on_behalf_page.py
├── tests/ # Test modules per feature
│ ├── test_dashboard.py
│ ├── test_contacts.py
│ ├── test_travel.py
│ ├── test_meeting.py
│ ├── test_action_items.py
│ ├── test_agents.py
│ └── test_on_behalf.py
├── utilities/ # Helpers & utilities
│ ├── config_reader.py
│ ├── excel_handler.py
│ ├── db_handler.py
│ ├── logger.py
│ ├── screenshot_util.py
│ └── date_utils.py
├── fixtures/ # pytest fixtures & setup/teardown
│ └── conftest.py
├── data/ # Test data (Excel, JSON, YAML)
│ ├── contacts_test_data.xlsx
│ ├── travel_test_data.xlsx
│ ├── users.json
│ └── config.yaml
├── reports/ # HTML & Allure reports
├── logs/ # Log files
├── requirements.txt # Python dependencies
├── pytest.ini # pytest configuration
├── .env # Environment variables
└── README.md
---

## ⚙️ Technology Stack

| Technology          | Version     | Purpose                         |
|---------------------|-------------|---------------------------------|
| Python              | 3.9+        | Core Programming Language       |
| Playwright          | 1.40+       | Web Automation                  |
| pytest              | 7.4+        | Test Execution Framework        |
| pytest-xdist        | Latest      | Parallel Execution              |
| allure-pytest       | Latest      | Advanced Reporting              |
| pytest-html         | Latest      | HTML Reports                    |
| openpyxl / pandas   | Latest      | Excel File Handling             |
| psycopg2-binary     | Latest      | PostgreSQL Database Testing     |
| python-dotenv       | Latest      | Environment Variable Management |
| pyyaml              | Latest      | YAML Config Parsing             |
| faker               | Latest      | Test Data Generation            |

---

## 🧪 Test Coverage by Module

### 📊 Dashboard Module
- Analytics data validation (charts, KPIs)
- Widget loading and refresh
- Date range filters
- Data accuracy verification

### 👥 Contacts Module
- Create, edit, delete contacts
- Search and filter functionality
- Contact details validation
- Bulk import/export operations
- Contact tagging and categorization

### ✈️ Travel Module
- Flight / hotel / car booking flows
- Itinerary creation and management
- Travel preferences validation
- Booking modifications and cancellations
- Travel expense tracking

### 📅 Meeting Module
- Schedule, reschedule, cancel meetings
- Calendar integration
- Invite attendees and track RSVPs
- Meeting reminders and notifications
- Recurring meeting setup

### ✅ Action Items Module
- Create, assign, and track tasks
- Priority and due date management
- Status updates (pending, in-progress, completed)
- Action item reminders
- Completion verification

### 🤖 Agents Module
- AI Agent configuration
- Agent response validation
- Agent permissions and access control
- Agent activity logging
- Integration with other modules

### 🔄 On Behalf Module
- Delegate permissions to users
- Act on behalf of other users
- Access control validation
- Audit trail verification
- Revoke delegation

---

## 🚀 Getting Started

### ✅ Prerequisites

- Python 3.9 or higher  
- pip (Python package manager)  
- Playwright browsers installed  
- PostgreSQL (optional, for DB validation)

### 📦 Installation

```bash
# Clone the repository
git clone https://github.com/your-org/MyClario_AutomationTesting.git
cd MyClario_AutomationTesting

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install

🧪 Running Tests
# Run all tests
pytest

# Run specific module tests
pytest tests/test_contacts.py
pytest tests/test_travel.py

# Run with specific browser
pytest --browser=chromium      # or firefox, webkit

# Run in headed mode (visible browser)
pytest --headed

# Run tests in parallel (4 workers)
pytest -n 4

# Run specific test marker
pytest -m "smoke"
pytest -m "regression"

# Run with HTML report
pytest --html=reports/report.html

# Run with Allure report
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
🏷️ Available Test Markers
Marker	Description
@pytest.mark.smoke	Critical path tests
@pytest.mark.regression	Full regression suite
@pytest.mark.dashboard	Dashboard module tests
@pytest.mark.contacts	Contacts module tests
@pytest.mark.travel	Travel module tests
@pytest.mark.meeting	Meeting module tests
@pytest.mark.action_items	Action Items module tests
@pytest.mark.agents	Agents module tests
@pytest.mark.on_behalf	On Behalf module tests
📊 Reporting
Reports are auto-generated in the reports/ directory.

✅ pytest-html – Simple HTML reports

✅ Allure – Rich, interactive reports with test steps

✅ Console output – Real-time test logs

✅ Screenshots – Automatically captured on test failures

🔧 Configuration Files

File	Purpose
.env	Environment variables (URLs, credentials)
config.yaml	Framework settings (browsers, timeouts)
pytest.ini	pytest markers, filters, default args
requirements.txt	Python dependencies

Sample .env file

BASE_URL=https://staging.myclario.com
ADMIN_USERNAME=admin@myclario.com
ADMIN_PASSWORD=secure_password
DB_HOST=localhost
DB_NAME=myclario_db
DB_USER=postgres
DB_PASSWORD=postgres

🛠️ Best Practices
✅ Page Object Model
Each page/feature = one class

Locators & actions inside page classes

BasePage for common functions

✅ Test Data Management
Externalize data using Excel / JSON / YAML

Use data/ folder for test data files

Generate dynamic test data using Faker library

✅ Error Handling & Debugging
Playwright's auto-waiting reduces flakiness

Screenshots captured automatically on failures

Logging via Python's logging module

✅ Parallel & Cross-browser
Use pytest-xdist for parallel execution

Define browser fixtures in conftest.py

Module-level isolation to avoid test interference

🤝 Contributing
Fork the repository

Create a feature branch (git checkout -b feature/new-test)

Commit your changes

Push to the branch

Open a pull request

Code Standards
Follow PEP 8 guidelines

Add docstrings for all page methods

Update test markers in pytest.ini when adding new modules

📝 License
This project is proprietary and confidential. All rights reserved to MyClario.

👥 Team
QA Automation Team

MyClario Development Team

📞 Support
For issues or queries, contact the QA team or raise an issue in this repository.

🔗 Project Status
🚧 Active Development – Continuously adding test coverage for all modules
