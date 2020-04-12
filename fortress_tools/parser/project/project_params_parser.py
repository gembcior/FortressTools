import yaml

class ProjectParamsParser:
    def __init__(self, params_file):
        self.begin_marker = "[ftt]"
        self.end_marker = "[#ftt]"
        self.params = yaml.load(open(params_file, 'r'), Loader=yaml.FullLoader)

    def load(self, params_file):
        self.template = yaml.load(open(params_file, 'r'), Loader=yaml.FullLoader)

    def get_line(self, line):
        begin_marker_index = line.find(self.begin_marker)
        begin_marker_end_index = begin_marker_index + len(self.begin_marker)
        end_marker_index = line.find(self.end_marker)
        end_marker_end_index = end_marker_index + len(self.end_marker)
        if begin_marker_index < end_marker_index and begin_marker_index > 0 and begin_marker_index > 0:
            param = line[begin_marker_end_index:end_marker_index].split(".")
            for item in self.params[param[0]]:
                if item.get(param[1]) is not None:
                    line = line.replace(line[begin_marker_index:end_marker_end_index], item[param[1]])
        return line
