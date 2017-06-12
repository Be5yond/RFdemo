*** Settings ***
Documentation     Test for invalid input
...               This testsuite covers 5 interfaces include:
...               playerpage.getUrl
...               getPushToken
...               getPushUrl
...               getActivityMachineState
...               streaminfo.search
Force Tags        low
Resource          conf.txt

*** Variables ***
${uid}            1

*** Test Cases ***
try get
    TRY    uid=${uid}
    Check Response By Path "args.default" Equals to "myarg"
    Check Response By Path "args.uid" Equals to "1"

get and check ok
    [Template]    TRY Get and Check Status Code
    a=2
    b=3
    c=4

*** Keywords ***
TRY Get and Check Status Code
    [Arguments]    &{args}
    TRY    &{args}
    check_status_code    ${200}
