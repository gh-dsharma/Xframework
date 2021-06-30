

def test_gid_207146_tables():
    """
    Description:
        Truth table of %gene% %call% %level_3_detection%:
            *begin table*
            Gene   | call | hello | hi | testing | result
            CCND2  | 2    | hello | hi | testing | detected
            CDK4   | 2    | hello | hi | testing | detected
            FGFR2  | 2    | hello | hi | testing | detected
            *end table*

    Prerequisites:
        1) Truth table of %gene% %call% %level_3_detection%:
            *begin table*
            Gene   |  result
            CCND2  |  detected
            CDK4   |  detected
            FGFR2  |  detected
            *end table*

    Test Data:
        1) Truth table of %gene% %call% %copy_number% %zscore% %level_3_detection%:
            *begin table*
            PIK3CA | 2 | 2.39 | 15.09 |     detected | baseline
            PIK3CA | 2 | 3.39 | 16.09 |     detected | copy number and zscore both above requirement
            PIK3CA | 2 | 0    | 15.09 |     detected | copy number is 0 and zscore meets requirement
            PIK3CA | 2 | 2.39 | 0     |     detected | copy number is 2.39 and zscore is 0
            PIK3CA | 2 | NA   | NA    | not detected | copy number and zscore both NA
            PIK3CA | 1 | 2.39 | 15.09 | not detected | call is 1
            PIK3CA | 2 | 1.39 | 15.09 | not detected | copy number below requirement
            PIK3CA | 2 | 2.39 | 14.09 | not detected | zscore below requirement
            *end table*

    Steps:
        1) Add 1 + 2
            ER: The sum of 1 + 2 is 3
            Notes: NA

    Projects: SANBOX_BI
    """
    addition_sum = 1 + 2
    assert addition_sum == 3
