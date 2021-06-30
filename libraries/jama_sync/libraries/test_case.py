class TestCase:
    """
    A class to pass information about a test case in jama_sync.py
    """
    def __init__(self, name, parent_folder_path):
        """
        TestCase initializer. Most information in the test case
        will be filled out after it is initialized

        :name: name or title of the test case (should start with a TC-GID-XXXXX)
        """
        self.name = name
        self.parent_folder_path = parent_folder_path
        self.description = ""
        self.prerequisites = ""
        self.test_data = ""
        self.steps = []
        self.projects = {}
        self.global_id = ""

    class Step:
        """
        A class that holds specific information about each step in a test case
        """
        def __init__(self, step_description, expected_result, notes):
            self.step_description = step_description
            self.expected_result = expected_result
            self.notes = notes

    class ProjectTrack:
        """
        A class that holds information about a test case depending on the project
        """
        def __init__(self, project_id, test_case_id, parent_id):
            self.project_id = project_id
            self.test_case_id = test_case_id
            self.parent_id = parent_id
            self.sync_status = None

    def add_step(self, step_description, expected_result, notes):
        """
        Creates a new step and adds it to the array of steps in a TestCase
        """
        new_step = self.Step(step_description, expected_result, notes)
        self.steps.append(new_step)

    def add_project(self, project):
        """
        Adds a project string (key) to the projects dictionary and
        initializes the value as None for now
        """
        self.projects[project] = None

    def add_project_track(self, project, project_id, test_case_id, parent_id):
        """
        Creates a new ProjectTrack and adds it as the value for
        a specified project in the projects dictionary
        """
        self.projects[project] = self.ProjectTrack(project_id, test_case_id, parent_id)

    def set_name(self, name):
        """
        Sets the name for the TestCase
        """
        self.name = name

    def set_description(self, description):
        """
        Sets the description for the TestCase
        """
        self.description = description

    def set_prerequisites(self, prerequisite):
        """
        Sets the prerequisites for the TestCase
        """
        self.prerequisites = prerequisite

    def set_global_id(self, global_id):
        """
        Sets the global id for the TestCase
        """
        self.global_id = global_id

    def set_test_data(self, test_data):
        """
        Sets the test data for the TestCase
        """
        self.test_data = test_data

    def set_parent_id(self, project, parent_id):
        """
        Sets the test parent id for a project track
        """
        self.projects[project].parent_id = parent_id

    def get_name(self):
        """
        Returns the name for the TestCase
        """
        return self.name

    def get_parent_folder_path(self):
        """
        Returns the parent folder path for the TestCase
        """
        return self.parent_folder_path

    def get_description(self):
        """
        Returns the description for the TestCase
        """
        return self.description

    def get_prerequisites(self):
        """
        Returns the prerequisites for the TestCase
        """
        return self.prerequisites

    def get_test_data(self):
        """
        Returns the test data for the TestCase
        """
        return self.test_data

    def get_steps(self):
        """
        Returns the steps for the TestCase
        """
        return self.steps

    def get_projects(self):
        """
        Returns the projects for the TestCase
        """
        return self.projects

    def get_global_id(self):
        """
        Returns the global id for the TestCase
        """
        return self.global_id

    def get_project_id(self, project):
        """
        Returns the project id for a specified project
        """
        return self.projects[project].project_id

    def get_test_case_id(self, project):
        """
        Returns the test case id for a specified project
        """
        return self.projects[project].test_case_id

    def get_parent_id(self, project):
        """
        Returns the parent id for a specified project
        """
        return self.projects[project].parent_id

    def get_project_name(self, project_id):
        """
        Returns the project name
        """
        for project in self.projects:
            if self.projects[project].project_id == project_id:
                return project
        return "(Could not find project name)"

    def __str__(self):
        """
        Returns string representation for print functions
        """
        string_representation = "*********************************************************************************"
        string_representation += "\n" + self.name + \
                                 "\n---Global ID---\n" + self.global_id + \
                                 "\n---Description---" + self.description + \
                                 "\n---Prerequisites---\n" + self.prerequisites.strip().replace("\n\n", "\n") + \
                                 "\n---Test Data--- " + self.test_data + "\n---Steps---\n"

        count = 1
        for step in self.steps:
            string_representation += "  " + str(count) + ") " + step.step_description + "\n" + \
                                     "      ER: " + step.expected_result + "\n" + \
                                     "      Notes: " + step.notes + "\n"
            count += 1

        string_representation += "---Projects---\n"

        for project, project_track in self.projects.items():
            if project_track:
                string_representation += project + " (id: " + str(project_track.test_case_id) + ") (parent_id: " + \
                                         str(project_track.parent_id) + ")\n"
            else:
                string_representation += project + " (NO TEST CASE IN THIS PROJECT)\n"

        string_representation += "*********************************************************************************\n\n"

        return string_representation
