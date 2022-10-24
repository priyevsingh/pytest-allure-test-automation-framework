---------------------------------------------------
README !!!
---------------------------------------------------
On Windows (Use path separator as \ )
On UNIX (Use path separator as / )

---------------------------------------------------
ALLURE REPORT USAGES -> https://docs.qameta.io/allure-report/
ALLURE LATEST RELEASES -> https://github.com/allure-framework/allure2/releases
---------------------------------------------------

STEPS TO SETUP:
    . Run command pip install -r requirements.txt
---------------------------------------------------
COMMANDS TO MANUALLY RUN TESTS AND GENERATE REPORT:
    . pytest --alluredir=.\Reports\allure-results --allure-severities normal,critical 
    (Optional cli arguments can be used as: --browser=firefox or --browser=edge , by default --browser=chrome)

    . allure generate allure-results --clean
    . Run trends.bat    (refer to workflow_allure.png   | source: https://medium.com/testvagrant/generating-allure-trendline-on-gitlab-pages-df01c8798ae2)

---------------------------------------------------
TEST SUITE RUN:
    . pytest --alluredir=.\Reports\allure-results --allure-severities normal,critical TestSuite\UI\
        For First Run: (there is no historical trend data)
            . Run report.py utility file.
            . Run trends.bat
        
        For Second Run: (historical trend data is available)
            . Run trends.bat    (to get previous run historical data)
            . Run report.py utility file.

    (Running with different browsers as cli options)
    . pytest --alluredir=.\Reports\allure-results --allure-severities normal,critical TestSuite\UI\ --browser=firefox
    . pytest --alluredir=.\Reports\allure-results --allure-severities normal,critical TestSuite\UI\ --browser=edge

---------------------------------------------------
INDIVIDUAL SUITE RUN:
    . pytest --alluredir=.\Reports\allure-results --allure-severities normal,critical TestSuite\UI\HomePage\

---------------------------------------------------
TEST CASE RUN:
    . pytest --alluredir=.\Reports\allure-results --allure-severities normal,critical TestSuite\UI\HomePage\test_HomePage.py::TestHomePage::test_google_feeling_lucky_feature

---------------------------------------------------
TAIL THE LIVE LOGS:
    On Windows (powershell):
        . cd <path-to-Reports-folder>
        For Test Logs:
        . Get-Content -Path .\logs\test.log -Wait
        For Report Generation Logs:
        . Get-Content -Path .\logs\gen_report.log -Wait
    
    On Unix-like (console):
        . cd <path-to-Reports-folder>
        For Test Logs:
        . tail -F ./logs/test.log
        For Report Generation Logs:
        . tail -F ./logs/gen_report.log
---------------------------------------------------