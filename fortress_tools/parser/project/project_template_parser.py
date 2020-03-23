import yaml


class ProjectTemplateParser:

    def run(self, template_file):
        print("Project Template Parser run")
        yaml_file = yaml.load(open(template_file, 'r'), Loader=yaml.FullLoader)["root"]
        for x in yaml_file:
            print(x)
