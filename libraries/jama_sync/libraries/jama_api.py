from py_jama_rest_client.client import JamaClient
from halo import Halo


class JamaClientHelper:
    """
    A class to reference the py_jama_rest_client api functions
    """
    def __init__(self, jama_url: str, username: str, password: str, default_test_case_type: int,
                 default_folder_type: int, default_status: int, default_test_case_status: str) -> None:
        """
        This class initializes the Jama Client and handles the API calls

        :jama_url: A string representing the url of the jama cloud to call the Jama API
        :username: A string representing the username of the person that is calling the Jama API
        :password: A string representing the password of the person that is calling the Jama API
        :default_test_case_type: An integer representing the default id for test case type (Jama API side)
        :default_status: An integer representing the default test case status for a test case (Jama API side)
        :default_test_case_status: A string representing the default status for a test case (Jama API side)
        """
        self.jama_client = JamaClient(host_domain=jama_url, credentials=(username, password), oauth=True)
        self.default_test_case_type = default_test_case_type
        self.default_folder_type = default_folder_type
        self.default_status = default_status
        self.default_test_case_status = default_test_case_status
        self.spinner = Halo(text='Waiting for Jama API', spinner='dots')

    def get_synced_items(self, test_case_id):
        """
        Return the API call for all synced (pushed) items. We want to separate this function call so that the code
        doesn't have strange redundancy like jama_client.jama_client.get_items_synceditems_status()

        Args:
            test_case_id: An integer representing a test case ID

        Returns: A json response from the Jama API
        """

        if not test_case_id:
            return []

        self.spinner.start("Retrieving synced items from Jama API")
        try:
            response = self.jama_client.get_items_synceditems(test_case_id)
        except Exception as e:
            print("\nUnable to find item's synced items:" + test_case_id + "\n" + str(e))
            return []
        self.spinner.stop()

        return response

    def get_synced_items_status(self, test_case_id, other_test_case_id):
        """
        Return the API call for the status of all synced (pushed) items. We want to separate this function call so
        that the code doesn't have strange redundancy like jama_client.jama_client.get_items_synceditems_status()

        Args:
            test_case_id: An integer representing the ID of the test case to compare against
            other_test_case_id: An integer representing the ID of the other test case

        Returns: A json response from the Jama API
        """
        self.spinner.start("Retrieving status of synced items from Jama API")
        try:
            response = self.jama_client.get_items_synceditems_status(test_case_id, other_test_case_id)
        except Exception as e:
            print("\n" + str(e))
            return -1
        self.spinner.stop()

        return response

    def get_project_id(self, project_name):
        """
        Return the project ID that matches with the project name that is passed as an argument

        Args:
            project_name: A string representing a JAMA project name

        Returns: An integer that indicates the project ID associated with the JAMA project
        """

        self.spinner.start("Retrieving project ID for " + project_name + " from Jama API")
        projects = self.jama_client.get_projects()
        self.spinner.stop()

        # Search through the projects available on Jama and find the matching name
        project_id = ''
        for project in projects:
            if isinstance(project, dict):
                if project_name == project['fields']['name'] and project['isFolder'] is False:
                    project_id = project['id']

        if project_id == '':
            raise Exception("No such JAMA project is named '" + project_name + "'")

        return project_id

    def get_test_case_id_from_global_id(self, project, project_id, global_id):
        """
        Return the test case id based upon project ID and the global ID

        Args:
            project: A string representing the project name of a JAMA project
            project_id: An integer representing the project ID of a JAMA project
            global_id: An integer representing the global ID of a test case

        Returns: An integer that represents the test case id of the test case
                 that has the same global id in the JAMA project that was passed in.
                 If there were no test case IDs, a -1 will be passed back
        """

        # Need to format this to have the expected GID that Jama has if the GID is in xframework standards (gid_1234)
        formatted_global_id = global_id.upper().replace("_", "-")

        self.spinner.start("Retrieving test case ID from Jama API")
        abstract_items = self.jama_client.get_abstract_items(project=[project_id], contains=[formatted_global_id])
        self.spinner.stop()

        if len(abstract_items) > 1:
            raise Exception("More than one test case with global id '" + global_id +
                            "' was found was found in project '" + project + "'")

        if abstract_items:
            for test_case in abstract_items:
                if test_case['globalId'] == formatted_global_id:
                    # Debugging print statement below
                    # print("Current fields: ", json.dumps(self.jama_client.get_abstract_items(
                    #     project=[project_id], contains=[formatted_global_id]), indent=4))
                    return test_case['id']
        else:
            return -1

    def get_folder_id(self, project_id, folder_path, project_name):
        """
        Return the folder id based upon the project and it's name

        Args:
            project_id: An integer representing the project's id to search in
            folder_path: A string representing the path from the root folder to the file
            project_name: A string representing the project that is being searched in

        Returns: An integer representing the id of the folder that was passed in
        """

        path_names = folder_path.split("/")
        root_folder = path_names.pop(0)
        parent = self.jama_client.get_abstract_items(project=project_id, contains=root_folder,
                                                     item_type=self.default_folder_type)

        if not parent:
            raise Exception("Could not find root folder named '" + root_folder + "' in project " + project_name)

        if len(parent) > 1:
            raise Exception("More than 1 root folder named '" + root_folder + "' is present in project " + project_name)

        parent_id = parent[0]['id']

        # Iterate through the children of the Jama items and create the new
        # folders if the folder has not been found in the children
        while len(path_names) > 1:
            next_parent_folder = path_names.pop(0)
            children = self.jama_client.get_item_children(parent_id)
            next_parent_folder_id = None

            for item in children:
                if next_parent_folder == item['fields']['name']:
                    next_parent_folder_id = item['id']

            if next_parent_folder_id:
                parent_id = next_parent_folder_id
            else:
                fields = {
                    'name': next_parent_folder
                }
                try:
                    parent_id = self.jama_client.post_item(project_id,
                                                           self.default_folder_type,
                                                           self.default_test_case_type,
                                                           parent_id,
                                                           fields)
                except Exception as e:
                    raise Exception("Could not create folder named '" +
                                    next_parent_folder + "' in project " + project_name)

        return parent_id

    def get_parent_id(self, test_case_id):
        """
        Return the parent id of a test case (needed for some API)

        Args:
            test_case_id: An integer representing the project ID of a JAMA project

        Returns: An integer that represents the parent id of the test case that was passed in
        """

        self.spinner.start("Retrieving parent ID from Jama API")
        try:
            response = self.jama_client.get_item(test_case_id)['location']['parent']['item']
        except Exception as e:
            print("\n" + str(e))
            return -1
        self.spinner.stop()

        return response

    def get_global_id(self, test_case_id):
        """
        Return the global id of a test case

        Args:
            test_case_id: An integer representing the test case id of a test case

        Returns: A string representing the global id of a test case
        """

        self.spinner.start("Retrieving global ID from Jama API")
        try:
            response = self.jama_client.get_item(test_case_id)['globalId']
        except Exception as e:
            print("\n" + str(e))
            return -1
        self.spinner.stop()

        return response

    def update_test_case(self, project, test_case):
        """
        Update a single test case

        Args:
            project: A string that represents the project that the test case needs to be updated in
            test_case: A TestCase object

        Returns: An integer representing the JAMA API response (e.g. 200 status for a successful update)
        """
        location = {"item": test_case.get_parent_id(project)}
        fields = self.assemble_add_update_fields(test_case)

        # print("Current fields: ", json.dumps(self.jama_client.get_abstract_items(
        #     project=[test_case.get_project_id(project)],contains=[test_case.get_test_case_id(project)]), indent=4))
        # print("New fields: ", json.dumps(fields, indent=4))

        # Call API to update test case
        self.spinner.start("Updating test case " + test_case.name + " in project " + project + " from Jama API")
        try:
            output = self.jama_client.put_item(test_case.get_project_id(project),
                                               test_case.get_test_case_id(project),
                                               self.default_test_case_type,
                                               self.default_test_case_type,
                                               location,
                                               fields)
        except Exception as e:
            print("\n" + str(e))
            return -1
        self.spinner.stop()

        return output

    def add_sync_link(self, project, test_case, master_test_case_id):
        """
        Update a single test case

        Args:
            project: A string that represents the project that the test case needs to be updated in
            test_case: A TestCase object
            master_test_case_id: A string that represents the test case id to sync the new test case with

        Returns: An integer that represents the JAMA API response (e.g. 200 status for a successful update)
        """

        location = {"item": test_case.get_parent_id(project)}
        fields = self.assemble_add_update_fields(test_case)

        # Call API to add a new test case to the project that we want to add it to. First add a test case to the
        # project with a temporary global id (placeholder) then sync the new test case (below). Currently we are
        # unable to make this in one call which will be problematic if the post_item call is successful but the
        # post_item_sync is unsuccessful. Emmit Parubrub has asked the Jama support team about how to approach this
        # and this is what the Jama support team advised him to do.
        try:
            self.spinner.start("Waiting for Jama API to add " + test_case.get_name() + " to project " + project)
            new_test_case_id = self.jama_client.post_item(test_case.get_project_id(project),
                                                          self.default_test_case_type,
                                                          self.default_test_case_type,
                                                          location,
                                                          fields,
                                                          global_id="AUTOMATION-GID-PLACEHOLDER-12345")
            self.spinner.stop()

        except Exception as e:
            self.spinner.stop()
            print("\nUnable to find the test case " + test_case.get_name() + " in project " + project + "\n" + str(e))
            return -1

        try:
            self.spinner.start("Waiting for Jama API to sync " + test_case.get_name() + " in project " + project)
            output = self.jama_client.post_item_sync(new_test_case_id, master_test_case_id)
            self.spinner.stop()
        except Exception as e:
            self.spinner.stop()
            print("\nUnable to sync test case " + test_case.get_name() + " in project " + project + "\n" + str(e))
            return -1

        return output

    def add_new_test_case(self, master_project, parent_id, test_case):
        """
        Add a new test case to the master project

        Args:
            master_project: A string representing the master JAMA project name
            parent_id: An integer representing parent item's id that the test case is added under
            test_case: A TestCase object

        Returns: An integer representing the id of the new test case that was added
        """

        location = {"item": parent_id}
        fields = self.assemble_add_update_fields(test_case)

        # Call API to add a new test case to the project that we want to add it to. First add a test case to the
        # project with a temporary global id (placeholder) then sync the new test case (below). Currently we are
        # unable to make this in one call which will be problematic if the post_item call is successful but the
        # post_item_sync is unsuccessful. Emmit Parubrub has asked the Jama support team and this is what the
        # Jama support team told him to do.

        try:
            self.spinner.start("Waiting for Jama API to add " + test_case.get_name() +
                               " to master project " + master_project)
            new_test_case_id = self.jama_client.post_item(self.get_project_id(master_project),
                                                          self.default_test_case_type,
                                                          self.default_test_case_type,
                                                          location,
                                                          fields)
            self.spinner.stop()
        except Exception as e:
            self.spinner.stop()
            print("\n" + str(e))
            return -1

        return new_test_case_id

    def assemble_add_update_fields(self, test_case):
        """
        Returns a formatted json for API calls that add/update with test case information

        Args:
            test_case: A TestCase object

        Returns: A json that contains the properly formatted fields that add/update Jama API requires
        """

        # TODO: Add character limits
        #  - some documentation goes off the page
        #  - there might be a char limit in json or in jama
        #  - what if characters go to the new line and code is expecting numbers? "1)"

        # Initialize the API values
        fields = {
            "name": test_case.get_name(),
            "description": test_case.get_description(),
            "prerequisite_steps$89": "",
            "testCaseSteps": [],
            "status": self.default_status,
        }

        # Separate prerequisites by the newline
        prerequisite_field = ""
        for prerequisite in test_case.get_prerequisites().split('\n\n'):
            prerequisite_field += "\n<p>" + prerequisite + "</p>\n"
        prerequisite_field += "\n<p>&nbsp;</p>\n"

        # If test case data is present, add the information to the prerequisites
        if test_case.get_test_data():
            prerequisite_field += "\n<p>Test Data:</p>\n"
            for test_data in test_case.get_test_data().split('\n\n'):
                prerequisite_field += "\n<p>" + test_data + "</p>\n"
        fields["prerequisite_steps$89"] = prerequisite_field

        # Append the test case steps as separate objects
        for step in test_case.get_steps():
            test_case_step = {
                "action": step.step_description,
                "notes": step.notes,
                "expectedResult": step.expected_result,
                "sub_steps": []
            }
            fields["testCaseSteps"].append(test_case_step)

        return fields


