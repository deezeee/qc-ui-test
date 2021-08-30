*** Settings ***
Library             ToastMessageElement
Library             DateTime
Resource            common.robot
Resource            resources_create_new_campaign.robot
Variables           current_env.py

Suite Setup       Suite Setup For Small Native Infeed Banner
Suite Teardown    Suite Teardown For Small Native Infeed Banner

Test Teardown    Run Keyword If Test Failed    Capture Page Screenshot

*** Test Cases ***
C38598_Verify whether user can create a Small native in-feed banner campaign successfully with valid values
    [Tags]    testrailid=38598
    ${today}    Get Current Date    UTC    +7hours    %d/%m/%Y
    ${random_name}    Generate Random String    30    [LOWER][UPPER][NUMBERS][LETTERS]
    ${campaign_info}    Create New Small Native Infeed Banner Campaign
    ...    ${G_normal_user_id}    ${random_name}_Auto_created
    ...    ${today}    ${today}
    ...    ${G_daily_limit_type[1]}    ${Small_zen_min_daily_limit_budget.replace(',','')}
    ...    ${G_delivery_type[1]}    ${G_stats_tracking[1]}

*** Keywords ***
Suite Setup For Small Native Infeed Banner
    Open chrome    ${G_root_url}
    Login To QC System    ${G_normal_user_name}    ${G_normal_user_password}

Suite Teardown For Small Native Infeed Banner
    Logout
    Close All Browsers