*** Settings ***
Documentation	  Here's some standard examples of how to use Jama Integration

Default Tags      documentation

*** Test Cases ***
TC-GID-200747: Robot Addition Test Case
    [Documentation]
    ...     Description:
    ...     Verify that 1 + 2 = 3
    ...
    ...     Prerequisites:
    ...     1) This test is being run on a functional computer with proper logical operations
    ...
    ...     Test Data:
    ...     1) Numbers 1 and 2
    ...
    ...     Steps:
    ...     1) Perform 1 + 2
    ...         ER: 1 + 2 = 3
    ...         Notes: NA
    ...
    ...     Projects: SANBOX_BI

    # Test Setup
    ${ONE} =    Set Variable    ${1}
    ${TWO} =    Set Variable    ${2}
    ${SUM} =    Evaluate    ${ONE} + ${TWO}
    Should be Equal     ${SUM}  ${3}

TC-GID-200748: Robot Subtraction Test Case
    [Documentation]
    ...     Description:
    ...     Verify the difference of two numbers when subtracting one number by the other
    ...
    ...     Prerequisites:
    ...     1) This test is being run on a functional computer with proper logical operations
    ...
    ...     Test Data: NA
    ...
    ...     Steps:
    ...     1) Subtract a number from another number such as 3 - 2
    ...         ER: The user is able to subtract a number from another number
    ...         Notes: NA
    ...     2) Make an assumption about the difference of those numbers and evaluate the difference
    ...         ER: The difference is evaluated based on the user's assumption
    ...         Notes: Example: 3 - 2 = 1
    ...
    ...     Projects: SANBOX_BI

    # Test Setup
    ${ONE} =    Set Variable    ${1}
    ${TWO} =    Set Variable    ${2}
    ${SUM} =    Evaluate    ${TWO} - ${ONE}
    Should be Equal     ${SUM}  ${2}