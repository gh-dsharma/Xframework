# Emmit Parubrub 2/11/2020 Jama Sync V1.0.0

*** Settings ***
Documentation	  Here's some standard examples of how to use Jama Integration

Default Tags      documentation

*** Test Cases ***
TC-GID-207193: Divide Test Case
    [Documentation]
    ...     Description:
    ...     Truth table of %gene% %call% %level_3_detection%:
    ...         *begin table*
    ...         Gene   | call | hello | hi | testing | result
    ...         CCND2  | 2    | hello | hi | testing | detected
    ...         CDK4   | 2    | hello | hi | testing | detected
    ...         FGFR2  | 2    | hello | hi | testing | detected
    ...         *end table*
    ...
    ...     Prerequisites:
    ...     1) Truth table of %gene% %call% %level_3_detection%:
    ...         *begin table*
    ...         Gene   |  result
    ...         CCND2  |  detected
    ...         CDK4   |  detected
    ...         FGFR2  |  detected
    ...         *end table*
    ...
    ...     Test Data:
    ...     1) Truth table of %gene% %call% %copy_number% %zscore% %level_3_detection%:
    ...         *begin table*
    ...         PIK3CA | 2 | 2.39 | 15.09 |     detected | baseline
    ...         PIK3CA | 2 | 3.39 | 16.09 |     detected | copy number and zscore both above requirement
    ...         PIK3CA | 2 | 0    | 15.09 |     detected | copy number is 0 and zscore meets requirement
    ...         PIK3CA | 2 | 2.39 | 0     |     detected | copy number is 2.39 and zscore is 0
    ...         PIK3CA | 2 | NA   | NA    | not detected | copy number and zscore both NA
    ...         PIK3CA | 1 | 2.39 | 15.09 | not detected | call is 1
    ...         PIK3CA | 2 | 1.39 | 15.09 | not detected | copy number below requirement
    ...         PIK3CA | 2 | 2.39 | 14.09 | not detected | zscore below requirement
    ...         *end table*
    ...
    ...     Steps:
    ...     1) Perform 2 / 1
    ...         ER: multiplication step runs smoothly
    ...         Notes: NA (other hello)
    ...     2) Check Result
    ...         ER: 2 / 1 = 2
    ...         Notes: NA
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