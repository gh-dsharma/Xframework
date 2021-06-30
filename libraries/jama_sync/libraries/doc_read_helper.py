import html


def read_section(buf, new_test_case, section_name):
    # Read in section information and ensure that the information is documented correctly
    section_line = buf.readline()
    if section_name + ":" not in section_line:
        if section_name == "Description":
            raise Exception("Expecting '" + section_name + "' line in test case " + new_test_case.get_name() +
                            " (if this section is present, check that it is the first line in the doc-string)")
        else:
            raise Exception("Expecting '" + section_name + "' line in test case " + new_test_case.get_name() +
                            " or the previous section data (if this section is present, check that it is directly 2 "
                            "lines below the last section)")

    count = 1
    section_string = ""
    line = buf.readline().strip()
    while line != "":
        if not section_name == "Description":
            if not (line.startswith("-") or line.startswith(str(count) + ")") or line == "*begin table*"):
                raise Exception("Expecting either '" + str(count) + ")', another dash '-', or '*begin table*' "
                                "in the " + section_name + " section in " + new_test_case.get_name())
        if line == "*begin table*":
            table_section = []
            line = buf.readline().strip()
            while line != "" and line != "*end table*":
                table_section.append(filter_special_characters(line))
                line = buf.readline().strip()
            if line == "":
                raise Exception("Expecting '*end table*' in the " + section_name + " section in "
                                + new_test_case.get_name())
            else:
                # double /n for newline (split this in field assembly)
                section_string += "\n\n" + format_tables(table_section, new_test_case.get_name())
                line = buf.readline().strip()
        else:
            if not section_name == "Description":
                if line.startswith(str(count) + ")"):
                    count += 1
                section_string += "\n\n" + filter_special_characters(line)  # double /n for newline (split this in field assembly)
            else:
                section_string += "\n" + filter_special_characters(line)
            line = buf.readline().strip()
    return section_string


def read_step_section(buf, count, line, new_test_case, step_section_name):
    """
    Reads a step section and returns the data that was read

    Args:
        buf: buffer to read a line
        count: the line count for the step description
        line: the last line that was read
        new_test_case: the new test case object
        step_section_name: the name of the step section (e.g. step, ER, Notes)

    Returns: a tuple containing the step count, the last line that was read, and the step section string
    """
    step_section = line
    if step_section_name == "Steps":
        if not step_section.startswith(str(count) + ")"):
            raise Exception("Expecting '" + str(count) +
                            ")' line under 'Steps' in test case " + new_test_case.get_name())
        step_section = step_section.replace(str(count) + ")", "").strip()
        count += 1
    else:
        if not step_section.startswith(step_section_name + ":"):
            raise Exception("Expecting '" + step_section_name +
                            ":' line under 'Steps' in test case " + new_test_case.get_name())
        step_section = step_section.replace(step_section_name + ":", "").strip()

    next_line = buf.readline().strip()
    if next_line.startswith("-"):
        while next_line.startswith("-"):
            step_section += "\n" + next_line
            next_line = buf.readline().strip()

    # filter out the special characters
    step_section = filter_special_characters(step_section)

    return count, next_line, step_section


def format_tables(table_string_list, test_case_name):
    """
    Interprets a list of strings representing a table and returns a formatted string for Jama to create a table

    Args:
        table_string_list: A string list representing a table
        test_case_name: The name of the test case that this table belongs to

    Returns: a formatted string modified for Jama to create a table
    """
    if len(table_string_list) == 0:
        raise Exception("No rows provided in the table entered in " + test_case_name)

    # Get the column count for the table
    column_count = len(table_string_list[0].split("|"))

    return_string = "<p>&nbsp;</p><table border=\"1\" cellpadding=\"1\" " \
                    "cellspacing=\"0\" style=\"border-collapse:collapse; width:100%\">\n\t<tbody>"
    # uncomment to have an unset width (looks good in Jama but scrunched in Word)
    # "cellspacing=\"0\" style=\"border-collapse:collapse;\">\n\t<tbody>"
    # uncomment to have a set width (looks good in both Jama and Word but may cut out long text)
    # "cellspacing=\"0\" style=\"border-collapse:collapse; width:500px\">\n\t<tbody>"

    for table_string in table_string_list:
        if len(table_string.split("|")) != column_count:
            raise Exception("Table row: '" + table_string + "' does not have the expected amount "
                            "of columns:" + str(column_count) + " as the rest of the table in " + test_case_name)
        else:
            return_string += "\n\t\t<tr>"
            for i in table_string.split("|"):
                return_string += "\n\t\t\t<td>" + i.strip() + "</td>"
            return_string += "\n\t\t</tr>"

    return_string += "\n\t</tbody>\n</table><p>&nbsp;</p>"
    return return_string


def filter_special_characters(data_string):
    """
    Returns a formatted string that replaces special characters with strings that
    Jama interprets properly (html). This prevents Jama from reading these
    characters as html and instead provides them as their entity names. This
    function will continuously support special characters that need to be handled.
    More information can be found in the GQ-2006 Jira ticket.

    Currently handling the following characters/strings: (<), (>), (&), ("), (')

    Args:
        data_string: A string that will be used to upload information to Jama

    Returns: a formatted string that replaces brackets with strings that Jama interprets
    """
    return html.escape(data_string)
