import yaml
import os

class ProjectTemplateParser:
    def __init__(self):
        self.template = None

    def _get_files_and_directories(self, data, directories, files, previous_dir=""):
        for x in data:
            if type(data[x]) is str:
                files.update({os.path.join(previous_dir, x) : data[x]})
            elif type(data[x]) is dict:
                temp_previous_dir = os.path.join(previous_dir, x)
                directories.append(temp_previous_dir)
                self._get_files_and_directories(data[x], directories, files, temp_previous_dir)
            elif data[x] is None:
                directories.append(os.path.join(previous_dir, x))

    def load(self, template_file):
        self.template = yaml.load(open(template_file, 'r'), Loader=yaml.FullLoader)["root"]

    def get_project_items(self):
        directories = []
        files = {}
        self._get_files_and_directories(self.template, directories, files)
        return directories, files
