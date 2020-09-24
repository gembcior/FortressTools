from .base_project import FtBaseProject
import os

class FtPythonProject(FtBaseProject):
    def __init__(self, settings, verbose=False):
        super(FtPythonProject, self).__init__(settings, verbose)

    def _post_project_structure_phase(self):
        super()._post_project_structure_phase()
        module_dir = os.path.join(self.settings.project_directory, "modules")
        new_module_dir = os.path.join(self.settings.project_directory, self.settings.name.lower())
        os.rename(module_dir, new_module_dir)

