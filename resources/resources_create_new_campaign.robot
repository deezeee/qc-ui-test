*** Settings ***
Library    	            Selenium2Library
Library                 String
Library                 DateTime
Library                 BuiltIn
Library                 Collections
Library                 CampaignListPage
Library                 common
Resource                common.robot
Variables               current_env.py

*** Keywords ***
Create New Small Native Infeed Banner Campaign
    [Arguments]
    ...    ${user_id}   ${name}
    ...    ${period_from}=${EMPTY}    ${period_to}=${EMPTY}
    ...    ${daily_limit}=${EMPTY}    ${max_daily_limit}=${EMPTY}
    ...    ${delivery_type}=${EMPTY}    ${stats_tracking}=${EMPTY}
    Go To Campaign List Page    ${user_id}
    Click Create Campaign Button
    Select Where You Want To Display Your Ads    ${Small_zen_location}
    Select The Position Of Your Ads    ${Small_zen_position}
    Select Campaign Type    ${Small_zen_campaign_type}
    Input Campaign Name    ${name}
    Input Campaign Period    ${period_from}    ${period_to}
    Run Keyword If    '${daily_limit}'!='${EMPTY}'    Select Daily Limit Type    ${daily_limit}
    Run Keyword If    '${daily_limit}'=='${G_daily_limit_type[1]}'    Input Daily Limit    ${max_daily_limit}
    Run Keyword If    '${delivery_type}'!='${EMPTY}'    Select Delivery Type    ${delivery_type}
    Run Keyword If    '${stats_tracking}'!='${EMPTY}'    Select Stats Tracking    ${stats_tracking}
#    Verify error message
    ${campaign_id}    ${error_message}    Click Create Campaign Save Button
    FOR    ${key}    IN    @{error_message}
        Should Be Empty    ${error_message}[${key}]
    END
#    Verify infomation
    Go To Advert List Page    ${campaign_id}
    ${campaign_info}    Get Campaign All Info
    Set To Dictionary    ${campaign_info}    campaign_id=${campaign_id}
    Should Match Regexp    ${campaign_info}[campaign_name]    ${name}\\s+-\\s+[\\d|\\w]+
    ${current_date}    Get Current Date    UTC    +7hours    %d.%m.%Y
    ${date_from}    Run Keyword If    '${period_from}'=='${EMPTY}'
    ...    Convert Date From dd.mm.yyyy to dd.mm.yy    ${current_date}
    ...    ELSE    Convert Date From dd.mm.yyyy to dd.mm.yy    ${period_from.replace('/','.')}
    Should Be Equal    '${campaign_info}[campaign_from]'    '${date_from}'
    ${date_to}    Run Keyword If    '${period_to}'!='${EMPTY}'
    ...    Convert Date From dd.mm.yyyy to dd.mm.yy    ${period_to.replace('/','.')}
    ...    ELSE    Set Variable    None
    Should Be Equal    '${campaign_info}[campaign_to]'    '${date_to}'
    ${en_status}    Run Keyword And Return Status    Should Be Equal    '${campaign_info}[campaign_status]'    'Active'
    ${vi_status}    Run Keyword And Return Status    Should Be Equal    '${campaign_info}[campaign_status]'    'Đang hoạt động'
    Should Be True    '${en_status}'=='${True}' or '${vi_status}'=='True'
    ${en_type}    Run Keyword And Return Status    Should Be Equal    '${campaign_info}[campaign_type]'    'Small Native In-feed Banner'
    ${vi_type}    Run Keyword And Return Status    Should Be Equal    '${campaign_info}[campaign_type]'    'Quảng Cáo Nội Dung Tự Nhiên'
    Should Be True    '${en_type}'=='${True}' or '${vi_type}'=='True'
    Should Be Equal    '${campaign_info}[campaign_delivery_type]'    '${delivery_type}'
    Should Be Equal    '${campaign_info}[campaign_stats_tracking]'    '${stats_tracking}'
    Should Be Equal    '${campaign_info}[campaign_payment_type]'    '${Small_zen_payment_type}'
    ${daily_limit_currency}    Convert Number To Currency    ${max_daily_limit}    ${SPACE}
    ${daily_limit_en}    Set Variable    ${daily_limit_currency}${SPACE}VND/day
    ${daily_limit_vi}    Set Variable    ${daily_limit_currency}${SPACE}VNĐ/ngày
    Should Be True    '${daily_limit_en}'=='${campaign_info}[campaign_daily_limit]' or '${daily_limit_vi}'=='${campaign_info}[campaign_daily_limit]'

    [Return]    ${campaign_info}

Get Campaign Info In Campaign List By Id
    [Arguments]    ${user_id}    ${campaign_id}
    Go To Campaign List Page    ${user_id}

