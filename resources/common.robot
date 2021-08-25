*** Settings ***
Library    	            Selenium2Library
Library    	            PageObjectLibrary
Library    	            LoginPage
Library                 CampaignListPage
Library                 AdvertListPage
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

Go To Campaign List Page
    [Arguments]  ${user_id}    ${language}=${G_language}
    Go To Dynamic Page    CampaignListPage    ${user_id}    ${language}
    wait for page loading campaign

Go To Advert List Page
    [Arguments]    ${campaign_id}    ${language}=${G_language}
    [Documentation]
    ...
    ...    Should Login before go to advert list
    ...
    Go To Dynamic Page    AdvertListPage    ${campaign_id}    ${language}

Convert Date From dd.mm.yyyy to dd.mm.yy
    [Arguments]    ${src_date}    ${separator}=.
    ${date_slice}    Split String    ${src_date}    ${separator}
    ${year_converted}    Get Regexp Matches    ${date_slice[2]}    \\d{2}(\\d{2})    1
    ${target_date}    Set Variable    ${date_slice[0]}.${date_slice[1]}.${year_converted[0]}
    [Return]    ${target_date}