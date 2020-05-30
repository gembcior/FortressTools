import os

class FtBaseSettings:
    def __init__(self):
        self._name = None
        self._workspace = None
        self._templates = None
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
    def templates(self):
        return self._templates

    @templates.setter
    def templates(self, value):
        templates = os.path.expanduser(value)
        templates = os.path.abspath(templates)
        if os.path.exists(templates):
            self._templates = templates
        else:
            raise Exception("Unable to set templates property. Directory does not exist.")

    @property
    def project_template(self):
        return self._project_template

    @project_template.setter
    def project_template(self, value):
        project_template = os.path.join(self.templates, "project", value)
        if os.path.exists(project_template):
            self._project_template = project_template
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
