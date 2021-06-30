# Helper function to replace a section in a file
def replace_section_in_file(file_path: str, section: str, section_change: str, interpreter: str,
                            delete_section: bool = False):
    test_write = ""
    file = open(file_path, 'r')
    line = file.readline()
    while line:
        if line.strip() == section:
            if not delete_section:
                test_write += line

            if section_change:
                test_write += section_change + "\n\n"

            if interpreter == "xframework":
                while line.strip() != "":
                    line = file.readline()
            elif interpreter == "robot":
                while line.replace("...", "").strip() != "":
                    line = file.readline()
            elif interpreter == "gherkin":
                while line.strip() != "":
                    line = file.readline()
            else:
                raise Exception("Please provide a valid interpreter (gherkin, robot or xframework) instead of: " +
                                interpreter)
        else:
            test_write += line
        line = file.readline()
    file.close()

    with open(file_path, 'w') as file:
        for line in test_write:
            file.write(line)
    file.close()


# Helper function to standardize the file again
def standardize_file(file_path: str, standard_path: str):
    open(file_path, 'w').close()
    with open(standard_path) as standard:
        with open(file_path, "w") as file:
            for line in standard:
                file.write(line)
    standard.close()
    file.close()
