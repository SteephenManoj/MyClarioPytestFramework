# 🤖 My Clario Automation Testing Framework

A comprehensive end-to-end automation framework for testing the GrowStack AI platform, covering AI functionalities, UI components, and robust backend integrations.

---

## 📌 Overview

This framework is designed to automate testing for the **GrowStack AI** platform, focusing on:

- AI chat interactions  
- Brand voice features  
- UI validations  
- User experience scenarios

Built with **Java**, **Selenium WebDriver**, **TestNG**, and **Cucumber**, the framework supports cross-browser and parallel testing with detailed reporting.

---

## 🧠 Key Features

- ✅ Page Factory Pattern (Page Object Model)  
- ✅ BDD Testing with Cucumber  
- ✅ Cross-browser Testing Support  
- ✅ Parallel Test Execution  
- ✅ Extent Reports for Comprehensive Reporting  
- ✅ Database Integration (PostgreSQL)  
- ✅ Excel-based Data Management (Apache POI)  
- ✅ Robust Error Handling and Logging  
- ✅ Dynamic Wait Mechanisms  

---

## 📂 Project Structure

```

GrowStackAI\_AutomationTesting/
├── src/
│   └── test/
│       ├── java/
│       │   ├── pageFactory/       # Page Object classes
│       │   ├── preRequisites/     # Setup/config classes
│       │   ├── runner/            # TestNG & Cucumber runners
│       │   ├── stepDefinition/    # Cucumber step definitions
│       │   └── uTility/           # Utilities and helpers
│       └── resources/
│           ├── features/          # Feature files
│           └── config/            # Configuration files
├── test-reports/                  # HTML & Cucumber reports
├── pom.xml                        # Maven dependencies
└── README.md                      # Project documentation

````

---

## ⚙️ Technology Stack

| Technology         | Version   | Purpose                     |
|--------------------|-----------|-----------------------------|
| Java               | 1.7+      | Core Programming Language   |
| Selenium WebDriver | 4.26.0    | Web Automation              |
| TestNG             | 7.10.2    | Test Execution Framework    |
| Cucumber           | 7.20.1    | BDD Testing Framework       |
| WebDriverManager   | 5.7.0     | Browser Driver Management   |
| Extent Reports     | 5.1.2     | HTML Reporting              |
| Apache POI         | 5.4.0     | Excel File Handling         |
| PostgreSQL         | 42.7.3    | Database Testing            |

---

## 🧪 Test Coverage

### 🤖 AI Features
- AI Command Prompt Testing  
- Audio Prompt Interactions  
- Response Validations  

### 🎯 UI Components
- Header & Footer Navigation  
- Brand Voice UI Integration  

### 🔒 User Experience
- Welcome Message Flow  
- Error Message Handling  
- Trial Limit Enforcement  

### 📑 Legal & Informational
- Terms of Service  
- Privacy Policy  
- Platform Information  

---

## 🚀 Getting Started

### ✅ Prerequisites

- Java JDK 1.7 or higher  
- Maven 3.x  
- Chrome / Firefox / Edge browsers  
- PostgreSQL (for DB validation)

---

### 📦 Installation

```bash
# Clone the repository
git clone https://github.com/your-org/GrowStackAI_AutomationTesting.git
cd GrowStackAI_AutomationTesting

# Install dependencies
mvn clean install
````

---

### 🧪 Running Tests

```bash
# Run all tests
mvn test

# Run specific suite
mvn test -Dsuite=testng.xml

# Run with specific browser
mvn test -Dbrowser=chrome
```

---

## 📊 Reporting

Reports are auto-generated in the `test-reports/` directory after test execution.

* ✅ Extent Reports (HTML)
* ✅ TestNG Reports
* ✅ Cucumber Reports (if using BDD)

---

## 🔧 Configuration Files

| File                | Purpose                           |
| ------------------- | --------------------------------- |
| `config.properties` | General test environment settings |
| `testng.xml`        | TestNG suite config               |
| `pom.xml`           | Maven dependencies and plugins    |

---

## 🛠️ Best Practices

### ✅ Page Object Model

* Use PageFactory pattern
* Keep methods reusable

### ✅ Test Data Management

* Use Excel + Apache POI
* Keep data externalized

### ✅ Error Handling

* Use explicit waits
* Log using try-catch
* Capture screenshots on failure

### ✅ Reporting

* Log every test step
* Capture screenshots on failure
* Use detailed assertions

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

---

## 📝 License

This project is **proprietary and confidential**. All rights reserved to **GrowStack Inc.**

---

## 👥 Team

* QA Automation Team
* GrowStack AI Development Team

---

## 📞 Support

For issues or queries, contact the QA team or raise an issue in this repository.

---

## 🔗 Project Status

🚧 **Active Development**
