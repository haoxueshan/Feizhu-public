# Feizhu-public
A Python-based automation system for retrieving order information and managing cookies from Feizhu platform.

The project supports automated browser login, cookie acquisition, order data extraction, and database storage.


## Project Structure

```
Feizhu-public
└── big-fish-feizhu-main
    ├── feizhu_unit
    │   ├── cookie2.txt          # Stored login cookie for Feizhu session
    │   ├── emaill.py            # Email notification module for error alerts
    │   └── sqlserver.py         # SQL Server database connection and operations
    │
    ├── google
    │   ├── ChromeSetup.exe      # Chrome browser installer
    │   ├── Firefox-latest.exe   # Firefox browser installer
    │   ├── chromedriver.exe     # Chrome WebDriver for Selenium automation
    │   ├── geckodriver.exe      # Firefox WebDriver
    │   ├── stealth.min.js       # Anti-detection script
    │   └── 驱动下载.txt          # Driver download instructions
    │
    ├── feizhu_cookie.py         # Script to obtain Feizhu login cookies
    ├── google_get_cookie.py     # Script to retrieve cookies through Google login
    ├── olderls.py               # Order list crawler
    ├── operate.py               # Business logic operations
    ├── orderinfo.py             # Order information processing
    ├── run.py                   # Main program entry point
    └── README.md
```
