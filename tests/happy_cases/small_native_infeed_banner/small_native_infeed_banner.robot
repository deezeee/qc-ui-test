*** Settings ***
Library             ToastMessageElement
Resource            common.robot
Variables           current_env.py

Suite Setup       Open chrome    ${G_root_url}
Suite Teardown    Run Keywords    Logout    Close All Browsers

*** Test Cases ***
Test
    Login To QC System    ${G_normal_user_name}    ${G_normal_user_password}