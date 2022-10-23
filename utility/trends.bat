@echo off
xcopy "..\\Reports\\allure-report\\history\\" "..\\Reports\\allure-results\\history\\" /e /i /h /y
xcopy "%~dp0\\environment.properties" "..\\Reports\\allure-results\\" /y
xcopy "%~dp0\\categories.properties" "..\\Reports\\allure-results\\" /y