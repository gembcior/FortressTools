import os
import importlib.resources as resources

class FtBaseSettings:
    def __init__(self):
        self._name = None
        self._workspace = None
        self._project_template = None
        self._project_type = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value.strip()

    @property
    def workspace(self):
        return self._workspace

    @workspace.setter
    def workspace(self, value):
        workspace = os.path.expanduser(value)
        workspace = os.path.abspath(workspace)
        if os.path.exists(workspace):
            self._workspace = workspace
        else:
            raise Exception("Unable to set workspace property. Directory does not exist.")

    @property
    def project_template(self):
        return self._project_template

    @project_template.setter
    def project_template(self, value):
        with resources.path(__name__.split(".")[0] + ".templates.project." + self.project_type, value) as project_template_path:
            if os.path.exists(project_template_path):
                self._project_template = project_template_path
            else:
                raise Exception("Unable to set project_template property. File does not exist.")

    @property
    def project_type(self):
        return self._project_type

    @project_type.setter
    def project_type(self, value):
        self._project_type = value.strip()

    @property
    def project_directory(self):
        self._project_directory = os.path.join(self.workspace, self.name)
        return self._project_directory
