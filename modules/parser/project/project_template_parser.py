import yaml
import os

class ProjectTemplateParser:
    def __init__(self, template_file):
        try:
            self.template = yaml.load(open(template_file, 'r'), Loader=yaml.FullLoader)["structure"]
        except Exception:
            self.template = []
        self.begin_marker = "[ftt]"
        self.end_marker = "[#ftt]"

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
        try:
            self.template = yaml.load(open(template_file, 'r'), Loader=yaml.FullLoader)["structure"]
        except Exception:
            self.template = []
        try:
            self.params = yaml.load(open(template_file, 'r'), Loader=yaml.FullLoader)["params"]
        except Exception:
            self.params = []

    def get_project_items(self):
        directories = []
        files = {}
        try:
            self._get_files_and_directories(self.template, directories, files)
        except Exception:
            directories = []
            files = {}
        return directories, files

# TODO replace with regex
    def get_line(self, line, params):
        begin_marker_index = line.find(self.begin_marker)
        begin_marker_end_index = begin_marker_index + len(self.begin_marker)
        end_marker_index = line.find(self.end_marker)
        end_marker_end_index = end_marker_index + len(self.end_marker)
        if begin_marker_index < end_marker_index and begin_marker_index > 0 and begin_marker_index > 0:
            param = line[begin_marker_end_index:end_marker_index].split(".")
            if getattr(params, param[1]) is not None:
                line = line.replace(line[begin_marker_index:end_marker_end_index], getattr(params, param[1]))
        return line
