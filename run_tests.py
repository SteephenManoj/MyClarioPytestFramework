#!/usr/bin/env python3
"""
Test Runner Script - Executes tests and organizes reports with datetime, suite name, and test IDs

Usage:
    python run_tests.py                              # Run all tests
    python run_tests.py test_mc_Login                # Run specific test file
    python run_tests.py test_mc_Login -v             # Verbose mode
    python run_tests.py --help                       # Show available options
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def run_tests(test_file=None, *pytest_args):
    """
    Execute pytest with organized report directory structure
    
    Directory structure created:
    reports/
    └── YYYY-MM-DD_HH-MM-SS_<test_suite_name>/
        ├── report.html                  ← HTML test report
        ├── allure-results/              ← Allure JSON data
        ├── allure-report/               ← Allure HTML dashboard
        ├── screenshots/                 ← Pass/fail screenshots
        │   ├── passed/
        │   └── failed/
        ├── logs/                        ← Test execution logs
        └── traces/                      ← Playwright traces
    """
    
    project_root = Path(__file__).parent
    
    # Build pytest command
    cmd = ["pytest"]
    
    # Add test file if specified
    if test_file:
        test_path = project_root / "src/test/tests" / f"{test_file}.py"
        if not test_path.exists():
            # Try without .py extension
            test_path = project_root / "src/test/tests" / f"{test_file}"
        cmd.append(str(test_path))
    else:
        cmd.append(str(project_root / "src/test/tests"))
    
    # Add remaining pytest arguments
    cmd.extend(pytest_args)
    
    # Print info
    print("=" * 80)
    print("TEST RUNNER - Organized Report Generation with Allure")
    print("=" * 80)
    print(f"Command: {' '.join(cmd)}")
    print(f"Project Root: {project_root}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    print()
    
    # Execute pytest
    result = subprocess.run(cmd, cwd=project_root)
    
    # Show report location info
    if result.returncode in [0, 1]:  # 0 = all passed, 1 = tests failed (but ran)
        print("\n" + "=" * 80)
        print("TEST EXECUTION COMPLETED")
        print("=" * 80)
        
        # Find latest report directory
        reports_dir = project_root / "reports"
        if reports_dir.exists():
            latest_report = max(
                reports_dir.glob("*_*/"),
                key=lambda p: p.stat().st_mtime,
                default=None
            )
            
            if latest_report:
                print(f"\n📁 Report Location: {latest_report.relative_to(project_root)}/")
                print("\n📊 Available Reports:")
                
                report_files = {
                    "HTML Report": latest_report / "report.html",
                    "Allure Results": latest_report / "allure-results",
                    "Allure Dashboard": latest_report / "allure-report" / "index.html",
                    "Screenshots (Passed)": latest_report / "screenshots" / "passed",
                    "Screenshots (Failed)": latest_report / "screenshots" / "failed",
                    "Test Logs": latest_report / "logs" / "test_execution.log",
                }
                
                for report_name, report_path in report_files.items():
                    exists = report_path.exists()
                    status = "✓" if exists else "✗"
                    print(f"  {status} {report_name:.<40} {report_path.relative_to(project_root) if exists else 'Not generated'}")
                
                print("\n🔗 View Reports:")
                if (latest_report / "report.html").exists():
                    print(f"  HTML Report: {latest_report.relative_to(project_root)}/report.html")
                if (latest_report / "allure-report" / "index.html").exists():
                    print(f"  Allure Dashboard: {latest_report.relative_to(project_root)}/allure-report/index.html")
                
                print("\n💡 Tips:")
                print(f"  • Open HTML report: start {latest_report.relative_to(project_root)}/report.html")
                print(f"  • View Allure: start {latest_report.relative_to(project_root)}/allure-report/index.html")
                print(f"  • Check logs: cat {latest_report.relative_to(project_root)}/logs/test_execution.log")
        
        print("\n" + "=" * 80)
    
    return result.returncode

if __name__ == "__main__":
    # Parse arguments
    test_file = None
    pytest_args = []
    
    if len(sys.argv) > 1:
        # First argument could be test file name
        first_arg = sys.argv[1]
        
        if first_arg in ["-h", "--help", "-v", "-vv", "-q"]:
            # It's a pytest argument
            pytest_args = sys.argv[1:]
        else:
            # Assume it's a test file
            test_file = first_arg
            pytest_args = sys.argv[2:]
    
    # Run tests
    exit_code = run_tests(test_file, *pytest_args)
    sys.exit(exit_code)
