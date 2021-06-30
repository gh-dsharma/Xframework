# Emmit Parubrub 2/11/2020 Jama Sync V1.0.0

*** Settings ***
Documentation	  Here's some standard examples of how to use Jama Integration

Default Tags      documentation

*** Test Cases ***
<NEW>: Test Documentation
    [Documentation]
    ...     Description:
    ...     The purpose of this test case is to test that Jama Sync is working properly
    ...
    ...     Prerequisites:
    ...     1) Testing Jama Sync writing in Prerequisites
    ...
    ...     Test Data:
    ...     1) Testing Jama Sync writing in Test Data
    ...
    ...     Steps:
    ...     1) Testing Jama Sync writing in Steps
    ...         ER: Testing Jama Sync writing in Expected Results
    ...         Notes: Testing Jama Sync writing in Notes
    ...
    ...     Projects: SANBOX_BI

    # Test Setup
    ${ONE} =    Set Variable    ${1}
    ${TWO} =    Set Variable    ${2}
    ${OUTPUT} =    Multiply two numbers     ${ONE}  ${TWO}
    Should Be Equal     ${OUTPUT}  ${2}

*** Keywords ***
# This keyword adds two numbers
Add two NUmbers
        [Arguments]    ${NUM1}      ${NUM2}
        ${SUM} =    Evaluate    ${NUM1} + ${NUM2}
        [Return]    ${SUM}

# This keyword multiplies two numbers
Multiply two numbers
        [Arguments]    ${NUM1}      ${NUM2}
        ${OUTPUT} =    Evaluate    ${NUM1} * ${NUM2}
        [Return]    ${OUTPUT}