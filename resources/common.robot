*** Settings ***
Library    	            Selenium2Library
Library    	            PageObjectLibrary
Library    	            LoginPage
Variables               current_env.py

*** Keywords ***
Open chrome
    [Arguments]     ${root}
    ${chrome options} =     Evaluate    sys.modules['selenium.webdriver'].ChromeOptions()    sys, selenium.webdriver
    Run keyword If  "${G_headless}" == "true"  Run keywords
    ...  Call Method    ${chrome options}   add_argument    headless
    ...  AND  Call Method    ${chrome options}   add_argument    disable-gpu
    Call Method    ${chrome options}    add_argument    disable-infobars
    Create Webdriver    Chrome    chrome_options=${chrome options}
    Run keyword If  "${G_headless}" == "true"  Set Window Size  1920  1080
    ...  ELSE
    ...  Maximize browser window
    Go to   ${root}

Logout
    Delete all cookies

Login To QC System
    [Arguments]    ${user}    ${password}    ${language}=${G_language}
    Go To Dynamic Page    LoginPage      ${language}
	Enter username 	${user}
	Enter password 	${password}
	Click the login button